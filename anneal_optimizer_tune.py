# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, sys
import numpy as np
import anneal_optimizer

def anneal_optimizer_test():
    logger.debug('anneal optimizer started')
    a = anneal_optimizer.AnnealOptimizer()

    node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
    ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}
    a.start = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    a.finish = np.array(('Ryazan',ryazan_coords['lat'],ryazan_coords['lng']),dtype = node_dtype)

    nodes_data = get_nodes_data(recreate_nodes_data=False)
    logger.debug("nodes_data\n%s" % (nodes_data))
    
    a.nodes = nodes_data
    # инициализация узлов и последовательностей
    a.set = list(np.arange(a.nodes.shape[0]))
    a.new_set = a.set[:]  # быстрая копия (не глубокая)
    a.update_stats()
    logger.debug(a)
    # оценка качества
    logger.debug("initial a.score=%s" % a.score)
    logger.debug("initial a.new_score=%s" % a.new_score)
    logger.debug(a.new_score)

    max_loops = 1e3
    max_temp = max_loops/1e1
    alpha = 1-(1/max_temp)/2
    a.init_cooling_schedule(max_temp,alpha)
    count_loops = 0

    a.SWAP_NEAREST = True
    
    # b_n = a.get_bad_node()
    # logger.debug("b_n\n%s" % (b_n,))
    # logger.debug("a.nodes[b_n]['name']\n%s" % (a.nodes[b_n]['name'],))

    # s_n = a.get_sub_node(excluded_indeces = [b_n])
    # logger.debug("s_n\n%s" % (s_n,))
    # logger.debug("a.nodes[s_n]['name']\n%s" % (a.nodes[s_n]['name'],))

    logging.disable(logging.DEBUG)
    while True:  #!!!
        a.loop()
        count_loops += 1
        logger.debug("step %d   %d" % (count_loops, a.stats[-1][0]))
        # if a.stats[-1][0]<=350:
        #     break
        if count_loops>max_loops:
            break
    logging.disable(logging.NOTSET)
    logger.debug(a)
    logger.debug(a.stats[-3:])
    logger.debug("loops counted %d" % (count_loops))
    a.plot_stats()
    # поиск лучшего решения за эксперимент
    # stats_dtype = np.dtype([('score',np.float64, 1),  ('set', np.float64, 5)])
    stats_dtype = np.dtype([('score',np.float64, 1),  ('set', np.float64, len(a.nodes)), ('temp',np.float64, 1)])
    stats_tuples = [tuple(st) for st in a.stats]
    # np_stats = np.array((1.,[0,1,2,3,4]),dtype=stats_dtype)
    np_stats = np.array(stats_tuples,dtype=stats_dtype)
    
    logger.debug("np_stats\n%s" % (np_stats,))
    np_stats_sorted = np.sort(np_stats,order=('score','temp'))[::-1]
    logger.debug("np_stats_sorted\n%s" % (np_stats_sorted,))
    a.plot_route_from_stats()
    logger.debug('anneal optimizer finished')

if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("optimizer script run directly")
    anneal_optimizer_test()
    logger.info("optimizer script finished running")
