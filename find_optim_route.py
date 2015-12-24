# -*- coding: utf-8 -*-
import plot_routes
def test_plot_routes():
    # cities_data_dict = {'Tver':[],'Krasnogorsk':[],'Moscow':[],'Sarov':[]}
    cities_data_dict = {'Tver':[],'Krasnogorsk':[],'Voskresensk':[],'Sarov':[],'Dmitrov':[]}

    for key,data_list in cities_data_dict.iteritems():
        data_list.append(plot_routes.get_lat_lon_by_address(key))

    # coords_tver = plot_routes.get_lat_lon_by_address('Tver')
    # coords_krasnogorsk = plot_routes.get_lat_lon_by_address('Krasnogorsk')
    coords_moscow = plot_routes.get_lat_lon_by_address('Moscow')
    # coords_sarov = plot_routes.get_lat_lon_by_address('Sarov')
    # print(coords_tver)
    # print(coords_krasnogorsk)
    # print(coords_moscow)

    for key,el in cities_data_dict.iteritems():
        print(key)
        print(len(el))
        print(el)

    for key,data_list in cities_data_dict.iteritems():
        data_list.append(plot_routes.get_route_from_gmaps(coords_moscow,data_list[0]))

    for key,el in cities_data_dict.iteritems():
        print(key)
        print(len(el))
        print(el[-1][-1]/(60.*60),"hours")

    
    sorted_routes = sorted(cities_data_dict.items(), key=lambda x:x[-1][-1][-1])
    print(sorted_routes)
    for city in sorted_routes:
        print("%s, %f hours"%(city[0],city[-1][-1][-1]/(60*60.)))
        # print(city[1][1][0])
        # print(city[1][1][1])
        print(city[1][0])
        # print(len(el))
        # print(el[-1][-1]/(60.*60),"hours")
    # print(len(sorted_routes[0][1][1]))
    # print(len(sorted_routes[0][1][1][0]))
    # print(len(sorted_routes[0][1][1][1]))
    
    cities_coords = []
    cities_names = []
    for city in sorted_routes:
        cities_coords.append(plot_routes.get_pairs_list_from_dicts_list([city[1][0]])[0])
        cities_names.append(city[0])

    print(cities_names)
    print(cities_coords)

    plot_routes.plot_route_on_basemap(sorted_routes[0][1][1][0], sorted_routes[0][1][1][1],added_points_param_list=[cities_coords,cities_names])

    return True

def test():
	dur_to_closest = 0.
	dist_to_closest = 0.

	return dur_to_closest, dist_to_closest

if __name__ == "__main__":
    ret = test_plot_routes()
    print(ret)