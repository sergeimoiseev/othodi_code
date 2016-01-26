# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm
import logging.config, os, yaml, inspect
import time, math, random, sys, copy
import numpy as np
import abstract_optimizer, anneal_optimizer
import haversine
# haversine((45.7597, 4.8422),(48.8567, 2.3508),miles = True)243.71209416020253
logger = logging.getLogger(__name__)

class SplitterOptimizer(abstract_optimizer.AbstractOptimizer):
    """SplitterOptimizer class provides 
    splitter
    based on AbstractOptimizer."""

    def __init__(self, start = None, finish = None, **kwarg):
        super(SplitterOptimizer, self).__init__()
        self.start = start
        self.finish = finish
        self.center = None
        self.knot = None
        # self.node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])

    def get_score(self,a_set_):
        super(SplitterOptimizer, self).get_score()


    def sort(self,a_set_):
        super(SplitterOptimizer, self).sort(a_set_)

    def find_knot(self):
        node4sorting_dtype = [(name,self.node_dtype[name]) for name in self.node_dtype.names] + [('r_cm', np.float64, 1), ('r_s', np.float64, 1)]
        nodes4sort = np.zeros(self.nodes.shape[0],dtype = node4sorting_dtype)
        for node,n4s in zip(self.nodes,nodes4sort):
            n4s['name'] = node['name']
            n4s['lat'] = node['lat']
            n4s['lng'] = node['lng']
            n4s['r_cm'] = tools.r([self.center['lat'],self.center['lng']],[node['lat'],node['lng']])
            n4s['r_s'] = 0.
        nodes4sort = np.sort(nodes4sort,order=('r_cm'))
        self.knot = self.nodes[self.nodes['name']==nodes4sort[0]['name']][0]

    def split_nodes(self):
        # поиск центра масс точек
        n = self.nodes.shape[0]
        self.center = np.array( ('center', np.sum(self.nodes['lat'])/n, np.sum(self.nodes['lng'])/n), dtype = self.node_dtype)
        logger.debug("s.center\n%s" % (self.center,))
        self.find_knot()
        logger.debug("nearest_node_to_center\n%s" % (self.knot,))
        xc = tools.lng_to_km(self.knot)
        yc = tools.lat_to_km(self.knot)

        xs = tools.lng_to_km(self.start)
        ys = tools.lat_to_km(self.start)
        xf = tools.lng_to_km(self.finish)
        yf = tools.lat_to_km(self.finish)
        if xs!=xf and ys!=yf:
            A = xf-xs
            B = yf-ys
            C = -A*xc - B*yc
            # # line: A*x + B*y + C = 0    -- прямая-нормаль к start--finish, проходящая через узел, ближайший к  центру масс точке
            def part_by_sign(x,y):
                return A*x + B*y + C
        else:
            # line: (x-xs)/(xc-xs) - (y-ys)/(yc-ys)   -- прямая start--центр_масс   для случай, когда начало и конец маршрута в одной точке
            def part_by_sign(x,y):
                return (x-xs)/(xc-xs) - (y-ys)/(yc-ys)
        # разбиение на две группы по принадлежности к полуплоскостям
        part_left = []
        part_right = []
        for node in self.nodes:
            x,y = tools.lng_to_km(node['lng']), tools.lat_to_km(node['lat'])
            in_part_of_surface = part_by_sign(x,y)
            if in_part_of_surface<0:
                logger.debug("node to the left:\n%s" % (node['name'],))
                part_left.append(node)
            if in_part_of_surface>0:
                logger.debug("node to the right:\n%s" % (node['name'],))
                part_right.append(node)
        part_right_np_nodes = np.array(part_right,dtype = self.node_dtype)
        part_left_np_nodes = np.array(part_left,dtype = self.node_dtype)
        return part_right_np_nodes, part_left_np_nodes, self.knot


    def recursive_split(self,parts,nodes,fins,Lmax):
        if all([len(part)<=Lmax for part in parts]):
            return parts, fins
        for part in parts:
            if len(part)<=Lmax:
                continue
            else:
                i = parts.index(part)

                logger.debug("part\n%s" % (part,))
                logger.debug("i\n%s" % (i,))
                logger.debug("self.nodes before extracting\n%s" % (self.nodes,))
                self.nodes = nodes[part]
                logger.debug("self.nodes after extracting\n%s" % (self.nodes,))
                logging.disable(logging.DEBUG)
                rp,lp,new_finish = self.split_nodes()
    
                logger.debug("len(self.nodes)\n%s" % (len(self.nodes),))
                rp_idxs = tools.find_indeces_of_subarray(nodes.tolist(),rp.tolist())
                lp_idxs = tools.find_indeces_of_subarray(nodes.tolist(),lp.tolist())
                self.finish = new_finish

                parts[i:i+1] = rp_idxs,lp_idxs
                fins[i] = tools.find_indeces_of_subarray(nodes.tolist(),[new_finish])[0]
                fins[i+1] = tools.find_indeces_of_subarray(nodes.tolist(),[new_finish])[0]
                return self.recursive_split(parts,nodes,fins,Lmax)


    def split_anneal_a_route(self,max_nodes_in_part,max_anneal_loops=100,additional_full_anneal = False):
        s = self
        list_of_lists_of_indeces = [range(len(s.nodes))]
        all_nodes_list = copy.deepcopy(s.nodes)
        knots_indices = [None]*len(s.nodes)
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

        def anneal_a_sequence(part_idxs,finish,plot_stats=False):
            if len(part_idxs)<=1:
                return part_idxs
            a = anneal_optimizer.AnnealOptimizer()
            a.nodes = all_nodes_list[part_idxs]
            a.start = tver_np_arr
            a.finish = finish
            logger.debug("a.start\n%s" % (a.start,))
            logger.debug("a.finish\n%s" % (a.finish,))

            a.set = list(np.arange(a.nodes.shape[0]))
            a.SORT_ON = True
            a.set = a.sort(a.set)
            a.new_set = copy.deepcopy(a.set)  # глубокая
            # инициализация констант
            max_loops = max_anneal_loops
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
            annealed_nodes_sequence = tools.find_indeces_of_subarray(all_nodes_list,a.nodes[a.set])
            # annealed_nodes = all_nodes_list[annealed_nodes_sequence]   
            if plot_stats==True:
                a.plot_stats(fname=str(annealed_nodes_sequence))
            return annealed_nodes_sequence

        for part_idxs,finish_idx in zip(list_of_lists_of_indeces,knots_indices):
            if finish_idx!=None:
                finish_node = all_nodes_list[finish_idx]
            else:
                finish_node = s.finish
            annealed_nodes_sequence = anneal_a_sequence(part_idxs,finish_node,plot_stats = True)
            annealed_index_sets.append(annealed_nodes_sequence)

        logging.disable(logging.NOTSET)
        logger.debug("annealed_index_sets\n%s" % (annealed_index_sets,))

        full_route_indices = []
        for part,fin in zip(annealed_index_sets,knots_indices):
            full_route_indices += part
            if fin!=None:
                full_route_indices.append(fin)
        logger.debug("full_route_indices\n%s" % (full_route_indices,))

        if additional_full_anneal:
            logging.disable(logging.DEBUG)
            final_full_route_indices = anneal_a_sequence(full_route_indices,ryazan_np_arr,plot_stats=True)
            logging.disable(logging.NOTSET)
        else:
            final_full_route_indices = full_route_indices
        
        # рисование групп узлов и промежуточных финишей
        # moscow = locm.Location(address='Moscow')
        # plot = bokehm.Figure(output_fname='annealed_splitter.html',center_coords=moscow.coords,use_gmap=True,)
        # plot.add_line(all_nodes_list, circle_size=10,circles_color='blue',alpha= 0.1,no_line = True)
        # colors_list = ['red','green','blue','orange','yellow']*(len(annealed_index_sets)//5+1)
        # for i,part in enumerate(annealed_index_sets):
        #     logger.debug("len(part)\n%s" % (len(part),))
        #     logger.debug("part\n%s" % (part,))
        #     plot.add_line(all_nodes_list[part], circle_size=5,circles_color=colors_list[i],alpha= 0.5,no_line = False)
        #     if knots_indices[i]!=None:
        #         plot.add_line([s.start,all_nodes_list[knots_indices[i]]], circle_size=10,circles_color='red',alpha= 1.,no_line = False)
        # plot.save2html()

        # moscow = locm.Location(address='Moscow')
        # plot = bokehm.Figure(output_fname='a_route_annealed_splitted.html',center_coords=moscow.coords,use_gmap=True,)
        # step_grid = np.arange(len(full_route_indices))
        # plot.add_line( all_nodes_list[full_route_indices], circle_size=step_grid,circles_color='red',alpha= 0.5,no_line = False)
        # plot.save2html()

        return final_full_route_indices

