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
        # super(AbstractOptimizer, self).__init__()
        # self.init_graph = kwarg.get('init_nodes_func',None)
        # self.order = kwarg.get('order_func',None) # order nodes if needed
        # self.get_score = kwarg.get('get_score_func',None)
        # self.get_bad_node = kwarg.get('get_bad_node_func',None)
        # self.get_sub_node = kwarg.get('get_sub_node_func',None)
        # self.node_container = {'pointer':None, 'node_copy':None}
        # self.swap = kwarg.get('swap_func',None)
        # self.choose_graph = kwarg.get('choose_graph_func',None)
        # self.calc_stats = kwarg.get('calc_stats_func',None)
        # self.visualize = kwarg.get('visualize_func',None)
        self.nodes = None  # all graph nodes in ordered object
        self.set = None  # chosen state of graph -- some ordered object of indeces
        self.new_set = None # storage for new (unchosen) state of graph
        self.score = None
        self.new_score = None
        self.statisitcs = None
        logger.debug(self.__class__.__name__+" object created")
    def copy_set(self):
        self.new_set = self.set
    def get_score(self,a_set=False,new=False):
        def get_max_derivative(the_set):
            temp_list = []
            for i,pair in enumerate(tools.pairwise(the_set)):
                d_val = self.nodes[pair[-1]] - self.nodes[pair[0]]
                d_i = 1.
                temp_list.append(d_val/d_i)
            return max(temp_list)
        if a_set:
            return get_max_derivative(a_set)
        elif new:
            self.score = get_max_derivative(self.new_set)
            return True
        else:
            self.new_score = get_max_derivative(self.set)
            return True


        return 
    def choose_set(self):
        score = self.get_score(self.graph)
        nscore = self.get_score(self.ngraph)
        if nscore < score:
            self.graph = self.ngraph
            return True
        else:
            pass
            return False
    def update_statistics(self):
        return
        
    def __str__(self):
        return "AbstractOptimizer object has variables:\n" + tools.print_vars_values_types(self)

def abstract_optimizer_test():
    logger.debug('simple optimizer started')
    a = AbstractOptimizer()
    logger.debug(a)
    a.nodes = np.arange(10,100,10)
    a.set = tuple(np.arange(a.nodes.shape[0]))
    logger.debug("set:\n" + str(a.set))
    logger.debug("new set:\n" + str(a.new_set))
    logger.debug(a)
    logger.debug(a.get_score())
    logger.debug(a.score)
    a.copy_set()
    logger.debug(a.get_score(new=True))
    logger.debug(a.new_score)
    logger.debug(a.get_score([0,0,0,0,0,0]))
    # print(repr(a))
    logger.debug('simple optimizer finished')

def main():
    pass

if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("optimizer script run directly")
    # logging.disable(logging.INFO)
    # logging.disable(logging.NOTSET)
    abstract_optimizer_test()
    logger.info("optimizer script finished running")