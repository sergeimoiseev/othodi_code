# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math
import numpy as np

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

def try_to_guess_routes():

    cities_fname = 'test_city_names_list_100.txt'
    # cities_fname = 'test_city_names_list_21.txt'
    # cities_fname = 'test_city_names_list.txt'
    # cities_fname = 'cities_from_dropbox.txt'

    FILE_WITH_COORDS_PAIRS_NAME = "cities_coords.txt"


    moscow = locm.Location(address='Moscow')
    ## run this when need to update cities coords / change cities list
    # locs_list, nodes_coords_list = generate_locations()
    # put_locs_to_file(nodes_coords_list,fname = FILE_WITH_COORDS_PAIRS_NAME)

    ## routes_list = [routem.Route(moscow.coords,dest.coords) for dest in locs_list]
    ## for route,loc in zip(routes_list,locs_list):
    ##     print(loc.address)
    ##     print(route.to_str())

    # run this to only prepare the tsp test
    nodes_coords_list = read_coords_from_file(FILE_WITH_COORDS_PAIRS_NAME) # only variable nodes` coords here

    tsp_params_list = get_tsp_params_list(FILE_WITH_COORDS_PAIRS_NAME)
    import sys
    logger.error("max_itterations = %d" % (tsp_params_list[4]))
    sys.argv = tsp_params_list
    result_tuple = tspm.main()

    locs_coords_list = [nodes_coords_list[index] for index in result_tuple[-1]]
    plot_fname =  'othodi_app_test_%d_%f.html' % (len(nodes_coords_list),result_tuple[1])
    fig_on_gmap = bokehm.Figure(output_fname=plot_fname,use_gmap=True, center_coords=nodes_coords_list[0])
    # fig_on_gmap.add_line(locs_coords_list,circle_size=1, circles_color='red',alpha=1.)
    # fig_on_gmap.add_line([nodes_coords_list[0]],circle_size=35, circles_color='green',alpha=0.5)
    # fig_on_gmap.save2html()
    # fig_on_gmap.show()
    
    cars_num = 5
    # # cities_num=100
    only_var_nodes = locs_coords_list[1:-1]
    cities_num=(len(only_var_nodes))
    cities_per_car = cities_num//cars_num
    print("cities_per_car=%d" % cities_per_car)

    parts = [only_var_nodes[car_i*cities_per_car : (car_i+1)*cities_per_car] for car_i in range(cars_num)]
    parts_indeces = [range(car_i*cities_per_car,(car_i+1)*cities_per_car,1) for car_i in range(cars_num)]
    # print(parts_indeces)
    # print(parts)
    
    best_scores_list = []
    best_routes_list = []

    colors_list = ["red","green","blue","orange","pink"]
    # parts_with_start_finish = [[nodes_coords_list[0]] + part + [nodes_coords_list[-1]] for part in parts]
    put_locs_to_file(locs_coords_list[1:-1],fname = "cities_coords_all_in_order.txt")
    for i,part in enumerate(parts):
        part_coords_file_name = "cities_coords_part_%d.txt" % (i)
        put_locs_to_file(part,fname = part_coords_file_name)

        logger.info("reading var nodes` coords from file - one car route evaluation")
        nodes_coords_list = read_coords_from_file(part_coords_file_name) # only variable nodes` coords here

        tsp_params_list = get_tsp_params_list(part_coords_file_name)
        import sys
        sys.argv = tsp_params_list
        logger.info("starting part route evaluation")
        result_tuple = tspm.main()

        logger.info("preparing list of dicts of coords for plotting")
        locs_coords_list = [tver_coords]+[nodes_coords_list[index] for index in result_tuple[-1]] + [ryazan_coords] 
        # locs_coords_list = [moscow.coords]+[nodes_coords_list[index] for index in result_tuple[-1]]+[moscow.coords]
        # fig_on_gmap = bokehm.Figure(output_fname='o_part_%d_ncities_%d_%f.html' % (i,len(part),result_tuple[1]),use_gmap=True, center_coords=nodes_coords_list[0])
        circle_sizes = [(i*3) for index in locs_coords_list]
        fig_on_gmap.add_line(locs_coords_list,circle_size=circle_sizes, circles_color=colors_list[i],alpha=0.5)
        # fig_on_gmap.add_line([nodes_coords_list[0]],circle_size=35, circles_color=colors_list[i],alpha=0.5)
        logger.error("a car route: part %d ncities=%d length=%f" % (i,len(part),result_tuple[1]))
        best_scores_list.append(result_tuple[1])
        best_routes_list.append(result_tuple[-1])
    fig_on_gmap.save2html()

    return best_scores_list,best_routes_list,plot_fname 

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

