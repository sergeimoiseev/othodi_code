# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, sys, copy
import numpy as np
import anneal_optimizer, splitter_optimizer
# import haversine
logger = logging.getLogger(__name__)

def test_init_optimize_one_route():
    n_cities = 20
    nodes_data = tools.get_nodes_data(nodes_num = n_cities, recreate_nodes_data=False)
    return nodes_data

def optimize_one_route(nodes_data,max_split_part = 10):
    s = splitter_optimizer.init_split_optimizer(nodes_data)
    max_nodes_in_part = max_split_part
    indices = s.split_anneal_a_route(max_nodes_in_part)

    moscow = locm.Location(address='Moscow')
    plot = bokehm.Figure(output_fname='a_route_annealed_splitted.html',center_coords=moscow.coords,use_gmap=True,)
    step_grid = np.arange(len(indices))
    plot.add_line(nodes_data[indices], circle_size=step_grid,circles_color='red',alpha= 0.5,no_line = False)
    plot.save2html()
    
if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("optimize_one_route script run directly")
    nodes_data = test_init_optimize_one_route()
    optimize_one_route(nodes_data)
    logger.info("optimize_one_route script finished running")
