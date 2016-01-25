# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, sys, copy
import numpy as np
import anneal_optimizer, splitter_optimizer
import haversine
# haversine((45.7597, 4.8422),(48.8567, 2.3508),miles = True)243.71209416020253
logger = logging.getLogger(__name__)

def split_anneal_a_route(nodes_data):
    
    # создание сплиттера-оптимизатора
    s = splitter_optimizer.SplitterOptimizer()
    node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    # node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
    ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}
    s.start = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    ### BUG STARTING HERE!!!  
    # Вариант 1.
    # когда делаешь старт совпадающий с финишом, последняя часть
    # полученная при разбиении недосчитывается со странной (казалось бы невозможной) ошибкой - 
    # в списке узлов больше на 1, чем на самом деле - к этому несуществующему узлу невозможно посчитать расстояние.
    # Ошибка всегда возникает только при расчетах, связанных с последней частью маршртуа.
    # Вариант 2
    # Та же ошибка возникает и при задании максимального числа узлов в одной части большего или
    # равного количеству городов - 
    # то есть, когда разбиения не происходит совсем, алгоритм до конца не доходит.
    # Строка вызывающая первый вариант ошибки
    s.finish = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    # s.finish = np.array(('Ryazan',ryazan_coords['lat'],ryazan_coords['lng']),dtype = node_dtype)
    # инициализация узлов

    logger.debug("nodes_data\n%s" % (nodes_data))
    s.nodes = nodes_data

    parts = [s.nodes]

    list_of_lists_of_indeces = [range(len(nodes_data))]
    all_nodes_list = nodes_data
    # Строка вызывающая второй вариант ошибки
    max_nodes_in_part = 30
    knots_indices = [None]*len(nodes_data)
    logging.disable(logging.DEBUG)
    list_of_lists_of_indeces, knots_indices = s.recursive_split(list_of_lists_of_indeces,all_nodes_list,knots_indices,Lmax=max_nodes_in_part)
    logging.disable(logging.NOTSET)
    logger.debug("knots_indices\n%s" % (knots_indices,))
    logger.debug("list_of_lists_of_indeces\n%s" % (list_of_lists_of_indeces,))

    # отжиг каждой части маршрута по отдельности
    tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
    ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}
    tver_np_arr = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = s.node_dtype)
    ryazan_np_arr = np.array(('Tver',ryazan_coords['lat'],ryazan_coords['lng']),dtype = s.node_dtype)
    # silent anneal
    annealed_index_sets = []
    logging.disable(logging.DEBUG)

    def anneal_a_sequence(part_idxs,finish):
        if len(part_idxs)<=1:
            return part_idxs
        a = anneal_optimizer.AnnealOptimizer()
        a.nodes = nodes_data[part_idxs]
        a.start = tver_np_arr
        a.finish = finish
        logger.debug("a.start\n%s" % (a.start,))
        logger.debug("a.finish\n%s" % (a.finish,))

        a.set = list(np.arange(a.nodes.shape[0]))
        a.SORT_ON = True
        a.set = a.sort(a.set)
        a.new_set = copy.deepcopy(a.set)  # глубокая
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

        for i in range(0,max_loops,100):
            logger.debug("i t - f - b   %d %.02f - %.02f - %s - %.3f" % (i*10,t[i],float_value[i],bool_val[i],score_list[i]))
        annealed_nodes_sequence = tools.find_indeces_of_subarray(nodes_data,a.nodes[a.set])
        # annealed_nodes = nodes_data[annealed_nodes_sequence]   
        a.plot_stats(fname=str(annealed_nodes_sequence))
        return annealed_nodes_sequence

    for part_idxs,finish_idx in zip(list_of_lists_of_indeces,knots_indices):
        if finish_idx!=None:
            finish_node = nodes_data[finish_idx]
        else:
            finish_node = s.finish
        annealed_nodes_sequence = anneal_a_sequence(part_idxs,finish_node)
        annealed_index_sets.append(annealed_nodes_sequence)

    logging.disable(logging.NOTSET)
    logger.debug("annealed_index_sets\n%s" % (annealed_index_sets,))

    # рисование групп узлов и промежуточных финишей
    moscow = locm.Location(address='Moscow')
    plot = bokehm.Figure(output_fname='annealed_splitter.html',center_coords=moscow.coords,use_gmap=True,)
    plot.add_line(s.nodes, circle_size=10,circles_color='blue',alpha= 0.1,no_line = True)
    colors_list = ['red','green','blue','orange','yellow']*(len(annealed_index_sets)//5+1)
    for i,part in enumerate(annealed_index_sets):
        logger.debug("len(part)\n%s" % (len(part),))
        logger.debug("part\n%s" % (part,))
        plot.add_line(nodes_data[part], circle_size=5,circles_color=colors_list[i],alpha= 0.5,no_line = False)
        if knots_indices[i]!=None:
            plot.add_line([s.start,nodes_data[knots_indices[i]]], circle_size=10,circles_color='red',alpha= 1.,no_line = False)
    plot.save2html()

    full_route_indices = []
    for part,fin in zip(annealed_index_sets,knots_indices):
        full_route_indices += part
        if fin!=None:
            full_route_indices.append(fin)
    logger.debug("full_route_indices\n%s" % (full_route_indices,))
    
    moscow = locm.Location(address='Moscow')
    plot = bokehm.Figure(output_fname='a_route_annealed_splitted.html',center_coords=moscow.coords,use_gmap=True,)
    step_grid = np.arange(len(full_route_indices))
    plot.add_line( nodes_data[full_route_indices], circle_size=step_grid,circles_color='red',alpha= 0.5,no_line = False)
    plot.save2html()

    logging.disable(logging.DEBUG)
    full_route_indices = anneal_a_sequence(full_route_indices,ryazan_np_arr)
    logging.disable(logging.NOTSET)

    return full_route_indices

def main():
    logger.debug('main  started')
    n_cities = 20
    nodes_data = tools.get_nodes_data(nodes_num = n_cities, recreate_nodes_data=False)
    indices = split_anneal_a_route(nodes_data)

    moscow = locm.Location(address='Moscow')
    plot = bokehm.Figure(output_fname='a_route_annealed_splitted.html',center_coords=moscow.coords,use_gmap=True,)
    step_grid = np.arange(len(indices))
    plot.add_line(nodes_data[indices], circle_size=step_grid,circles_color='red',alpha= 0.5,no_line = False)
    plot.save2html()
    logger.debug('main  finished')

if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("optimize_one_route script run directly")
    main()
    logger.info("optimize_one_route script finished running")
