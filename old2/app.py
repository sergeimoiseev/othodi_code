# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import numpy, time

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

def try_to_guess_routes():

    def generate_locations():
        cities_fname = 'test_city_names_list_100.txt'
        # cities_fname = 'test_city_names_list_21.txt'
        # cities_fname = 'test_city_names_list.txt'
        # cities_fname = 'cities_from_dropbox.txt'
        with open(cities_fname,'r') as cities_file:
            address_list = [line.strip() for line in cities_file.readlines()]

        locs_list = [locm.Location(addr) for addr in address_list]
        moscow = locm.Location(address='Moscow')
        # routes_list = [routem.Route(moscow.coords,dest.coords) for dest in locs_list]
        # for route,loc in zip(routes_list,locs_list):
        #     print(loc.address)
        #     print(route.to_str())
        nodes_coords_list = [tver_coords] + [loc.coords for loc in locs_list] + [ryazan_coords] 
        # nodes_coords_list = [moscow.coords] + [loc.coords for loc in locs_list] + [moscow.coords] 
        return locs_list, nodes_coords_list

    FILE_WITH_COORDS_PAIRS_NAME = "cities_coords.txt"

    def put_locs_to_file(nodes_coords_list, fname=FILE_WITH_COORDS_PAIRS_NAME):
        with open(fname,'w') as coords_file:
            for coord_pair_dict in nodes_coords_list:
                coords_file.write("%f" % coord_pair_dict[u'lat'])
                coords_file.write(',')
                coords_file.write("%f" % coord_pair_dict[u'lng'])
                coords_file.write("\n")

    def read_coords_from_file(fname = FILE_WITH_COORDS_PAIRS_NAME):
        with open(fname,'r') as coords_file:
            nodes_coords_list_of_lists = [line.strip().split(',') for line in coords_file]
            nodes_coords_list = [{u'lat':float(l[0]),u'lng':float(l[1])}for l in nodes_coords_list_of_lists]
        # for line in coord_file:
        #     x,y=line.strip().split(',')
        #     coords.append((float(x),float(y)))
        return nodes_coords_list

    moscow = locm.Location(address='Moscow')
    ## run this when need to update cities coords / change cities list
    # locs_list, nodes_coords_list = generate_locations()
    # put_locs_to_file(nodes_coords_list,fname = FILE_WITH_COORDS_PAIRS_NAME)

    # run this to only prepare the tsp test
    nodes_coords_list = read_coords_from_file() # only variable nodes` coords here

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

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    func_name, func_args = inspect.stack()[0][3],  inspect.getargvalues(inspect.currentframe())[3]
    # caller_name, func_name, func_args = inspect.stack()[1][3], inspect.stack()[0][3],  inspect.getargvalues(inspect.currentframe())[3]
    logger.debug(" %s with args = %s" % (func_name, func_args))
    logger.info("Main skript started")

    t_start = time.time()
    best_scores,nearest_routes,plot_file_name = [],[],""
    # stdev_of_length = 10.
    # mean_length = -100.
    while True:
        best_scores,nearest_routes,plot_file_name = try_to_guess_routes()
        arr = numpy.array(best_scores)
        logger.error("mean_best_score = %.4f +- %.4f" % (float(numpy.mean(arr, axis=0)), float(numpy.std(arr, axis=0))))
        stdev_of_length=float(numpy.std(arr, axis=0))
        mean_length=float(numpy.mean(arr, axis=0))
        if stdev_of_length<1. and mean_length>-10.: break
    
    t_stop = time.time()
    delta_t = t_stop - t_start
    logger.error("route with small stdev plotted: %s, time elapsed=%.2f seconds" % (plot_file_name,delta_t))