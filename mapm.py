# -*- coding: utf-8 -*-
"""
class Map
	properties
		locations
	methods
		get_route
		plot(), plot_location(), add_route(loc1,loc2), distance(self,loc1,loc2)
"""

import tools, locm, gmaps
import time

class Map(object):
    def __init__(self, **kwargs):
        #args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
        self.locations = kwargs.get('locations',[])
        self.routes = kwargs.get('routes',[])
    def lan_lng(self, *args, **kwargs):
        if 'locations' in args:
            lat_list = [point.coords['lat'] for point in self.locations]
            lng_list = [point.coords['lng'] for point in self.locations]
        elif 'routes' in args:
            lat_list = [point.coords['lat'] for point in self.locations]
            lng_list = [point.coords['lng'] for point in self.locations]
        return lat_list, lng_list 
    def add_locations_from_file(self, fname=None,dropbox=False):
        if dropbox:
            import dropboxm
            dc = dropboxm.DropboxConnection()
            f = dc.open_dropbox_file(fname)
        elif not fname:
            f = open('test_city_names_list.txt','r')
        else:
            raise ValueError("wrong arguments given to Map#add_locations_from_file()")
        for line in f:
            if '#' in line: # scip commented lines
                continue
            time.sleep(0.5)  # 10 requests per second - google api
            try:
                new_loc = locm.Location(address=line.strip(),name=line.strip())
                self.locations.append(new_loc)
            except Exception as e:
                print('Can`t create a location. Error:\n%s' % e)
        return True

if __name__ == "__main__":
    pass
    # import locm, gmaps
    # import frontend_mpl_basemap as mpl_bm_fr

    # l1 = locm.Location(54.54,56.65)
    # l2 = locm.Location(56.65,54.54)
    # m1 = Map(locations=[l1,l2])
    # print(m1.locations)
    # print(m1.routes)
    # print(m1.locations[0].to_str())
    # dropbox_filename = '/othodi/cities.txt'
    # m1=Map()
    # m1.add_locations_from_file(fname=dropbox_filename,dropbox=True)
    # print(len(m1.locations))

    # origin = locm.Location("Moscow",name='Moscow')
    # raw_routes = []
    # for location in [locn for locn in m1.locations if locn.name != origin.name]:
    #     if 'lat' in location.coords and 'lng' in location.coords:
    #         raw_routes.append(gmaps.get_route(origin.coords, location.coords))

    # from operator import itemgetter
    # raw_routes.sort(key=itemgetter(-1)) # sort by duration
    # for i,point in enumerate(m1.locations):
    #     print("%i: %s" % (i,str(point.coords)))
    # add_points_coords_list = [(point.coords['lat'],point.coords['lng']) for point in m1.locations]
    # add_points_annotes_list = [point.name for point in m1.locations]
    # import frontend_mpl_basemap as frontend
    # frontend.plot_route_on_basemap(raw_routes[0][0], raw_routes[0][1], [add_points_coords_list,add_points_annotes_list]) # plots nearest route
    # for loc in m1.locations:
    #     pp(loc)