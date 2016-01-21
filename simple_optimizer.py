# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random
import numpy as np
import abstract_optimizer

class SimpleOptimizer(abstract_optimizer.AbstractOptimizer):
    """SimpleOptimizer class provides 
    example of a real optimizer
    based on AbstractOptimizer."""
    def __init__(self, **kwarg):
        super(SimpleOptimizer, self).__init__()

    def get_score(self,a_set):
        super(SimpleOptimizer, self).get_score()
        def get_max_derivative(the_set):
            temp_list = []
            for i,pair in enumerate(tools.pairwise(the_set)):
                d_val = self.nodes[pair[-1]] - self.nodes[pair[0]]
                d_i = 1.
                temp_list.append(d_val/d_i)
            return max(temp_list)
        return get_max_derivative(a_set)
        
    def choose(self):
        super(SimpleOptimizer, self).choose()
        if self.new_score > self.score:
            return True
        else:
            return False

def simple_optimizer_test():
    logger.debug('simple optimizer started')
    a = SimpleOptimizer()
    arr = np.arange(10,100,10)
    # np.random.shuffle(arr)
    a.nodes = arr
    # инициализация узлов и последовательностей`
    a.set = list(np.arange(a.nodes.shape[0]))
    a.new_set = a.set[:]  # быстрая копия (не глубокая)
    a.update_stats()
    logger.debug(a)
    # оценка качества
    logger.debug("initial a.score=%s" % a.score)
    logger.debug("initial a.new_score=%s" % a.new_score)
    logger.debug(a.new_score)

    count_loops = 0
    logging.disable(logging.DEBUG)
    while True:
        a.loop()
        count_loops += 1
        logger.info("step %d   %d" % (count_loops, a.stats[-1][0]))
        if a.stats[-1][0]>=80:
            break
    logging.disable(logging.NOTSET)
    logger.debug(a)
    logger.debug(a.stats[-3:])
    logger.debug("loops counted %d" % (count_loops))
    a.plot_stats()
    logger.debug('simple optimizer finished')


def main():
    pass

if __name__ == "__main__":
    tools.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("optimizer script run directly")
    simple_optimizer_test()
    logger.info("optimizer script finished running")