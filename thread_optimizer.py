# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, sys, copy
import numpy as np
import anneal_optimizer
import haversine
# haversine((45.7597, 4.8422),(48.8567, 2.3508),miles = True)243.71209416020253
logger = logging.getLogger(__name__)

class ThreadOptimizer(anneal_optimizer.AnnealOptimizer):
    """ThreadOptimizer class provides 
    splitter
    based on AnnealOptimizer."""

    def __init__(self, start = None, finish = None, **kwarg):
        super(ThreadOptimizer, self).__init__()
        self.start = start
        self.finish = finish
        # self.set = None
        # self.new_set = None
        self.threads_scores = None
        self.score = None
        self.new_score = None
        self.n_threads = None
        self.node4threading_dtype = [(name,self.node_dtype[name]) for name in self.node_dtype.names] + [('potential', np.float64, 1),('proximity', np.float64, 1)]

    def get_score(self,a_set_):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        full_score = 0.
        # threads_scores = []
        logger.debug("self.set\n%s" % (self.set,))
        for thread_number,thread_idxs in enumerate(self.set):
            logger.debug("thread_idxs\n%s" % (thread_idxs,))
            a = anneal_optimizer.AnnealOptimizer()
            a.nodes = np.take(self.nodes,thread_idxs)
            a.start = self.start
            a.finish = self.finish
            a.set = list(np.arange(a.nodes.shape[0]))
            a.SORT_ON = True
            a.set = a.sort(a.set)
            logger.debug("after sort a.nodes[a.set]['name']\n%s" % (a.nodes[a.set]['name'],))
            a.update_stats()
            # a.plot_route_from_stats()
            # threads_scores.append(a.score)
            full_score += a.score
        return full_score
        
    def create_threads(self):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        # node4threading_dtype = [(name,self.node_dtype[name]) for name in self.node_dtype.names] + [('potential', np.float64, 1),('proximity', np.float64, 1)]
        nodes4threading = np.zeros(self.nodes.shape[0],dtype = self.node4threading_dtype)
        for node,n4s in zip(self.nodes,nodes4threading):
            n4s['name'] = node['name']
            n4s['lat'] = node['lat']
            n4s['lng'] = node['lng']
            n4s['potential'] =  tools.r([self.start['lat'],self.start['lng']],[node['lat'],node['lng']]) + \
                                tools.r([self.finish['lat'],self.finish['lng']],[node['lat'],node['lng']])
        nodes4threading = np.sort(nodes4threading,order=('potential'))
        logger.debug("nodes4threading\n%s" % (nodes4threading,))
        sorted_indices = []
        for node_name in nodes4threading['name']:
            sorted_indices.append(np.where(self.nodes['name'] == node_name)[0][0])
        sorted_indices = np.array(sorted_indices)
        # logger.debug("sorted_indices\n%s" % (sorted_indices,))
        n_per_route = self.nodes.shape[0]//self.n_threads
        logger.debug("n_per_route\n%s" % (n_per_route,))
        if self.nodes.shape[0] % self.n_threads != 0.:
            logger.error("nodes left behind by threading - remainder of division is not 0")
        splitted_sorted_indices = np.split(sorted_indices,n_per_route)
        logger.debug("splitted_sorted_indices\n%s" % (splitted_sorted_indices,))

        thr_idxs = np.zeros((self.n_threads,n_per_route),dtype = np.int32)
        for part_num, split_part_indices in enumerate(splitted_sorted_indices):
            part_nodes = np.take(nodes4threading,split_part_indices)
            for thread_n in range(self.n_threads):
                if part_num==0:
                    thr_idxs[thread_n][part_num] = split_part_indices[thread_n]# первый узел в нитке проставляем просто по порядку узлов в списке эквипотенциальных с наименьшим потенциалом
                else:
                    prev_nodes_idxs = thr_idxs[thread_n][0:part_num]
                    prev_nodes = np.take(nodes4threading,split_part_indices)
                    prev_nodes_coords = [ [node['lat'],node['lng']] for node in prev_nodes]
                    part_nodes_coords = [ [node['lat'],node['lng']] for node in part_nodes if node['name']!='']
                    proximity_matrix = tools.get_proximity_matrix(prev_nodes_coords,part_nodes_coords)
                    _ ,equi_nodes_min_idx = np.unravel_index(np.argmin(proximity_matrix), proximity_matrix.shape)
                    
                    next_node_in_thread_name = part_nodes[equi_nodes_min_idx]['name']
                    thr_idxs[thread_n][part_num] = \
                                                np.where(nodes4threading['name']==next_node_in_thread_name)[0][0]
                    logger.debug("node added to route :\n%s" % nodes4threading[thr_idxs[thread_n][part_num]])
                    part_nodes = np.delete(part_nodes, equi_nodes_min_idx)
                    logger.debug("part_nodes after delete\n%s" % str(part_nodes))
        logger.debug("thr_idxs\n%s" % (thr_idxs,))
        self.set = thr_idxs
        self.threads_scores = np.zeros((self.n_threads),dtype = np.float64)


    def calc_scores(self):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        self.score = 0.
        logger.debug("self.set\n%s" % (self.set,))
        for thread_number,thread_idxs in enumerate(self.set):
            logger.debug("thread_idxs\n%s" % (thread_idxs,))
            a = anneal_optimizer.AnnealOptimizer()
            a.nodes = np.take(self.nodes,thread_idxs)
            a.start = self.start
            a.finish = self.finish
            a.set = list(np.arange(a.nodes.shape[0]))
            a.SORT_ON = True
            a.set = a.sort(a.set)
            logger.debug("after sort a.nodes[a.set]['name']\n%s" % (a.nodes[a.set]['name'],))
            a.update_stats()
            # a.plot_route_from_stats()
            self.threads_scores[thread_number] = a.score
            self.score += a.score

    def get_worst_thread_and_bad_node(self):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        max_score = max(self.threads_scores)
        longest_thread_index = [i for i,j in enumerate(self.threads_scores) if j == max_score][0]
        thread_nodes = np.take(self.nodes,self.set[longest_thread_index])
        nodes4sorting = np.zeros(thread_nodes.shape[0],dtype = self.node4threading_dtype)
        for node,n4s in zip(thread_nodes,nodes4sorting):
            n4s['name'] = node['name']
            n4s['lat'] = node['lat']
            n4s['lng'] = node['lng']
            n4s['potential'] =  tools.r([self.start['lat'],self.start['lng']],[node['lat'],node['lng']]) + \
                                tools.r([self.finish['lat'],self.finish['lng']],[node['lat'],node['lng']])
        nodes4sorting = np.sort(nodes4sorting,order=('potential'))[::-1]
        logger.debug("nodes4sorting\n%s" % (nodes4sorting,))
        return longest_thread_index, nodes4sorting[0]

    def get_nearest_node(self, indices_to_choose_from, node_name):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        part_nodes = np.take(self.nodes, indices_to_choose_from)
        logger.debug("part_nodes\n%s" % (part_nodes,))
        node = np.take(self.nodes, np.where(self.nodes['name'] == node_name)[0][0])
        logger.debug("node\n%s" % (node,))
        part_nodes_coords = [ [node['lat'],node['lng']] for node in part_nodes if node['name']!=node_name]
        proximity_matrix = tools.get_proximity_matrix(part_nodes_coords,[[node['lat'],node['lng']]])
        _ ,part_nodes_min_idx = np.unravel_index(np.argmin(proximity_matrix), proximity_matrix.shape)
        nearest_node = np.take(part_nodes, part_nodes_min_idx)
        return nearest_node

    def swap_indices_in_threads(self,i,j):
        position_of_index_i = np.where( self.set == i )
        logger.debug("position_of_index_i\n%s" % (position_of_index_i,))
        position_of_index_j = np.where( self.set == j )
        logger.debug("position_of_index_j\n%s" % (position_of_index_j,))
        self.set[position_of_index_i] = j
        self.set[position_of_index_j] = i

    def update_stats(self):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        if self.stats == None and self.score != None: # and self.set != None:
            new_entry = [self.score, self.set]
            self.stats = [copy.deepcopy(new_entry)]
        else:
            new_entry = [self.score, self.set]
            self.stats.append(copy.deepcopy(new_entry))
        self.stats[-1].append(self.current_temp)

    def loop(self):
        self.new_set = self.set[:]

        longest_thread_number, bad_node = self.get_worst_thread_and_bad_node()
        logger.debug("bad_node\n%s" % (bad_node,))
        other_threads_idxs = self.set[:]
        other_threads_idxs = np.delete(other_threads_idxs, longest_thread_number,axis=0)
        logger.debug("other_threads_idxs\n%s" % (other_threads_idxs,))
        flattend_indices_to_choose_from = [idx for sublist in other_threads_idxs for idx in sublist]

        nearest = self.get_nearest_node(flattend_indices_to_choose_from,bad_node['name'])
        logger.debug("nearest\n%s" % (nearest,))
        idx_of_bad_node = np.where(self.nodes['name'] == bad_node['name'])[0][0]
        idx_of_nearest = np.where(self.nodes['name'] == nearest['name'])[0][0]
        logger.debug("idx_of_bad_node\n%s" % (idx_of_bad_node,))
        logger.debug("idx_of_nearest\n%s" % (idx_of_nearest,))
        logger.debug("before swap self.set\n%s" % (self.set,))
        
        self.swap_indices_in_threads(idx_of_bad_node,idx_of_nearest)
        logger.debug("after swap self.set\n%s" % (self.set,))

        self.calc_scores()
        logger.debug("self.score\n%s" % (self.score,))

        if self.choose():
            logger.debug("New set chosen over old one")
            self.set = self.new_set[:]
            new_set_chosen = True
        else:
            logger.debug("Old set remains current one")
            new_set_chosen = False
        logger.debug("new_set_chosen\n%s" % (new_set_chosen,))

        self.update_stats()
        return new_set_chosen

