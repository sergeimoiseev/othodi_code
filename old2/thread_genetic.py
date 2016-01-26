# -*- coding: utf-8 -*-
import threadsm, single_route_anneal
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools, bokehm, tspm
import logging.config, os, yaml, inspect
import time, math, os
import numpy as np
import random


tver_coords = {u'lat':56.8583600,u'lng':35.9005700}
ryazan_coords = {u'lat':54.6269000,u'lng':39.6916000}

def test_on_grid():
    try:
        os.remove("app.log")
    except:
        logger.info("Error while removing logfile - mayby file not found.")
        pass
    GRID_LEN = 10
    STAT_LENGTH = 1000
    ANNEAL = True
    start_temp_list = [100.]*GRID_LEN
    # start_temp_list = [100.,70.,50.,25.,10.,5.,2.5,1.,0.5,0.1,0.01]
    alpha_list = [0.6,0.7,0.75,0.8,0.85,0.9,0.95,0.95,0.99,0.99,0.999]
    logger.error("start_temp_list \n%s"% (start_temp_list))
    logger.error("alpha_list \n%s"% (alpha_list))
    scores_dtype = np.dtype([('max_itter', np.int32, 1), ('algorythm',np.str_, 16), ('st_temp', np.float64, 1), ('fin_temp', np.float64, 1),('alpha', np.float64, 1),('score',np.float64,1)])
    scores_vs_settings = np.zeros(GRID_LEN+1,dtype = scores_dtype)
    for i in range(GRID_LEN):
        logger.error("thread genetic started itteration No %d"%i)
        START_TEMP,ALPHA = start_temp_list[i],alpha_list[i]
        score,fin_temp = threadsm.main(STAT_LENGTH,ANNEAL,START_TEMP,ALPHA)
        scores_vs_settings[i]['max_itter']=STAT_LENGTH
        if ANNEAL:
            scores_vs_settings[i]['algorythm']='ANNEAL'
            scores_vs_settings[i]['st_temp']=start_temp_list[i]
            scores_vs_settings[i]['fin_temp']=fin_temp
            scores_vs_settings[i]['alpha']=alpha_list[i]
        else:
            scores_vs_settings[i]['algorythm']='DOWNHILL'
        scores_vs_settings[i]['score']=score
        logger.error("thread genetic result:\n%s"%(scores_vs_settings[i]))
    
    logger.error("thread genetic final result:\n%s"%(scores_vs_settings))

def test_threadsm():
    STAT_LENGTH,ANNEAL,START_TEMP,ALPHA = 1000,True,100.,0.9
    best_score, finish_temp, best_routes = threadsm.main(STAT_LENGTH,ANNEAL,START_TEMP,ALPHA)
    # a_route = best_routes[-1]
    # init_len = threadsm.calc_route_length(a_route['coords'])
    # logger.error("init_len = %.3f" % (init_len))
    threadsm.plot_current_routes(0,best_routes,'best_routes before ordering')

    for a_route in best_routes:
        a_route = threadsm.order_nodes_in_route(a_route)
        ordered_len = threadsm.calc_route_length(a_route['coords'])
        logger.error("ordered_len = %.3f" % (ordered_len)) # good mean length

    threadsm.plot_current_routes(1,best_routes,'best_routes after ordering') # other mean length - why?
    ## old - obsolete
    # a_route = single_route_anneal.swap_nodes_at_random(a_route)
    # single_route_anneal.main(a_route,STAT_LENGTH,ANNEAL,START_TEMP,ALPHA)
    return True

if __name__ == "__main__":
    threadsm.setup_logging()
    logger = logging.getLogger(__name__)
    test_threadsm()