# -*- coding: utf-8 -*-
"""
Some useful methods
"""

import ast
from pprint import pprint as pp

def type_of_value(var):
    try:
       return type(ast.literal_eval(var))
    except Exception:
       return str


import math
def distance_straight(coords1, coords2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1 = coords1['lng'], coords1['lat']
    lon2, lat2 = coords2['lng'], coords2['lat']
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def write_sample_cities_data_to_file(cities_names):
	import gmaps
	out_fname = 'example_locs_to_read_from.txt'
	with open(out_fname,'w') as f:
		for name in cities_names:
			coords = gmaps.get_lat_lon(name)
			# print(coords)
			f.write("%s,%f,%f\n" % (name,coords['lat'],coords['lng']))
	print("sample cities data written to file '%s'" % out_fname)
	return out_fname


def get_pairs_list_from_dicts_list(coords_list_of_dicts):
	#"""needed in gmaps module"""
    p_list = []
    for a_dict in coords_list_of_dicts:
        p_list.append((a_dict[u'lat'],a_dict[u'lng']))
    return p_list

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


def print_vars_values_types(obj):
    out_str = ""
    for var in dir(obj):
        if not (var.startswith("__") and var not in ['os','sys']):
            col_width = 40
            try:
                var_value = obj.__dict__[var]
            except KeyError:
                continue
            out_str += var + " "*(col_width/2-len(var)) + str(var_value)[:col_width]
            out_str += " "*(col_width-len(str(var_value)[:col_width])) + str(type(var_value)) + "\n"
    return out_str

import itertools
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None) # b itterator is moved one step forward from initial position
    return itertools.izip(a, b)