def init_thread_optimizer(n_cities=100):
    t = ThreadOptimizer()
    nodes_data = tools.get_nodes_data(nodes_num = n_cities, recreate_nodes_data=False)
    t.nodes = nodes_data
    tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
    ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}
    t.start = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = t.node_dtype)
    t.finish = np.array(('Ryazan',ryazan_coords['lat'],ryazan_coords['lng']),dtype = t.node_dtype)

    logging.disable(logging.DEBUG)
    t.set = [range(t.nodes.shape[0])]
    logging.disable(logging.NOTSET)
    logger.debug("t.set\n%s" % (t.set,))

    max_loops = 100
    # max_temp = max_loops/1e1
    max_temp = 50
    stop_temperature = 0.1
    alpha = (1 - 1./max_loops)
    logger.debug("alpha\n%s" % (alpha,))
    # alpha = 1-(1/max_temp)/2.
    t.SWAP_NEAREST = False
    t.SWAP_ORDER = True
    t.SWAP_ONLY_NEIGHBOUR = False

    # инициализация генератора температур в оптимизаторе
    t.init_linear_cooling_schedule(max_temp,max_loops,stop_temp = stop_temperature)
    return t

def main():
    t = init_thread_optimizer()
    t.n_threads = 5
    logging.disable(logging.DEBUG)
    t.create_threads()
    t.calc_scores()
    logging.disable(logging.NOTSET)
    logger.debug("t.score\n%s" % (t.score,))
    logger.debug("t.threads_scores\n%s" % (t.threads_scores,))
    t.update_stats()


    logging.disable(logging.DEBUG)
    for i in range(10):
        new_set_chosen = t.loop()
        logger.debug("new_set_chosen\n%s" % (new_set_chosen,))
        logger.debug("t.current_temp\n%s" % (t.current_temp,))
        propability = t.get_transition_probability()
        logger.debug("propability\n%.3f" % (propability,))
    logging.disable(logging.NOTSET)
    logger.debug("t.stats[-1]\n%s" % (t.stats[-1],))


if __name__ == "__main__":
    tools.setup_logging()
    logger.info("thread optimizer script run directly")
    main()
    logger.info("thread optimizer script finished running")