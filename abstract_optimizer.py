# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, copy
import numpy as np
logger = logging.getLogger(__name__)

class AbstractOptimizer(object):
    """AbstractOptimizer class provides 
    basic functions and stubs."""
    def __init__(self, **kwarg):
        self._nodes = None  # all graph nodes in ordered object
        self._set = None  # chosen stats of graph -- some ordered object of indeces
        self._new_set = None # storage for new (unchosen) stats of graph
        self.score = None
        self.new_score = None
        self.stats = None
        logger.debug(self.__class__.__name__+" object created")

    @property
    def nodes(self):
        return self._nodes
    
    @nodes.setter
    def nodes(self, a_nodes): 
        self._nodes = np.copy(a_nodes)

    @property
    def set(self):
        return self._set
    
    @set.setter
    def set(self, a_set): 
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        # logger.debug("inspect.stack()\n%s" % (inspect.stack(),))
        # self._set = a_set[:]
        self._set = copy.deepcopy(a_set)
        self.score = self.get_score(self._set)

    @property
    def new_set(self):
        return self._new_set
    
    @set.setter
    def new_set(self, a_set): 
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        # logger.debug("inspect.stack()\n%s" % (inspect.stack(),))
        # self._new_set = a_set[:]
        self._new_set = copy.deepcopy(a_set)
        self.new_score = self.get_score(self._new_set)
    
    def get_score(self):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        
    def choose(self):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))

    def get_bad_node(self,excluded_indeces=[]):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        list_to_choose_from = [node_idx for node_idx in self.set if node_idx not in excluded_indeces]
        return random.choice(list_to_choose_from)
    def get_sub_node(self,excluded_indeces=[]):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        list_to_choose_from = [node_idx for node_idx in self.set if node_idx not in excluded_indeces]
        logger.debug("all nodes \n%s" % (self.set,))
        logger.debug("list_to_choose_from\n%s" % (list_to_choose_from,))
        return random.choice(list_to_choose_from)
    def swap(self,a_set,i,j):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        a_set[i], a_set[j] = a_set[j], a_set[i]
        self.score = self.get_score(self._set)
        self.new_score = self.get_score(self._new_set)
        return a_set

    def update_stats(self):
        logger.debug(tools.get_string_caller_objclass_method(self,inspect.stack()))
        if self.stats == None and self.score != None and self._set != None:
            new_entry = [self.score, self._set]
            self.stats = [copy.deepcopy(new_entry)]
            # self.stats = [new_entry[:]]
        else:
            new_entry = [self.score, self._set]
            self.stats.append(copy.deepcopy(new_entry))
            # self.stats.append(new_entry[:])

    def __str__(self):
        return str(self.__class__) + " object has variables:\n" + tools.print_vars_values_types(self,with_id=True)

    def view_sets_scores(self):
        out_str = ''
        out_str += 'set: \n%s\nid=%s\n' % (self._set,hex(id(self._set)))
        out_str += 'score: \n%s\nid=%s\n' % (self.score,hex(id(self.score)))
        out_str += 'new_set: \n%s\nid=%s\n' % (self._new_set,hex(id(self._new_set)))
        out_str += 'new_score: \n%s\nid=%s\n' % (self.new_score,hex(id(self.new_score)))
        return out_str

    def loop(self):
        # logger.debug("1 view_sets_scores\n%s" % (self.view_sets_scores(),))
        # logger.debug("nodes in current order\n%s" % (self.nodes[self.set]))
        # выбор и смена мест узлов
        b_n = self.get_bad_node()
        s_n = self.get_sub_node(excluded_indeces = [b_n])
        logger.debug("nodes swap %d -> %d" % (b_n, s_n))
        # logger.debug("old self.new_score=%s\n%s" % (self.new_score,self.nodes[self.new_set]))
        self.new_set = self.swap(self.new_set,b_n,s_n)
        # logger.debug("2 view_sets_scores\n%s" % (self.view_sets_scores(),))
        # self.score = self.get_score(self._set)
        # self.new_score = self.get_score(self._new_set)
        # оценка качества
        # logger.debug("new self.new_score=%s\n%s" % (self.new_score,self.nodes[self.new_set]))

        # меняем состояние на новое, если качество повысилось
        if self.choose():
            logger.debug("New set chosen over old one")
            # self.set = copy.deepcopy(self.new_set)  # doesn't help
            self.set = self.new_set[:]
        else:
            logger.debug("Old set remains current one")
        # logger.debug("3 view_sets_scores\n%s" % (self.view_sets_scores(),))
        self.update_stats()
        # logger.debug("self.stats\n%s" % (self.stats,))
        # logger.debug("4 view_sets_scores\n%s" % (self.view_sets_scores(),))
        # logger.debug(self)
        # logger.debug(self.stats)

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
        if kwargs.get('save',True):
            bp.save(p)
        if kwargs.get('show',False):
            bp.show(p)


def main():
    pass

if __name__ == "__main__":
    logger.info("abstract optimizer is not intended to be run directly")