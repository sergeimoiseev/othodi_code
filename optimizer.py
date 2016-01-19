# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math
import numpy as np


class AbstractOptimizer(object):
    """AbstractOptimizer class provides 
    storage for function names
    used by a real optimizer."""
    def __init__(self, **kwarg):
        super(AbstractOptimizer, self).__init__()
        self.init_graph = kwarg.get('init_nodes_func',None)
        self.graph = None  # chosen state of graph -- some ordered object with unique nodes
        self.ngraph = None # storage for new (unchosen) state of graph
        self.order = kwarg.get('order_func',None) # order nodes if needed
        self.get_score = kwarg.get('get_score_func',None)
        self.score = None
        self.get_bad_node = kwarg.get('get_bad_node_func',None)
        self.get_sub_node = kwarg.get('get_sub_node_func',None)
        self.node_container = {'pointer':None, 'node_copy':None}
        self.swap = kwarg.get('swap_func',None)
        self.choose_graph = kwarg.get('choose_graph_func',None)
        self.calc_stats = kwarg.get('calc_stats_func',None)
        self.visualize = kwarg.get('visualize_func',None)

    def __str__(self):
        return "AbstractOptimizer object has variables:\n" + tools.print_vars_values_types(self)

    def dummy_func():
        pass

def simple_optimizer():
    logger.info('simple optimizer started')
    a = AbstractOptimizer()
    print(a)
    print(repr(a))
    logger.info('simple optimizer finished')

def main():
    pass

if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("optimizer script run directly")
    # logging.disable(logging.INFO)
    # logging.disable(logging.NOTSET)
    simple_optimizer()m,. 