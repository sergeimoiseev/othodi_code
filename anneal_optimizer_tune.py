# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, sys, copy
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

def anneal_optimizer_setup(n_cities):
    logger.debug('anneal optimizer setup started')
    a = anneal_optimizer.AnnealOptimizer()

    node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
    ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}
    a.start = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    a.finish = np.array(('Ryazan',ryazan_coords['lat'],ryazan_coords['lng']),dtype = node_dtype)

    nodes_data = tools.get_nodes_data(nodes_num = n_cities, recreate_nodes_data=False)
    logger.debug("nodes_data\n%s" % (nodes_data))
    # инициализация узлов
    a.nodes = nodes_data
    a.stats = None
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
    # logger.debug("np_stats_sorted\n%s" % (np_stats_sorted,))
    a.stats
    a.plot_route_from_stats()
    return np_stats_sorted[-1]

def anneal_optimizer_tune():
    best_results_list = []
    max_loops = 1e1
    max_temp = max_loops/1e1
    alpha = 1-(1/max_temp)/2.

    start_nodes_num = 5
    for n in range(start_nodes_num,21,1):
        list4fixed_nodes_num = []
        for i in range(3):
            a = anneal_optimizer_setup()
            list4fixed_nodes_num.append((anneal_optimizer_run(a,
                                                        max_loops = max_loops,
                                                        max_temp = max_temp,
                                                        alpha = alpha,
                                                            )))
        score_list = [res['score'] for res in list4fixed_nodes_num]
        route_list = [res['set'] for res in list4fixed_nodes_num]
        temp_list = [res['temp'] for res in list4fixed_nodes_num]
        
        best_results_list.append([np.mean(score_list),route_list[-1],np.mean(temp_list)])
            # a = None

    logger.debug("best_results_list\n%s" % (best_results_list,))
    score_list = [res[0] for res in best_results_list]
    route_list = [res[1] for res in best_results_list]
    temp_list = [res[2] for res in best_results_list]
    experiment_number = np.arange(start_nodes_num,len(best_results_list),1)
    logger.debug("experiment_number\n%s" % (experiment_number,))
    plot_tune(experiment_number,temp_list,y2=score_list)


def test_score():
    for i in range(1):
        n_cities = 20
        a = anneal_optimizer_setup(n_cities)
        # инициализация начального маршрута
        a.set = list(np.arange(a.nodes.shape[0]))
        a.SORT_ON = False
        a.set = a.sort(a.set)
        # logger.info("a\n%s" % (a,))
        a.new_set = copy.deepcopy(a.set)  # глубокая
        # a.new_set = a.set[:]  # быстрая копия (не глубокая)
        # logger.info("a\n%s" % (a,))

        # инициализация констант
        max_loops = 1000
        # max_temp = max_loops/1e1
        max_temp = 50
        stop_temperature = 0.1
        alpha = (1 - 1./max_loops)
        logger.debug("alpha\n%s" % (alpha,))
        # alpha = 1-(1/max_temp)/2.
        a.SWAP_NEAREST = False
        a.SWAP_ORDER = True
        a.SWAP_ONLY_NEIGHBOUR = False

        # инициализация генератора температур в оптимизаторе
        a.init_linear_cooling_schedule(max_temp,max_loops,stop_temp = stop_temperature)
        # a.init_kirkpatrick_cooling_schedule(max_temp,alpha,stop_temp = stop_temperature)

        t, float_value, bool_val, score_list = [], [], [], []
        # a.update_stats()
        # logger.debug("before run\n%s" % a)
        logging.disable(logging.DEBUG)
        for j in range(max_loops):
            new_set_chosen = a.loop()
            # logger.info("a.current_temp\n%s" % (a.current_temp,))
            t.append(a.current_temp)
            # a.new_score = 1000.
            # math.exp(1. -abs(self.new_score)/float(self.current_temp ))
            fl = math.exp(1. - abs(a.new_score)/float(a.current_temp))
            float_value.append(fl)
            bool_val.append(new_set_chosen)
            score_list.append(a.score)
            if j%1000==0:
                logger.info("%d of %d" % (j,max_loops))

        logging.disable(logging.NOTSET)
        # printing
        for i in range(0,max_loops,10):
            logger.debug("i t - f - b   %d %.02f - %.02f - %s - %.3f" % (i*10,t[i],float_value[i],bool_val[i],score_list[i]))    
        # logger.debug("float_value\n%s" % (float_value,))


        a.plot_stats()
        a.plot_route_from_stats()
        # logger.debug("after run\n%s" % (a,))
        stats_dtype = np.dtype([('score',np.float64, 1),  ('set', np.float64, len(a.nodes)), ('temp',np.float64, 1)])
        stats_tuples = [tuple(st) for st in a.stats]
        np_stats = np.array(stats_tuples,dtype=stats_dtype)
        np_stats_sorted = np.sort(np_stats,order=('score',))[::-1]
        logger.info("np_stats[0]\n%s" % (np_stats[0],))
        # for entry in np_stats_sorted:
        #     logger.debug("np_stats_sorted entry[0]\n%s" % (tools.print_vars_values_types(entry[0]),))
        a=None

def seed_cooling():
    a = anneal_optimizer_setup()
    # инициализация констант
    max_loops = 1000
    # max_temp = max_loops/1e1
    max_temp = 2000
    # alpha = (1 - 1./max_loops)
    # logger.debug("alpha\n%s" % (alpha,max_loops))
    a.init_linear_cooling_schedule(max_temp,max_loops)
    # a.init_kirkpatrick_cooling_schedule(max_temp,alpha)
    t = []
    float_value = []
    bool_val = []
    for i in range(max_loops):
        a.current_temp = next(a.cooling_schedule)
        t.append(a.current_temp)
        a.new_score = 1000.
        # math.exp(1. -abs(self.new_score)/float(self.current_temp ))
        fl = math.exp(1. - abs(a.new_score)/float(a.current_temp))
        float_value.append(fl)
        bool_val.append(True if fl>=1 else False)
    # printing
    for i in range(0,max_loops,10):
        logger.debug("i t - f - b   %d %.02f - %.02f - %s" % (i*10,t[i],float_value[i],bool_val[i]))    
        # logger.debug("float_value\n%s" % (float_value,))

def test_sort():
    
    a = anneal_optimizer_setup()
    a.SORT_ON = True
    logger.debug("a.set\n%s" % (a.set,))
    a.set = list(np.arange(a.nodes.shape[0]))
    logger.debug("a.set\n%s" % (a.set,))


def split_in_parts():
    pass

if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("optimizer script run directly")
    # anneal_optimizer_tune()
    # seed_cooling()
    # test_sort()
    test_score()

    logger.info("optimizer script finished running")