def init_split_optimizer(nodes_data):
    # создание сплиттера-оптимизатора
    s = SplitterOptimizer()
    node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    # node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
    ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}
    s.start = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    s.finish = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    # s.finish = np.array(('Ryazan',ryazan_coords['lat'],ryazan_coords['lng']),dtype = node_dtype)

    # инициализация узлов
    logger.debug("nodes_data\n%s" % (nodes_data))
    s.nodes = nodes_data
    return s

def splitter_optimizer_test():
    logger.debug('splitter optimizer  started')
    
    # создание оптимизатора
    s = SplitterOptimizer()
    node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    # node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
    ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}
    s.start = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    # s.finish = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    s.finish = np.array(('Ryazan',ryazan_coords['lat'],ryazan_coords['lng']),dtype = node_dtype)
    # инициализация узлов
    n_cities = 20
    nodes_data = tools.get_nodes_data(nodes_num = n_cities, recreate_nodes_data=False)
    logger.debug("nodes_data\n%s" % (nodes_data))
    s.nodes = nodes_data

    # parts = [s.nodes]

    list_of_lists_of_indeces = [range(len(nodes_data))]
    all_nodes_list = nodes_data#.tolist()
    max_nodes_in_part = 5
    knots = [None]*len(nodes_data)
    list_of_lists_of_indeces, knots = s.recursive_split(list_of_lists_of_indeces,all_nodes_list,knots,Lmax=max_nodes_in_part)
    logger.debug("knots\n%s" % (knots,))

    # рисование групп узлов и промежуточных финишей
    moscow = locm.Location(address='Moscow')
    plot = bokehm.Figure(output_fname='splitter.html',center_coords=moscow.coords,use_gmap=True,)
    plot.add_line(s.nodes, circle_size=10,circles_color='blue',alpha= 0.1,no_line = True)
    colors_list = ['pink','magenta','blue','orange','yellow']*(len(list_of_lists_of_indeces)//5+1)
    for i,part in enumerate(list_of_lists_of_indeces):
        logger.debug("len(part)\n%s" % (len(part),))
        logger.debug("part\n%s" % (part,))
        plot.add_line(nodes_data[part], circle_size=5,circles_color=colors_list[i],alpha= 0.5,no_line = True)
        if knots[i]!=None:
            plot.add_line([s.start,nodes_data[knots[i]]], circle_size=10,circles_color='red',alpha= 1.,no_line = False)

    plot.save2html()
    logger.debug('splitter optimizer  finished')
    return s

def main():
    pass

if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("splitter optimizer script run directly")
    splitter_optimizer_test()
    logger.info("splitter optimizer script finished running")