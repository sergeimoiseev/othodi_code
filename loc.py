# -*- coding: utf-8 -*-
from tools import type_of_value
import gmaps, catalog_of_wastes

class Location(object):
	def __init__(self, *args, **kwargs):
		#args -- tuple of anonymous arguments
		#kwargs -- dictionary of named arguments
		# print('creating location from')
		# print("args")
		# print(args)
		# print(isinstance(args[0], float))
		# print(isinstance(args[1], float))
		# print("kwargs")
		# print(kwargs)
		if isinstance(args[0], float) and isinstance(args[1], float):
			self._coords = {'lat':args[0],'lng': args[1]}
			self._address = gmaps.get_address(self._coords)
		elif type_of_value(args[0])!=str and type_of_value(args[1])!=str:
			self._coords = {'lat':float(args[0]),'lng': float(args[1])}
			self._address = gmaps.get_address(self._coords)
		elif type_of_value(args[0])==str and kwargs.get('address',None)==None:
			self._address = args[0]
			self._coords = gmaps.get_lat_lon(args[0])
		elif len(args)==0 and kwargs.get('address',None)!=None:
			self._address = kwargs['address']
			self._coords = gmaps.get_lat_lon(kwargs['address'])
		else:
			raise ValueError("Pass address as anonymous argument OR as a keyword argument")
		self.name = kwargs.get('object_name',None)
		waste_names = kwargs.get('type',[])
		if type_of_value(waste_names)==str:
			self.types = [waste_names] 
		elif all(isinstance(waste_names, str) for waste_names in kwargs['type']):
			self.types = waste_names
		else:
			raise ValueError("Waste types must be set with string OR list of strings")

		self._id = id(self)
		
	def to_str(self):
			return "%s: %s, %s" % (self.name,str(self._coords), self._address)

	@property
	def coords(self):
		return self._coords
	@property
	def address(self):
		return self._address
	@property
	def id(self):
		return self._id        

def create_locations_list(fname):
	locs = []
	with open(fname,'r') as f:
		for line in f:
			props = line.strip().split(',')
			loc = Location(props[1],props[2],object_name=props[0])
			locs.append(loc)
	return locs

if __name__ == "__main__":
	s1 = Location("54.8","88.6")
	s2 = Location(54.3,88.5)
	# s2 = Location("Moscow")
	print(s1.coords)
	# s1.coords = {'we': 21, 'wee': 23}
	# print(s1.coords)
	import tools
	print(tools.distance_straight(s1.coords,s2.coords))
	import maps
	mo = maps.Map(locations = [s1,s2])

	import gmaps
	cities_names = ['Moscow','Sarov','Krasnogorsk','Zelenograd','Dubna']
	sample_filename = tools.write_sample_cities_data_to_file(cities_names)
	locs_list = create_locations_list(sample_filename)
	str_lst = [loc.to_str() for loc in locs_list]
	for el in str_lst:
		print(el)

	origin = Location("Moscow")
	raw_routes = []
	for location in locs_list[1:]:
		raw_routes.append(gmaps.get_route(origin.coords, location.coords))

		#!!! rewrite:
	from operator import itemgetter
	raw_routes.sort(key=itemgetter(-1)) # sort by duration
	from pprint import pprint as pp
	pp(raw_routes)
	import plot_routes  
	add_points_coords_list = [(point.coords['lat'],point.coords['lng']) for point in locs_list]
	add_points_annotes_list = [point.name for point in locs_list]
	plot_routes.plot_route_on_basemap(raw_routes[0][0], raw_routes[0][1], [add_points_coords_list,add_points_annotes_list]) # plots nearest route