# -*- coding: utf-8 -*-
import time, math, random, sys, copy
import numpy as np
import bokeh.plotting as bp
from bokeh.models import LinearAxis, Range1d

def plot_route(seq,cities,text):
    x = cities[seq]['lat']
    y = cities[seq]['lng']
    # print(x)
    # print(y)
    out_fname = "habr_%s.html" % (text)
    bp.output_file(out_fname)
    p = bp.figure(plot_width=640, plot_height=480,title=u'')
    # np_stats = np.array(self.stats,dtype = object)
    p.x_range = Range1d(0, 10)
    p.y_range = Range1d(0, 10)
    p.line(
           x,
           y,
           line_width=2,
           color='blue',
           alpha=0.5,
           )
    bp.save(p)