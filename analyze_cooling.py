# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, random, sys
import bokeh.plotting as bp
from bokeh.models import LinearAxis, Range1d
import numpy as np
# import abstract_optimizer
import haversine
import anneal_optimizer
logger = logging.getLogger(__name__)

def plot_cooling_schedule():

    steps = np.arange(0,100)
    logger.debug("steps\n%s" % (steps,))

    a = anneal_optimizer.AnnealOptimizer()

    max_temp = 100
    alpha = 0.99
    a.init_cooling_schedule(max_temp,alpha)

    temp = []
    for step in steps:
        temp.append(next(a.cooling_schedule))
    temp = np.array(temp,dtype = np.float64)
    logger.debug("temp\n%s" % (temp,))

    temp_by_formula = []
    def t_formula(x, t_max,alpha_):
        return t_max*(1-(1-alpha_)*x)
    for step in steps:
        temp_by_formula.append(t_formula(step,max_temp,alpha))
    temp_by_formula = np.array(temp_by_formula,dtype = np.float64)
    logger.debug("temp_by_formula\n%s" % (temp_by_formula,))

    max_steps = 100
    a.init_linear_cooling_schedule(max_temp,max_steps)
    temp_linear_cooling = []
    for step in steps:
        temp_linear_cooling.append(t_formula(step,max_temp,alpha))
    temp_linear_cooling = np.array(temp_linear_cooling,dtype = np.float64)


    out_fname = "cooling.html"
    bp.output_file(out_fname)
    p = bp.figure(plot_width=640, plot_height=480,title=u'')
    # np_stats = np.array(self.stats,dtype = object)
    p.y_range = Range1d(0, max_temp)
    p.line(
           steps,
           temp,
           line_width=2,
           color='blue',
           alpha=0.5,
           )
    p.line(
           steps,
           temp_by_formula,
           line_width=2,
           color='green',
           alpha=1.,
           )
    p.line(
           steps,
           temp_linear_cooling,
           line_width=15,
           color='black',
           alpha=0.3,
           )
    bp.save(p)  

def test_boolean_chooser():
    a = anneal_optimizer.AnnealOptimizer()

    max_temp = 1000
    logger.debug("max_temp\n%s" % (max_temp,))
    max_steps = 100
    a.init_linear_cooling_schedule(max_temp,max_steps)
    a.current_temp = next(a.cooling_schedule)
    logger.debug("T = a.current_temp\n%s" % (a.current_temp,))
    a.score = 1001
    a.new_score = 1
    deltaE = a.new_score - a.score
    logger.debug("deltaE\n%s" % (deltaE,))
    exp = math.exp(1-abs(deltaE)/max_temp)
    logger.debug("exp\n%s" % (exp,))
    bool_res = a.bool_current_energy_opened()
    logger.debug("bool_res\n%s" % (bool_res,))
   
if __name__ == '__main__':
    tools.setup_logging()
    main()