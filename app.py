# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect

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

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    func_name, func_args = inspect.stack()[0][3],  inspect.getargvalues(inspect.currentframe())[3]
    # caller_name, func_name, func_args = inspect.stack()[1][3], inspect.stack()[0][3],  inspect.getargvalues(inspect.currentframe())[3]
    logger.debug(" %s with args = %s" % (func_name, func_args))
    logger.info("Main skript started")

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
        nodes_coords_list = [moscow.coords] + [loc.coords for loc in locs_list] + [moscow.coords] 
        return locs_list, nodes_coords_list

    FILE_WITH_COORDS_PAIRS_NAME = "cities_coords.txt"

    def put_locs_to_file(nodes_coords_list,fname=FILE_WITH_COORDS_PAIRS_NAME,):
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

    ## run this when need to update cities coords / change cities list
    # locs_list, nodes_coords_list = generate_locations()
    # put_locs_to_file(FILE_WITH_COORDS_PAIRS_NAME,nodes_coords_list)

    # run this to only prepare the tsp test
    nodes_coords_list = read_coords_from_file() # only variable nodes` coords here
    cars_num = 5
    # # cities_num=100
    only_var_nodes = nodes_coords_list[1:-1]
    cities_num=(len(only_var_nodes))
    cities_per_car = cities_num//cars_num

    parts = [only_var_nodes[car_i*cities_per_car : (car_i+1)*cities_per_car] for car_i in range(cars_num)]
    part_start_finish = [[nodes_coords_list[0]] + part + [nodes_coords_list[-1]] for part in parts]
        
    for i,part in enumerate(part_start_finish):
        part_cities_fname = "cities_coords_part_%d.txt" % (i)
        put_locs_to_file(part,part_cities_fname)


    # for i,part in enumerate(part_start_finish):
    #     print("first city in part %s" % str(part[0]))
    #     print("first city num in part %d" % (i*len(part)))
    #     print(len(part))
    #     print("last city in part %s" % str(part[-1]))
    #     print("last city in num part %d" % ((i+1)*len(part)))
    #     for i,c_coords in enumerate(part):
    #         print("i: %d coords: %s" % (i,c_coords))

    # print("moscow:%s" % (nodes_coords_list[0]))
    # print("moscow:%s" % (nodes_coords_list[-1]))
    import sys
    sys.exit(0)

    # setting up tsp module
    move_operator_name = "swapped_cities"
    max_itterations = 10000 # test value
    # max_itterations = 1000000 # best value
    alg_type = "anneal"
    start_temp = 100 # best value
    alpha = 0.99  # best value
    cooling_str = ''.join([str(start_temp),':',str(alpha)])
    cities_coords_fname = FILE_WITH_COORDS_PAIRS_NAME
    tsp_params_list = ['tspm.py','-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,cities_coords_fname]
    import sys
    sys.argv = tsp_params_list
    result_tuple = tspm.main()
    # new_locs_list = [nodes_coords_list[index] for index in result_tuple[-1]]
    locs_coords_list = [nodes_coords_list[index] for index in result_tuple[-1]]
    fig_on_gmap = bokehm.Figure(output_fname='othodi_app_test_%f.html' % (result_tuple[1]),use_gmap=True, center_coords=nodes_coords_list[0])
    # locs_coords_list = [l.coords for l in new_locs_list]
    # for i,loc in enumerate(new_locs_list):
    #     fig_on_gmap.add_line([loc.coords],circle_size=5+10*float(i)/len(new_locs_list), circles_color='red',alpha=0.5)
    fig_on_gmap.add_line(locs_coords_list,circle_size=5+10, circles_color='red',alpha=0.5)

    fig_on_gmap.add_line([nodes_coords_list[0]],circle_size=35, circles_color='green',alpha=0.5)
    fig_on_gmap.save2html()
    # fig_on_gmap.show()
    
    for i,part in enumerate(part_start_finish):
        fig_on_gmap = bokehm.Figure(output_fname='othodi_app_test_%f.html' % (result_tuple[1]),use_gmap=True, center_coords=nodes_coords_list[0])
        fig_on_gmap.add_line(locs_coords_list,circle_size=5+10, circles_color='red',alpha=0.5)
        fig_on_gmap.add_line([nodes_coords_list[0]],circle_size=35, circles_color='green',alpha=0.5)
        fig_on_gmap.save2html()

    # cars_num = 5
    # cities_per_car = 100//cars_num
    # for car_num in range(cars_num):
    #     for city_num in range(car_num*cities_per_car, car_num+1*cities_per_car,1):
    #         print(city_num)
    # sys.exit(0)


    ## plotting routes
    # fig_on_gmap = bokehm.Figure(output_fname='othodi_app_test.html',use_gmap=True, center_coords=moscow.coords)
    # for route,loc in zip(routes_list,locs_list):
    #     fig_on_gmap.add_line(route.waypoints,circle_size=5, circles_color='red',alpha=0.5)
    #     fig_on_gmap.add_line([loc.coords],circle_size=15, circles_color='green',alpha=0.3)
    # fig_on_gmap.save2html()
    # fig_on_gmap.show()
