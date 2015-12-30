# -*- coding: utf-8 -*-
"""
class Map
	properties
		locations
	methods
		get_route
		plot_part(), plot_location(), add_route(loc1,loc2), distance(self,loc1,loc2)
"""

import tools

class Map(object):
    def __init__(self, **kwargs):
    	#args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
    	self.locations = kwargs.get('locations',[])
    	self.routes = kwargs.get('routes',[])
    def plot_part(frontend,south_west_corner_coords,north_east_corner_coords):
    	return "No frontends implemented yet"
    def plot_location(frontend,location):
    	return "No frontends implemented yet"
    def add_route(self,loc1,loc2):
    	return "Not implemented yet"
    def distance(self,loc1,loc2):
    	return tools.distance_straight(loc1.coords,loc2.coords)

if __name__ == "__main__":
	import loc
	l1 = loc.Location(54.54,56.65)
	l2 = loc.Location(56.65,54.54)
	m1 = Map(locations=[l1,l2])
	print(m1.locations)
	print(m1.routes)
	print(m1.locations[0].to_str())
		