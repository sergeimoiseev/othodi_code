# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, sys, copy
import numpy as np
import anneal_optimizer, splitter_optimizer, thread_optimizer, optimize_one_route
import haversine
# haversine((45.7597, 4.8422),(48.8567, 2.3508),miles = True)243.71209416020253
logger = logging.getLogger(__name__)

def test_init_optimize_threads(n_cities = 100):
    nodes_data = tools.get_nodes_data(nodes_num = n_cities, recreate_nodes_data=False)
    return nodes_data

def optimize_threads(nodes_data):
    number_of_cities_from_file = 100
    max_threads_anneal_loops = 10
    # max_temp = max_loops/1e1
    max_threads_anneal_temp = 500
    stop_threads_anneal_temperature = 0.1

    t = thread_optimizer.init_thread_optimizer(n_cities=number_of_cities_from_file, 
                              max_loops = max_threads_anneal_loops,
                               max_temp = max_threads_anneal_temp,
                                stop_temp = stop_threads_anneal_temperature)
    t.n_threads = 5
    logging.disable(logging.DEBUG)
    t.create_threads()
    t.calc_scores()
    logging.disable(logging.NOTSET)
    logger.debug("t.score\n%s" % (t.score,))
    logger.debug("t.threads_scores\n%s" % (t.threads_scores,))
    t.update_stats()


    logging.disable(logging.DEBUG)
    for i in range(max_threads_anneal_loops):
        new_set_chosen = t.loop()
        logger.debug("new_set_chosen\n%s" % (new_set_chosen,))
        logger.debug("t.current_temp\n%s" % (t.current_temp,))
        propability = t.get_transition_probability()
        logger.debug("propability\n%.3f" % (propability,))
        if i%5==0:
            logger.info("threads anneal: %d from %d" % (i,max_threads_anneal_loops))
            logger.info("t.current_temp  %s" % (t.current_temp,))
            logger.info("t.score  %s" % (t.score,))

    logging.disable(logging.NOTSET)
    logger.debug("t.stats[-1]\n%s" % (t.stats[-1],))
    # t.plot_stats()

    # plot routes after thread anneal
    # for thread_number,thread_idxs in enumerate(t.set):
    #     # logger.debug("thread_idxs\n%s" % (thread_idxs,))
    #     a = anneal_optimizer.AnnealOptimizer()
    #     a.nodes = np.take(t.nodes,thread_idxs)
    #     a.start = t.start
    #     a.finish = t.finish
    #     a.set = list(np.arange(a.nodes.shape[0]))
    #     a.SORT_ON = True
    #     a.set = a.sort(a.set)
    #     # logger.debug("after sort a.nodes[a.set]['name']\n%s" % (a.nodes[a.set]['name'],))
    #     a.update_stats()
    #     a.plot_route_from_stats()
    return t.set

if __name__ == "__main__":
    tools.setup_logging()
    logger.info("thread optimizer script run directly")
    nodes_data = test_init_optimize_threads(n_cities = 100)
    threads_indices = optimize_threads(nodes_data)
    for thread_idxs in threads_indices:
        thread_nodes = np.take(nodes_data, thread_idxs)
        optimize_one_route.optimize_one_route(thread_nodes,max_split_part = 5)
    logger.debug("threads_indices\n%s" % (threads_indices,))
    logger.info("thread optimizer script finished running")