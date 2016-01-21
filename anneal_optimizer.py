# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, sys
import numpy as np
import abstract_optimizer
import haversine
# haversine((45.7597, 4.8422),(48.8567, 2.3508),miles = True)243.71209416020253
logger = logging.getLogger(__name__)

class AnnealOptimizer(abstract_optimizer.AbstractOptimizer):
    """AnnealOptimizer class provides 
    anneal optimizer
    based on AbstractOptimizer."""
    def __init__(self, start = None, finish = None, **kwarg):
        super(AnnealOptimizer, self).__init__()
        self.start = start
        self.finish = finish
        self.cooling_schedule = None
        self.current_temp = None
        self.SWAP_NEAREST = False

    def init_cooling_schedule(self,start_temp,alpha):
        def kirkpatrick_cooling(start_temp,alpha):
            T=start_temp
            while True:
                yield T
                T=alpha*T
        self.cooling_schedule = kirkpatrick_cooling(start_temp,alpha)

    def get_score(self,a_set):
        super(AnnealOptimizer, self).get_score()
        def root_len(start,finish,nodes_in_order):
            route_len = 0.
            all_points = list(nodes_in_order)
            all_points.append(finish.tolist())
            all_points.insert(0, start.tolist())
            for (c1,c2) in tools.pairwise(all_points):
                route_len += haversine.haversine((c1[1],c1[2]),(c2[1],c2[2]),miles=False)
            return route_len
        return root_len(self.start,self.finish,self.nodes[a_set])

    def get_sub_node(self,excluded_indeces=[]):
        if self.SWAP_NEAREST and excluded_indeces!=[]:
            bad_node_idx = excluded_indeces[0]
            logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
            list_to_choose_from = [node_idx for node_idx in self.set if node_idx not in excluded_indeces]
            array_of_radius = np.zeros(len(list_to_choose_from),np.float)
            lat = self.nodes[bad_node_idx]['lat']
            lng = self.nodes[bad_node_idx]['lng']
            for i,node_idx in enumerate(list_to_choose_from):
                array_of_radius[i] = haversine.haversine((lat,lng),(self.nodes[node_idx]['lat'],self.nodes[node_idx]['lng']),miles=False)
            sorted_array_of_radius = np.sort(array_of_radius)[::-1]
            propability = [0]*len(list_to_choose_from)
            propability[0] = 1.
            chosen_node = np.random.choice(sorted_array_of_radius, 1, p=propability)
            logger.debug("sorted_array_of_radius\n%s" % (sorted_array_of_radius,))
            # chosen_node = np.random.choice(sorted_array_of_radius, 1, p=[1./len(nodes_to_select_from)]*len(nodes_to_select_from))
            list_to_choose_from_idx = np.argmax(array_of_radius==chosen_node)
            sub_idx = list_to_choose_from[list_to_choose_from_idx]
            return sub_idx
        elif SWAP_NEAREST:
            logger.error("get_sub_node misused: excluded_indeces == []")
        return super(AnnealOptimizer, self).get_sub_node(excluded_indeces)

    def choose(self):
        super(AnnealOptimizer, self).choose()
        self.current_temp = next(self.cooling_schedule)
        if self.new_score < self.score:
            return 1.0
            # return True
        else:
            logger.debug("self.current_temp\n%s" % (self.current_temp,))
            return math.exp( -abs(self.new_score-self.score)/self.current_temp )
            # return False

    def update_stats(self):
        super(AnnealOptimizer, self).update_stats()
        self.stats[-1].append(self.current_temp)

    def plot_route_from_stats(self, stat_idx = -1):
        stat = self.stats[stat_idx]
        a_set = stat[1]
        a_score = stat[0]
        plot_fname =  ('%s_%d_nodes_%.1f_km.html') % (str(self.__class__.__name__),len(self.nodes),a_score)
        moscow = locm.Location(address='Moscow')
        fig_on_gmap = bokehm.Figure(output_fname=plot_fname,use_gmap=True, center_coords=moscow.coords)
        locs_coords_dict_list = [{'lat':node_data[1],'lng':node_data[2]} for node_data in self.nodes[a_set]]
        locs_coords_dict_list.append({'lat':self.finish['lat'],'lng':self.finish['lng']})
        locs_coords_dict_list.insert(0, {'lat':self.start['lat'],'lng':self.start['lng']})
        fig_on_gmap.add_line(locs_coords_dict_list,circle_size=5, circles_color='red',alpha=1.)
        fig_on_gmap.save2html()

    def plot_stats(self,**kwargs):
        import bokeh.plotting as bp
        out_fname = self.__class__.__name__+"_stats.html"
        bp.output_file(out_fname)
        p = bp.figure(plot_width=640, plot_height=480,title=kwargs.get('title',u''))
        np_stats = np.array(self.stats,dtype = object)
        p.line(
               np.arange(0,len(self.stats)),
               [entry[0] for entry in self.stats],
               line_width=kwargs.get('size',2),
               color=kwargs.get('color','red'),
               alpha=kwargs.get('alpha',0.5),
               )
        p.line(
               np.arange(0,len(self.stats)),
               [entry[-1] for entry in self.stats],
               line_width=kwargs.get('size',5),
               color=kwargs.get('color','blue'),
               alpha=kwargs.get('alpha',0.3),
               )
        if kwargs.get('save',True):
            bp.save(p)
        if kwargs.get('show',False):
            bp.show(p)

def anneal_optimizer_test():
    logger.debug('anneal optimizer started')
    a = AnnealOptimizer()

    node_dtype = np.dtype([('name',np.str_, 32),  ('lat', np.float64, 1),  ('lng', np.float64, 1)])
    tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
    ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}
    a.start = np.array(('Tver',tver_coords['lat'],tver_coords['lng']),dtype = node_dtype)
    a.finish = np.array(('Ryazan',ryazan_coords['lat'],ryazan_coords['lng']),dtype = node_dtype)

    nodes_data = tools.get_nodes_data(recreate_nodes_data=False)
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

def main():
    pass

if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("optimizer script run directly")
    anneal_optimizer_test()
    logger.info("optimizer script finished running")