if __name__ == "__main__":
    os.remove("app.log")
    setup_logging()
    logger = logging.getLogger(__name__)
    func_name, func_args = inspect.stack()[0][3],  inspect.getargvalues(inspect.currentframe())[3]
    # caller_name, func_name, func_args = inspect.stack()[1][3], inspect.stack()[0][3],  inspect.getargvalues(inspect.currentframe())[3]
    logger.debug(" %s with args = %s" % (func_name, func_args))
    logger.info("Main skript started")

    CITIES_FNAME = 'test_city_names_list_100.txt'
    with open(CITIES_FNAME,'r') as cities_file:
        names = [addr.strip() for addr in cities_file.readlines()]
        # locs_list = [locm.Location(addr.strip()) for addr in cities_file.readlines()]
    # nodes_coords_list = [loc.coords for loc in locs_list] 

    FILE_WITH_COORDS_PAIRS_NAME = "c_pairs_"+CITIES_FNAME
    # put_locs_to_file(nodes_coords_list,fname = FILE_WITH_COORDS_PAIRS_NAME)
    nodes_clist = read_coords_from_file(FILE_WITH_COORDS_PAIRS_NAME) # only variable nodes` coords here

    # calc potetial
    nodes_clist_of_tuples = [tuple(d.values()) for d in nodes_clist]
    cm = tspm.cartesian_matrix(nodes_clist_of_tuples)

    r_to_start_list = [r(tver_coords,node_cd) for node_cd in nodes_clist]

    # создание несортированного списка узлов-городов-точек
    unsorted_nodes = []
    pl = create_potential_list(nodes_clist_of_tuples,tver_coords,ryazan_coords)
    for pot, name,i,c_dict,r_s in zip(pl,names,range(len(names)),nodes_clist,r_to_start_list):
        # print("%d:%s %.3f  %s" % (i,name, pot,str(c_dict)))
        if len(name)!=0 and pot!=0 and len(c_dict)!=0:
            unsorted_nodes.append((i,name,pot,c_dict.values(),r_s))
    
    # создание и сортировка списка узлов с потенциалами
    node_dtype = dt = np.dtype([('idx', np.int32, 1), ('name',np.str_, 16), ('potential', np.float64, 1), ('coords', np.float64, 2),('rs',np.float64,1)])
    pln = np.array(unsorted_nodes,dtype = node_dtype)
    pln.sort(order = 'potential')  # sorted by potential
    # разбиение соритрованного списка на части по возрастанию потенциала
    n_cars = 5
    n_nodes = len(pln)
    n_per_route =  n_nodes//n_cars
    splitted_pln = np.split(pln,n_per_route)
    # print(splitted_pln[0])
    # выделение ниток маршрутов для каждой машины
    car_routes = np.empty((n_cars,n_per_route),dtype = node_dtype)
    for part_num, split_part in enumerate(splitted_pln):
        equi_nodes = np.copy(split_part)
        logger.info("equi_nodes before sorting by proximity to prev node\n%s" % str(equi_nodes))
        
        for car_number in range(n_cars):
            logger.info("car number %d" % car_number)
            if part_num == 0: # первый узел в нитке проставляем просто по порядку узлов в списке эквипотенциальных
            # с наименьшим потенциалом
                car_routes[car_number][part_num] = split_part[car_number]
                logger.info("first node assigned to this car`s route :\n%s" % split_part[car_number])
            else:  
                # НЕТ! в поле rs каждого непривязанного узла записываем расстояние до последнего узла в маршруте этой машины
                # logger.info("last node in route :\n%s" % str(car_routes[car_number][part_num-1]))
                # next_nodes_arb_rs = []
                # for node in equi_nodes:
                #     next_nodes_arb_rs.append(r(car_routes[car_number][part_num-1]['coords'],node['coords']))
                # equi_nodes['rs'] = next_nodes_arb_rs
                # equi_nodes.sort(order = 'rs')
                # logger.info("equi_nodes after sorting by proximity to prev node\n%s" % str(equi_nodes))
                logger.info("car_routes \n%s" % str(car_routes[car_number][0:part_num]))
                logger.info("equi_nodes \n%s" % str(equi_nodes))
                thread_len = len(car_routes[car_number][0:part_num])
                equi_nodes_num = len(equi_nodes)
                # proximity_m = np.fromfunction(lambda i, j: r(car_routes[car_number][i]['coords'],equi_nodes[j]['coords']), (thread_len, equi_nodes_num), dtype=np.float64)
                # proximity_m = np.fromfunction(lambda i, j: r(car_routes[car_number][i],tver_coords), (thread_len, equi_nodes_num), dtype=np.float64)
                # proximity_m = np.fromfunction(lambda i, j: i+j/100., (thread_len, equi_nodes_num), dtype=np.float64)
                # logger.info("proximity matrix:\n%s" % proximity_m)

                # рассчитаем расстояния между всеми парами (узел_в_нитке : узел_из_эквипотенциальных)
                # записываем расстояния в матрицу float-ов (proximity_matrix)
                proximity_matrix=np.empty((thread_len, equi_nodes_num), dtype=np.float64)
                for i,c1 in enumerate(car_routes[car_number][0:part_num]['coords']):
                    for j,c2 in enumerate(equi_nodes['coords']):
                        proximity_matrix[i,j]=r(c1,c2)
                # logger.info("proximity matrix:\n%s" % proximity_matrix)

                # нужен только номер столбца, в котором обнаружен минимальный элемент - 
                # это и будет номер того из эквипотенциальных узлов,
                # который ближе всего к одному из (забудем к какому) узлу из узлов будущего маршрута                 
                _ ,equi_nodes_min_idx = np.unravel_index(np.argmin(proximity_matrix), proximity_matrix.shape)
                # logger.info("equi_nodes_min_idx :\n%s" % str(equi_nodes_min_idx))
                car_routes[car_number][part_num] = equi_nodes[equi_nodes_min_idx]
                logger.info("node added to route :\n%s" % equi_nodes[equi_nodes_min_idx])
                equi_nodes = np.delete(equi_nodes, equi_nodes_min_idx)
                logger.info("equi_nodes after delete\n%s" % str(equi_nodes))

                # car_routes[car_number][part_num] = equi_nodes[0]
                # logger.info("node assigned :\n%s" % equi_nodes[0])
                # equi_nodes = np.delete(equi_nodes, 0)
                # # logger.info("nodes remaining: \n%s" % str(equi_nodes))
                # # восстанавливаю поле rs для выстраивания маршрута по расстоянию от пункта отправления
                # car_routes[car_number][part_num]['rs'] = split_part[0]['rs']


    for car_route in car_routes:
        car_route.sort(order = 'rs')
    # print(car_routes['rs'])
    routes_coords_dicts_lists = create_coords_dicts_lists(car_routes)
    car_routes_length = np.empty(len(car_routes),dtype = np.float64)
    for car_idx, car_route in enumerate(car_routes):
        logger.info("calc_route_length for route\n%s" % car_route)
        car_routes_length[car_idx] = calc_route_length(car_route['coords'])
    logger.info("routes length:\n%s" % car_routes_length)
    
    import sys
    sys.exit(0)    

    moscow = locm.Location(address='Moscow')
    fig_on_gmap = bokehm.Figure(output_fname='threads_pot_sorted_nearest.html',use_gmap=True, center_coords=moscow.coords)
    circle_sizes = 10
    colors_list = ['red','green','blue','orange','yellow']
    for car_number in range(n_cars):
        fig_on_gmap.add_line(routes_coords_dicts_lists[car_number],circle_size=circle_sizes, circles_color=colors_list[car_number],alpha=1.)
    fig_on_gmap.show()


    # t_start = time.time()
    # best_scores,nearest_routes,plot_file_name = [],[],""
    # # stdev_of_length = 10.
    # # mean_length = -100.
    # while True:
    #     best_scores,nearest_routes,plot_file_name = try_to_guess_routes()
    #     arr = np.array(best_scores)
    #     logger.error("mean_best_score = %.4f +- %.4f" % (float(np.mean(arr, axis=0)), float(np.std(arr, axis=0))))
    #     stdev_of_length=float(np.std(arr, axis=0))
    #     mean_length=float(np.mean(arr, axis=0))
    #     if stdev_of_length<1. and mean_length>-10.: break
    
    # t_stop = time.time()
    # delta_t = t_stop - t_start
    # logger.error("route with small stdev plotted: %s, time elapsed=%.2f seconds" % (plot_file_name,delta_t))