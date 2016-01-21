# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, sys
import numpy as np
import bokeh.plotting as bp
from bokeh.models import LinearAxis, Range1d
import anneal_optimizer

def plot_tune(x,y,y2=False,**kwargs):
    out_fname = "tune.html"
    bp.output_file(out_fname)
    p = bp.figure(plot_width=640, plot_height=480,title=kwargs.get('title',u''))
    # np_stats = np.array(self.stats,dtype = object)
    p.y_range = Range1d(0, 10)
    p.line(
           x,
           y,
           line_width=kwargs.get('size',2),
           color=kwargs.get('color','blue'),
           alpha=kwargs.get('alpha',0.5),
           )
    if not kwargs.get('y2',False):
        p.extra_y_ranges = {"foo": Range1d(start=0, end=550)}
        p.add_layout(LinearAxis(y_range_name="foo"), 'right')
        p.line(
               x,
               y2,
               line_width=kwargs.get('size',2),
               color=kwargs.get('color','red'),
               alpha=kwargs.get('alpha',0.5),
               y_range_name="foo"
              )

    bp.save(p)    

def anneal_optimizer_setup():
    logger.debug('anneal optimizer setup started')
    a = anneal_optimizer.AnnealOptimizer()

    node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
    ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}
    a.start = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    a.finish = np.array(('Ryazan',ryazan_coords['lat'],ryazan_coords['lng']),dtype = node_dtype)

    nodes_data = tools.get_nodes_data(recreate_nodes_data=False)
    logger.debug("nodes_data\n%s" % (nodes_data))
    
    # инициализация констант

    # инициализация узлов
    a.nodes = nodes_data

    return a

def anneal_optimizer_run(a,
                        max_loops = 1e3,
                        max_temp = 1e1,
                        alpha = 1-0.001,
                         ):
    # инициализация начального маршрута
    a.set = list(np.arange(a.nodes.shape[0]))
    a.new_set = a.set[:]  # быстрая копия (не глубокая)
    a.update_stats()
    logger.debug(a)
    # инициализация генератора температур в оптимизаторе
    a.init_cooling_schedule(max_temp,alpha)

    count_loops = 0
    a.SWAP_NEAREST = True

    logging.disable(logging.DEBUG)
    # запуск цикла отжига
    while True:  #!!!
        a.loop()
        count_loops += 1
        logger.debug("step %d   %d" % (count_loops, a.stats[-1][0]))
        # if a.stats[-1][0]<=350:
        #     break
        if count_loops>max_loops:  # выполняется фиксированное время
            break

    logging.disable(logging.NOTSET)
    # logger.debug(a)
    # logger.debug(a.stats[-3:])
    # logger.debug("loops counted %d" % (count_loops))
    # a.plot_stats()
    # поиск лучшего решения за эксперимент
    stats_dtype = np.dtype([('score',np.float64, 1),  ('set', np.float64, len(a.nodes)), ('temp',np.float64, 1)])
    stats_tuples = [tuple(st) for st in a.stats]
    np_stats = np.array(stats_tuples,dtype=stats_dtype)
    
    # logger.debug("np_stats\n%s" % (np_stats,))
    np_stats_sorted = np.sort(np_stats,order=('score','temp'))[::-1]
    logger.debug("np_stats_sorted\n%s" % (np_stats_sorted,))
    # a.plot_route_from_stats()
    return np_stats_sorted[-1]

def anneal_optimizer_tune():
    best_results_list = []
    
    max_loops = 1e3
    max_temp = max_loops/1e1
    alpha = 1-(1/max_temp)/2.

    for i in range(100):
        a = anneal_optimizer_setup()
        best_results_list.append((anneal_optimizer_run(a,
                                                    max_loops = max_loops,
                                                    max_temp = max_temp,
                                                    alpha = alpha,
                                                        )))

    logger.debug("best_results_list\n%s" % (best_results_list,))
    score_list = [res['score'] for res in best_results_list]
    route_list = [res['set'] for res in best_results_list]
    temp_list = [res['temp'] for res in best_results_list]
    experiment_number = np.arange(0,len(best_results_list))
    logger.debug("experiment_number\n%s" % (experiment_number,))
    plot_tune(experiment_number,temp_list,y2=score_list)

def test_score():
    a = anneal_optimizer_setup()
    # инициализация начального маршрута
    a.set = list(np.arange(a.nodes.shape[0]))
    a.new_set = a.set[:]  # быстрая копия (не глубокая)
    a.update_stats()

    # инициализация констант
    max_loops = 1e3
    # max_temp = max_loops/1e1
    max_temp = 0.000001
    alpha = 1-(1/max_temp)/2.
    a.SWAP_NEAREST = True
    # инициализация генератора температур в оптимизаторе
    a.init_cooling_schedule(max_temp,alpha)
    
    for i in range(1):
        logger.debug("before run\n%s" % a)
        # logging.disable(logging.DEBUG)
        a.loop()
        # logging.disable(logging.NOTSET)
        logger.debug("after run\n%s" % (a,))
        stats_dtype = np.dtype([('score',np.float64, 1),  ('set', np.float64, len(a.nodes)), ('temp',np.float64, 1)])
        stats_tuples = [tuple(st) for st in a.stats]
        np_stats = np.array(stats_tuples,dtype=stats_dtype)
        np_stats_sorted = np.sort(np_stats,order=('score','temp'))[::-1]
        logger.info("np_stats_sorted\n%s" % (np_stats_sorted,))

    logger.debug("a.get_score(a_set)\n%s" % (a.get_score(a.set),))
    # a.get_score()

    # s1 = [1.0, 2.0, 0.0, 3.0, 4.0]
    # s2 = [0.0, 2.0, 1.0, 3.0, 4.0]
    # logger.debug("a.get_score(a_set)\n%s" % (a.get_score(s1),))
    # logger.debug("a.get_score(a_set)\n%s" % (a.get_score(s2),))


if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("optimizer script run directly")
    anneal_optimizer_tune()
    # test_score()
    logger.info("optimizer script finished running")
