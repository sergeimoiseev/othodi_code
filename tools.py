# -*- coding: utf-8 -*-
"""
Some useful methods
"""

import ast
from pprint import pprint as pp
import logging
import numpy as np
logger = logging.getLogger(__name__)

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

def get_string_caller_objclass_method(obj,inspect_stack):
    return "\n%s() -> " % (inspect_stack[1][3])+obj.__class__.__name__+"#%s()" % (inspect_stack[0][3])

def print_vars_values_types(obj):
    out_str = ""
    sorted_var_list = [revvar[::-1] for revvar in sorted([var[::-1] for var in  dir(obj)])]
    # sorted_var_list = sorted(dir(obj))
    for var in sorted_var_list:
        if not (var.startswith("__") and var not in ['os','sys']):
            cons_width = 80
            out_str_part = ''
            try:
                var_value = obj.__dict__[var]
            except KeyError:
                continue
            out_str_part += var + " "*(cons_width/4-len(var)) + str(var_value)[:cons_width/2]
            out_str_part += " "*(cons_width/2-len(str(var_value)[:cons_width/2])) + str(type(var_value))
            out_str_part = out_str_part[:cons_width-1] + "\n"
            out_str += out_str_part
    return out_str

import itertools
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None) # b itterator is moved one step forward from initial position
    return itertools.izip(a, b)

# s_l = [revvar[::-1] for revvar in sorted([var[::-1] for var in ['aa','ab','ba','bba','baa']])]
# print(s_l)


def get_nodes_data(recreate_nodes_data=False):
    nodes_fname = 'nodes.txt'
    if recreate_nodes_data:
        # create locations -> nodes -> dump nodes to file
        cities_fname = 'test_city_names_list_21.txt'
        # cities_fname = 'test_city_names_list_100.txt'
        with open(cities_fname,'r') as cities_file:
            address_list = [line.strip() for line in cities_file.readlines()]
        locs_list = [locm.Location(addr) for addr in address_list[0:5]]

        # ('potential', np.float64, 1),    ,('radius',np.float64,1)
        nodes_data = []
        for loc in locs_list:
            if len(loc.address)!=0 and len(loc.coords)!=0:
                nodes_data.append((loc.address,loc.coords.values()))
        with open(nodes_fname,'w') as nodes_file:
            for node in nodes_data:
                nodes_file.write("%s,%s,%s\n" % (node[0],node[1][0],node[1][1]))
    else:
        # read nodes from file
        nodes_data = []
        with open(nodes_fname,'r') as nodes_file:
            for l in nodes_file.readlines():
                parts = l.strip().split(',')
                nodes_data.append(tuple(parts))

    logger.debug("nodes_data\n%s" % (nodes_data,))
    node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    np_nodes_data = np.array(nodes_data, dtype = node_dtype)
    return np_nodes_data