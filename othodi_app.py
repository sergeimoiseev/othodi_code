# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml

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
    
    # logging.config.fileConfig('logging.conf')
    # fh = logging.FileHandler('%s.log' % sys.argv[0].split('.')[0])
    # fh.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logger.addHandler(fh)

    cities_fname = 'test_city_names_list.txt'
    # cities_fname = 'cities_from_dropbox.txt'
    ## dr_fname = '/othodi/cities_few.txt'
    ## dc = dropboxm.DropboxConnection()
    ## with dc.open_dropbox_file(dr_fname) as dropbox_file:
    ##     address_list = [line.strip() for line in dropbox_file]
    with open(cities_fname,'r') as cities_file:
        address_list = [line.strip() for line in cities_file.readlines()]

    locs_list = [locm.Location(addr) for addr in address_list]
    moscow = locm.Location(address='Moscow')
    # routes_list = [routem.Route(moscow.coords,dest.coords) for dest in locs_list]
    # for route,loc in zip(routes_list,locs_list):
    #     print(loc.address)
    #     print(route.to_str())

    nodes_coords_list = [moscow.coords] + [loc.coords for loc in locs_list] + [moscow.coords] 
    FILE_WITH_COORDS_PAIRS_NAME = "cities_coords.txt"
    with open(FILE_WITH_COORDS_PAIRS_NAME,'w') as coords_file:
        for coord_pair_dict in nodes_coords_list:
            coords_file.write("%f" % coord_pair_dict[u'lat'])
            coords_file.write(',')
            coords_file.write("%f" % coord_pair_dict[u'lng'])
            coords_file.write("\n")
    import sys
    # setting up tsp module
    move_operator_name = "swapped_cities"
    max_itterations = 1000000 # 
    alg_type = "anneal"
    start_temp = 25
    alpha = 0.99
    cooling_str = ''.join([str(start_temp),':',str(alpha)])
    cities_coords_fname = FILE_WITH_COORDS_PAIRS_NAME
    tsp_params_list = ['tspm.py','-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,cities_coords_fname]
    sys.argv = tsp_params_list
    result_tuple = tspm.main()
    print(result_tuple)
    new_locs_list = [locs_list[index-1] for index in result_tuple[-1][1:-1]]
    fig_on_gmap = bokehm.Figure(output_fname='othodi_app_test.html',use_gmap=True, center_coords=moscow.coords)
    locs_coords_list = [l.coords for l in new_locs_list]
    # for i,loc in enumerate(new_locs_list):
    #     fig_on_gmap.add_line([loc.coords],circle_size=5+10*float(i)/len(new_locs_list), circles_color='red',alpha=0.5)
    fig_on_gmap.add_line(locs_coords_list,circle_size=5+10, circles_color='red',alpha=0.5)

    fig_on_gmap.add_line([moscow.coords],circle_size=35, circles_color='green',alpha=0.5)
    fig_on_gmap.save2html()
    fig_on_gmap.show()
    
    sys.exit(0)


    ## plotting routes
    # fig_on_gmap = bokehm.Figure(output_fname='othodi_app_test.html',use_gmap=True, center_coords=moscow.coords)
    # for route,loc in zip(routes_list,locs_list):
    #     fig_on_gmap.add_line(route.waypoints,circle_size=5, circles_color='red',alpha=0.5)
    #     fig_on_gmap.add_line([loc.coords],circle_size=15, circles_color='green',alpha=0.3)
    # fig_on_gmap.save2html()
    # fig_on_gmap.show()
