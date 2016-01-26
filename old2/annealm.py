# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math
import numpy as np
import random
logger = logging.getLogger(__name__)

tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}

def setup_logging(
    default_path='app_logging.yaml', 
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def get_tsp_params_list(cities_coords_fname):
    # setting up tsp module
    move_operator_name = "swapped_cities"
    max_itterations = 10000 # test value
    # max_itterations = 1000000 # best value
    alg_type = "anneal"
    start_temp = 100 # best value
    alpha = 0.99  # best value
    cooling_str = ''.join([str(start_temp),':',str(alpha)])
    cities_coords_fname = cities_coords_fname
    tsp_params_list = ['tspm.py','-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,cities_coords_fname]
    return tsp_params_list

def generate_locations(cities_fname):
    with open(cities_fname,'r') as cities_file:
        address_list = [line.strip() for line in cities_file.readlines()]

    locs_list = [locm.Location(addr) for addr in address_list]
    moscow = locm.Location(address='Moscow')
    nodes_coords_list = [tver_coords] + [loc.coords for loc in locs_list] + [ryazan_coords] 
    # nodes_coords_list = [moscow.coords] + [loc.coords for loc in locs_list] + [moscow.coords] 
    return locs_list, nodes_coords_list

def put_locs_to_file(nodes_coords_list, fname):
    with open(fname,'w') as coords_file:
        for coord_pair_dict in nodes_coords_list:
            coords_file.write("%f" % coord_pair_dict[u'lat'])
            coords_file.write(',')
            coords_file.write("%f" % coord_pair_dict[u'lng'])
            coords_file.write("\n")

def read_coords_from_file(fname):
    with open(fname,'r') as coords_file:
        nodes_coords_list_of_lists = [line.strip().split(',') for line in coords_file]
        nodes_coords_list = [{u'lat':float(l[0]),u'lng':float(l[1])}for l in nodes_coords_list_of_lists]
    return nodes_coords_list

def r(c1,c2):
    def convert(c):
        if type(c)!=type({}):
            return {'lat':c[0],'lng':c[1]}
        return c
    c1,c2 = convert(c1),convert(c2)
    return math.sqrt((c2['lat']-c1['lat'])**2 + (c2['lng']-c1['lng'])**2)

def create_potential_list(coords_tuples,start_coords,finish_coords):
    '''create a potential list for every city'''
    potential_list=[]
    xs,xf = start_coords['lat'],finish_coords['lat']
    ys,yf = start_coords['lng'],finish_coords['lng']
    for i,(x,y) in enumerate(coords_tuples):
        dxs,dys=x-xs,y-ys
        dxf,dyf=xf-x,yf-y
        potential=math.sqrt(dxs*dxs + dys*dys)+math.sqrt(dxf*dxf + dyf*dyf)
        potential_list.append(potential)
    return potential_list

def create_coords_dicts_lists(node_dtype_routes):
    coords_dicts_lists = np.empty(node_dtype_routes.shape,dtype = [('lat',np.float64,1),('lng',np.float64,1)])
    for route_n, part in enumerate(node_dtype_routes['coords']):
        coords_dicts_lists[route_n]['lat'] = [pair[0] for pair in part]
        coords_dicts_lists[route_n]['lng'] = [pair[1] for pair in part]
    return coords_dicts_lists

import itertools
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None) # b itterator is moved one step forward from initial position
    return itertools.izip(a, b)

def calc_route_length(route_coords):
    length = 0.
    for pair in pairwise(route_coords):
        length += r(pair[0],pair[1])
    return length

def get_proximity_matrix(from_coords, to_coords):
    proximity_matrix=np.empty((len(from_coords), len(to_coords)), dtype=np.float64)
    for i,c1 in enumerate(from_coords):
        for j,c2 in enumerate(to_coords):
            proximity_matrix[i,j]=r(c1,c2)
    return proximity_matrix

def get_init_car_routes(pln,node_dtype):
    # сортировка списка узлов по потенциалу
    pln.sort(order = 'potential')  # sorted by potential
    # разбиение соритрованного списка на части по возрастанию потенциала
    n_cars = 5
    n_nodes = len(pln)
    n_per_route =  n_nodes//n_cars
    splitted_pln = np.split(pln,n_per_route) # количество частей равно количеству городов в каждом маршруте
    # выделение ниток маршрутов для каждой машины
    car_routes = np.empty((n_cars,n_per_route),dtype = node_dtype)
    for part_num, split_part in enumerate(splitted_pln):
        equi_nodes = np.copy(split_part)
        logger.debug("equi_nodes before sorting by proximity to prev node\n%s" % str(equi_nodes))
        
        for car_number in range(n_cars):
            logger.debug("car number %d" % car_number)
            if part_num == 0: # первый узел в нитке проставляем просто по порядку узлов в списке эквипотенциальных
            # с наименьшим потенциалом
                car_routes[car_number][part_num] = split_part[car_number]
                logger.debug("first node assigned to this car`s route :\n%s" % split_part[car_number])
            else:  
                logger.debug("car_routes \n%s" % str(car_routes[car_number][0:part_num]))
                logger.debug("equi_nodes \n%s" % str(equi_nodes))
                # рассчитаем расстояния между всеми парами (узел_в_нитке : узел_из_эквипотенциальных)
                # записываем расстояния в матрицу float-ов (proximity_matrix)
                proximity_matrix = get_proximity_matrix(car_routes[car_number][0:part_num]['coords'], equi_nodes['coords'])
                # нужен только номер столбца, в котором обнаружен минимальный элемент - 
                # это и будет номер того из эквипотенциальных узлов,
                # который ближе всего к одному из (забудем к какому) узлу из узлов будущего маршрута                 
                _ ,equi_nodes_min_idx = np.unravel_index(np.argmin(proximity_matrix), proximity_matrix.shape)
                car_routes[car_number][part_num] = equi_nodes[equi_nodes_min_idx]
                logger.debug("node added to route :\n%s" % equi_nodes[equi_nodes_min_idx])
                equi_nodes = np.delete(equi_nodes, equi_nodes_min_idx)
                logger.debug("equi_nodes after delete\n%s" % str(equi_nodes))

    # сортируем каждый маршрут по расстоянию от начала
    # так чтобы узлы маршрута шли по очереди без колец
    for car_route in car_routes:
        car_route.sort(order = 'rs')
    return car_routes

def calc_all_routes_len(car_routes):
    car_routes_length = np.empty(len(car_routes),dtype = np.float64)
    for car_idx, car_route in enumerate(car_routes):
        logger.debug("calc_route_length for route\n%s" % car_route)
        car_routes_length[car_idx] = calc_route_length(car_route['coords'])
    return car_routes_length

def plot_routes(routes_coords_dicts_lists, fname = 'init_cars_routes.html',title_=''):
    routes_num = len(routes_coords_dicts_lists)
    moscow = locm.Location(address='Moscow')
    fig_on_gmap = bokehm.Figure(output_fname=fname,use_gmap=True, center_coords=moscow.coords,title=title_)
    circle_sizes = 10
    colors_list = ['red','green','blue','orange','yellow']*int(routes_num//5+1)
    for car_number in range(routes_num):
        fig_on_gmap.add_line(routes_coords_dicts_lists[car_number],circle_size=circle_sizes, circles_color=colors_list[car_number],alpha=1.)
    fig_on_gmap.save2html()
    # fig_on_gmap.show()

def select_node_to_replace_worst(pln_,worst_route_,worst_node_of_worst_route_,random_radius = -1):
    # ищем среди всех узлов в других маршрутах узел ближайший к этому, с возможно меньшим потенциалом
    mask = np.in1d(pln_, worst_route_)
    logger.debug("nodes of worst route:\n%s" % worst_route_['name'])
    nodes_to_select_from = np.copy(pln_[np.where(~mask)])
    logger.debug("nodes_to_select_from:\n%s" % nodes_to_select_from['name'])
    proximity_list = get_proximity_matrix([worst_node_of_worst_route_['coords']],nodes_to_select_from['coords'])
    logger.debug("proximity_list to worst route:\n%s" % proximity_list)
    # проставляю расстояния до худшего узла в копии списка узлов (вместо расстояния до старта - в поля rs)
    nodes_to_select_from['rs']=proximity_list
    # сортирую сначала по потенциалу, затем по расстоянию до худшего узла
    indxs = np.argsort(nodes_to_select_from, order=('rs', 'potential'))
    nodes_to_select_from = nodes_to_select_from[indxs]  # список ближайших узлов (со второй сортировкой по потенциалу)
    logger.info("indeces of nodes_to_select_from:\n%s" % nodes_to_select_from['idx'])
    logger.debug("nodes_to_select_from after multiple order sort:\n%s" % nodes_to_select_from['name'])
    # перебираем ближайшие узлы по очереди, пока не найдется узел, потенциал которого меньше чем у худшего
    for node in nodes_to_select_from:
        if node['potential']<=worst_node_of_worst_route_['potential']:
            node_to_replace_worst = np.copy(node)
            break # теоретически, "выгодной" перестановки может и не найтись
        if node == nodes_to_select_from[-1]: # все перебрали, условие не выполнено - подставляем самый ближний узел
            logger.info("finished search, node not found - replacing by first nearest")
            node_to_replace_worst = np.copy(nodes_to_select_from[0])
    return node_to_replace_worst

def guess_node_to_replace_worst(pln_,worst_route_,worst_node_of_worst_route_,proximity_swap_propability,random_radius = -1):
    mask = np.in1d(pln_, worst_route_)
    logger.debug("nodes of worst route:\n%s" % worst_route_['name'])
    nodes_to_select_from = np.copy(pln_[np.where(~mask)])
    logger.debug("nodes_to_select_from:\n%s" % nodes_to_select_from['name'])
    proximity_list = get_proximity_matrix([worst_node_of_worst_route_['coords']],nodes_to_select_from['coords'])
    logger.debug("proximity_list to worst route:\n%s" % proximity_list)
    # проставляю расстояние до худшего узла в копии списка узлов (вместо расстояния до старта в поля rs)
    nodes_to_select_from['rs']=proximity_list
    # сортирую сначала по потенциалу, затем по расстоянию до худшего узла
    indxs = np.argsort(nodes_to_select_from, order=('rs', 'potential'))
    nodes_to_select_from = nodes_to_select_from[indxs]  # список ближайших узлов со второй сортировкой по потенциалу
    logger.debug("nodes_to_select_from after multiple order sort:\n%s" % nodes_to_select_from['name'])

    # присваеваем узлу вероятность выбора обратную расстоянию до него
    proxim_arr = 1/nodes_to_select_from['rs']
    sum_of_proxim_arr = np.sum(proxim_arr)
    normed_proxim_arr = proxim_arr/sum_of_proxim_arr
    logger.debug("normed proximity array:\n%s"% (normed_proxim_arr))
    # угадываем в цикле, пока не найдется узел, потенциал которого меньше чем у худшего
    tries_quantity = 100
    node_to_replace_worst = np.copy(nodes_to_select_from[0])
    for try_num in range(tries_quantity):
        if proximity_swap_propability:
            node_guessed = np.random.choice(nodes_to_select_from, 1, p=normed_proxim_arr)[0]
        else:
            node_guessed = np.random.choice(nodes_to_select_from, 1, p=[1./len(nodes_to_select_from)]*len(nodes_to_select_from))[0]
        if node_guessed['potential']<=worst_node_of_worst_route_['potential']: # !!! не факт, что оптимальное условие
            logger.info("node_guessed:\n%s" % node_guessed)
            node_to_replace_worst = np.copy(node_guessed)
            break # теоретически, "выгодной" перестановки может и не найтись
        if node_to_replace_worst == nodes_to_select_from[-1]: # все перебрали, условие не выполнено - подставляем самый ближний узел
            logger.info("finished search, node not found - replacing by first nearest")
    return node_to_replace_worst

def swap_nodes(car_routes,first_node,second_node): 
    worst_node_of_worst_route = first_node
    node_to_replace_worst = second_node
    w_idx = worst_node_of_worst_route['idx']
    r_idx = node_to_replace_worst['idx']
    w_idx_routes = np.where(car_routes['idx']==w_idx)
    r_idx_routes = np.where(car_routes['idx']==r_idx)
    car_routes[w_idx_routes]=node_to_replace_worst
    car_routes[r_idx_routes]=worst_node_of_worst_route

def P(prev_score,next_score,temperature):
    if next_score < prev_score:
        return 1.0
    else:
        return math.exp( -abs(next_score-prev_score)/temperature )

def kirkpatrick_cooling(start_temp,alpha):
    T=start_temp
    while True:
        yield T
        T=alpha*T
def main(STAT_LENGTH,ANNEAL,START_TEMP,ALPHA):
    try:
        os.remove("app.log")
    except:
        logger.info("Error while removing logfile - mayby file not found.")
        pass
    func_name, func_args = inspect.stack()[0][3],  inspect.getargvalues(inspect.currentframe())[3]
    logger.debug(" %s with args = %s" % (func_name, func_args))
    logger.info("Main skript started")

    # выбор режима работы
    STOCHASTIC = True
    COOLING = True
    if not ANNEAL:
        DOWNHILL = True
    else:
        DOWNHILL = False
    

    if COOLING:
        cooling_schedule = kirkpatrick_cooling(START_TEMP,ALPHA)
    else:
        cooling_schedule = [1.5]*STAT_LENGTH
    
    PROXIMITY_MATTERS = True
    GUESS_RADIUS = -1  # радиус, внутри которого буду выбираться узлы на замену текущем
    # текущий в центре - радиус отсчитывается от него

    # использовать историю перестановок?
    SWAP_ONCE = False

    # сколько можно сделать итераций?
    # инициализация списка узлов - это список пар координат
    CITIES_FNAME = 'test_city_names_list_100.txt'
    FILE_WITH_COORDS_PAIRS_NAME = "c_pairs_"+CITIES_FNAME

    # применение настроек: выбор функций
    if STOCHASTIC:
        find_node_to_replace_worst = guess_node_to_replace_worst
    else:
        find_node_to_replace_worst = select_node_to_replace_worst

    with open(CITIES_FNAME,'r') as cities_file:
        names = [addr.strip() for addr in cities_file.readlines()]
        # locs_list = [locm.Location(addr.strip()) for addr in cities_file.readlines()]
    # nodes_coords_list = [loc.coords for loc in locs_list] 
    # put_locs_to_file(nodes_coords_list,fname = FILE_WITH_COORDS_PAIRS_NAME)
    nodes_clist = read_coords_from_file(FILE_WITH_COORDS_PAIRS_NAME) # only variable nodes` coords here
    nodes_clist_of_tuples = [tuple(d.values()) for d in nodes_clist]
    r_to_start_list = [r(tver_coords,node_cd) for node_cd in nodes_clist]

    # создание несортированного списка узлов (=городов=точек)
    # свойства каждого узла: i (номер города в исходном файле),name (название),pot (потенциал - сумма расстояний от начала и от финиша),c_dict.values() (пара координат),r_s (расстояние от старта)
    unsorted_nodes = []
    pl = create_potential_list(nodes_clist_of_tuples,tver_coords,ryazan_coords)
    for pot, name,i,c_dict,r_s in zip(pl,names,range(len(names)),nodes_clist,r_to_start_list):
        if len(name)!=0 and pot!=0 and len(c_dict)!=0:
            unsorted_nodes.append((i,name,pot,c_dict.values(),r_s))
    node_dtype = np.dtype([('idx', np.int32, 1), ('name',np.str_, 16), ('potential', np.float64, 1), ('coords', np.float64, 2),('rs',np.float64,1)])
    pln = np.array(unsorted_nodes,dtype = node_dtype) # список узлов в numpy array
    
    # аккуратно выбираем начальные маршруты для каждой из машин
    car_routes = get_init_car_routes(pln,node_dtype)

    # вычисляем длины начальных маршрутов каждой из машин
    car_routes_length = calc_all_routes_len(car_routes)
    # сортируем маршруты по длине
    routes_order_by_length = car_routes_length.argsort()
    car_routes = car_routes[routes_order_by_length]
    logger.info("routes initial in length order:\n%s" % car_routes['name'])
    # logger.info("routes len - initial routes:\n%s" % car_routes_length)
    car_routes_length = calc_all_routes_len(car_routes)
    logger.info("routes len after sort:\n%s" % car_routes_length)
    
    # рисуем начальные маршруты
    # routes_coords_dicts_lists = create_coords_dicts_lists(car_routes)
    # plot_routes(routes_coords_dicts_lists, fname = 'init_cars_routes.html')
    
    # инициализация статистики по длине маршрута
    routes_mean_len_old = float(np.mean(car_routes_length, axis=0))
    routes_mean_len_std_old = float(np.std(car_routes_length, axis=0))
    # лучший набор маршрутов инициализируем начальным
    best_routes = np.copy(car_routes)

    stat_dtype=np.dtype([('idx',np.int32,1),('mean',np.float64,1), ('std',np.float64,1)])
    len_statisitcs = np.zeros(STAT_LENGTH,dtype=stat_dtype)
    len_statisitcs[0]['idx'] = 0
    len_statisitcs[0]['mean'], len_statisitcs[0]['std'] = routes_mean_len_old, routes_mean_len_std_old
    logger.info("len of statisitcs:\n%s" % len(len_statisitcs))

    worst_node_of_worst_route = np.zeros(1,dtype = node_dtype)
    already_replaced_nodes = np.zeros(0,dtype = node_dtype)


    # улучшение маршрутов
    for i in range(1, len(len_statisitcs)):
        logger.debug("routes before swap of worst node:\n%s" % car_routes['name'])
        worst_route = np.copy(car_routes[-1]) # копируем маршрут с самой большой длиной
        worst_route.sort(order = 'potential')
        worst_route = worst_route[::-1]
        for node in worst_route:
            if node['name'] not in already_replaced_nodes['name']:
                logger.info("new worst node:\n%s" % node['name'])
                worst_node_of_worst_route = np.copy(node) # копируем "самый затратный" узел - узел с наибольшим потенциалом
                break
        if worst_node_of_worst_route['name'] == '':
            break # прекращаем перебор: все узлы в этом маршруте уже когда-то были "худшими"
        logger.info("worst_node of worst route:\n%s" % worst_node_of_worst_route)
        
        node_to_replace_worst = find_node_to_replace_worst(pln,worst_route,worst_node_of_worst_route,proximity_swap_propability=PROXIMITY_MATTERS,random_radius = GUESS_RADIUS) # использование одной из функций выбора узла на замену
        logger.info("node_to_replace_worst:\n%s" % node_to_replace_worst)

        # в списке маршрутов меняем местами худший и тот, что выбрали на замену
        new_car_routes = np.copy(car_routes)
        swap_nodes(new_car_routes,worst_node_of_worst_route,node_to_replace_worst)

        # сортируем каждый маршрут по расстоянию от начала
        # так чтобы узлы маршрута шли по очереди (без колец и обратного хода)
        for car_route in new_car_routes:
            for node in car_route:
                node['rs']=r(ryazan_coords,node['coords'])
            car_route.sort(order = 'rs')

        # обновляем несортированный список узлов
        pln = new_car_routes.flatten()

        # сортируем маршруты по длине
        car_routes_length = calc_all_routes_len(new_car_routes)
        routes_order_by_length = car_routes_length.argsort()
        new_car_routes = new_car_routes[routes_order_by_length]
        logger.debug("routes after swap of worst node:\n%s" % new_car_routes['name'])
        car_routes_length = calc_all_routes_len(new_car_routes)
        logger.debug("routes len after sort:\n%s" % car_routes_length)
        
        routes_mean_len_new = float(np.mean(car_routes_length, axis=0))
        routes_mean_len_std_new = float(np.std(car_routes_length, axis=0))

        if ANNEAL:
            temperature = next(cooling_schedule)
            # probablistically accept this solution
            # always accepting better solutions
            p=P(routes_mean_len_old,routes_mean_len_new,temperature)
            if random.random() < p:
                car_routes = new_car_routes
                logger.info("ANNEAL changed state from: %.3f to %.3f" % (routes_mean_len_old,routes_mean_len_new))
        elif DOWNHILL:
            if routes_mean_len_old > routes_mean_len_new:
                car_routes = new_car_routes
                logger.info("DOWNHILL changed state from: %.3f to %.3f" % (routes_mean_len_old,routes_mean_len_new))
        else:  # not DOWNHILL or ANNEAL
            car_routes = new_car_routes

        if routes_mean_len_new<np.amin(len_statisitcs['mean']):
            best_routes = np.copy(car_routes)
        len_statisitcs[i]['idx'] = i
        len_statisitcs[i]['mean'], len_statisitcs[i]['std'] = routes_mean_len_new, routes_mean_len_std_new
        routes_mean_len_old = routes_mean_len_new
        routes_mean_len_std_old = routes_mean_len_std_new
        
        if SWAP_ONCE: # не переставлять узлы, которые хотя бы раз переставлялись
            already_replaced_nodes_list = list(already_replaced_nodes)
            if worst_node_of_worst_route['name'] not in already_replaced_nodes['name']:
                already_replaced_nodes_list.append(worst_node_of_worst_route)
                already_replaced_nodes = np.array(already_replaced_nodes_list,dtype=node_dtype)
                logger.info("already_replaced_nodes updated:\nlen\n%s\nnames\n%s" % (len(already_replaced_nodes),already_replaced_nodes['name']))
        else: # не хранить историю: переставлять узлы, которые уже переставлялись
            pass
    finish_temp = next(cooling_schedule)
    logger.info("finish temp:\n%f" % finish_temp)

    if ANNEAL:
        MODE = 'ANNEAL'
    elif DOWNHILL:
        MODE = 'DOWNHILL'
    else:
        MODE = None

    logger.debug("len statisitcs:\n%s" % len_statisitcs)
    if ANNEAL:
        outfname = 'stLEN=%d_ANNEAL_Tst%.2f_a%.2f_score%.3f.html'%(STAT_LENGTH,START_TEMP,ALPHA,np.amin(len_statisitcs['mean']))
        stat_title = '%s prox%s,hist%s Ts%.2fa%.2fTf%.2f' % (MODE,PROXIMITY_MATTERS,SWAP_ONCE,START_TEMP,ALPHA,finish_temp)
    elif DOWNHILL:
        outfname = 'stLEN=%d_DOWNHILL_score%.3f.html'%(STAT_LENGTH,np.amin(len_statisitcs['mean']))
        stat_title = '%s prox%s,histor%s score%.3f' % (MODE,PROXIMITY_MATTERS,SWAP_ONCE,np.amin(len_statisitcs['mean']))
    else:
        outfname = 'len_stats_plot_STAT_LENGTH=%d.html'%(STAT_LENGTH)
        stat_title = '%s prox-ty_mats=%s,hist_mats=%s' % (MODE,PROXIMITY_MATTERS,SWAP_ONCE)
    fig_stats = bokehm.Figure(output_fname=outfname,use_gmap=False,title = stat_title)
    # fig_stats = bokehm.Figure(output_fname='len_stats_plot_STAT_LENGTH=%d.html'%(STAT_LENGTH),use_gmap=False,title = 'guess_r=%.2f\n prox-ty_mats=%s,hist_mats=%s' % (GUESS_RADIUS,PROXIMITY_MATTERS,SWAP_ONCE))
    fig_stats.add_errorbar(len_statisitcs['idx'], len_statisitcs['mean'], yerr=len_statisitcs['std'])
    # fig_stats.add_text()
    fig_stats.save2html()
    # fig_stats.show()

    # рисуем текущее состояние маршрутов
    routes_coords_dicts_lists = create_coords_dicts_lists(car_routes)
    # plot_routes(routes_coords_dicts_lists, fname = 'routes_after_determined_algorythm.html',title_ = 'last routes, mean=%.2f' % (routes_mean_len_old))

    # рисуем текущее состояние маршрутов
    routes_coords_dicts_lists = create_coords_dicts_lists(best_routes)
    # plot_routes(routes_coords_dicts_lists, fname = 'best_route_by_determined_algorythm.html',title_ = 'best routes, mean=%.2f' % (np.amin(len_statisitcs['mean'])))
    return np.amin(len_statisitcs['mean']), finish_temp, best_routes
    
if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    STAT_LENGTH = 1000
    ANNEAL = True
    START_TEMP,ALPHA = 0.1,0.999
    main(STAT_LENGTH,ANNEAL,START_TEMP,ALPHA)
