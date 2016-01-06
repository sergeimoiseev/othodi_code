# -*- coding: utf-8 -*-
import numpy as np
import time
# import numbers
adjacency_matrix =np.array([[0,1,1,1,0], # матрица смежности
                            [1,0,1,0,1],
                            [1,1,0,1,1],
                            [1,0,1,0,1],
                            [0,1,1,1,0]])
am = adjacency_matrix
potentials_matrix = np.zeros(am.shape,dtype='f')
pm = potentials_matrix

nodes_num = len(adjacency_matrix)  # число вершин

# filling index_matrix

pm[0][1], pm[0][2], pm[0][3] = 30, 40, 50
pm[1][2], pm[2][3] = 10, 20
pm[4][1], pm[4][2], pm[4][3] = 80, 60, 70
pm = pm + pm.T - np.diag(pm.diagonal())
# print(pm)
# finding shortest route


def fastest_route(pm,nodes_num):
    dt = np.dtype([('edges', np.float32,(nodes_num,2)),('dur', np.int32)])
    lm = np.zeros((nodes_num),dtype=dt)
    # lambdas_matrix = np.zeros((nodes_num),dtype='f')
    # lm = lambdas_matrix
    # fastest_route = []
    mpm = np.ma.masked_equal(pm, 0.0, copy=False)
    for i in range(1,nodes_num):
        # print('i=%i' % i)
        sums = np.empty((0))
        idxs = []
        for ii in range(0,i):
            # print("ii=%i" % ii)
            if mpm[ii][i]  is np.ma.masked:
                # continue
                # sums = np.append(sums,np.finfo(np.int32).max) # errors. Why?
                sums = np.append(sums,1e5) # errors. Why?
            else:
                sums = np.append(sums,lm[ii]['dur']+mpm[ii][i])
            idxs.append([ii,i])
        i_min = np.argmin(sums)
        lm[i]['dur']=sums[i_min]
        # print('idxs pair to put to lm:'+str(idxs[i_min]))
        offset = 0
        # print('edges_set')
        lm[i]['edges'][0] = idxs[i_min]
        for step in range(nodes_num):
            # print("step = %d" % step)
            prev_node = lm[i]['edges'][step][0]
            # print(prev_node)
            if prev_node != 0:
                # print(("  lm[%d]['edges'][0] = "% prev_node)+str( lm[prev_node]['edges'][0]))
                lm[i]['edges'][step+1] = lm[prev_node]['edges'][0]
            else:
                break
    return lm

# print(fastest_route(pm,nodes_num))

def test_fastest_route(nodes_num,density):
    # pm = np.array( [[0,1,1,1,0,0], 
    #                 [1,0,1,0,1,0],
    #                 [1,1,0,1,1,0],
    #                 [1,0,1,0,1,0],
    #                 [0,1,1,1,0,1],
    #                 [0,0,0,0,1,0],
    #                 ])
    # pm[0][1], pm[0][2], pm[0][3] = 30, 40, 50
    # pm[1][2], pm[2][3] = 10, 20
    # pm[4][1], pm[4][2], pm[4][3] = 80, 60, 70
    # pm[5][4] = 20
    n = nodes_num
    # p = 3
    pm = np.zeros((n,n))
    for the_random in np.random.randint(0,10,(n*density)):
        np.put(pm, np.random.choice(range(n*n), 1, replace=False),the_random)
    # print(pm)

    pm = np.random.randint(0,10, size=(nodes_num, nodes_num))
    np.fill_diagonal(pm, 0)
    pm = np.triu(pm)
    pm = pm + pm.T
    # print(pm)
    t_start = time.time()
    fr_res = fastest_route(pm,pm.shape[0])
    t_stop = time.time()
    # print(fr_res)
    # for r_n,route in enumerate(fr_res):
    #     str_route = ""
    #     print("route finish - %d, duration - %d" % (r_n,route['dur']))
    #     for node in route['edges'][:,0]:
    #         if node != 0:
    #             str_route += "%d->" % node
    #     print(str_route)
    # print("t_start = %f, t_stop = %f\ndelta_t = %f" % (t_start,t_stop,t_stop-t_start))

    return t_stop-t_start

# density sensitive? No
nodes_quantity = 100
density = 0.5
# dt_list = []
# density_list = []
# for density in range(1,50):
#     density_list.append(density/10.)
#     dt = test_fastest_route(nodes_quantity,density)
#     dt_list.append(dt)
#     print("%d - %f"% (density,dt))

dt_list = []
n_q_list = []
# nodes number sensitiveness measure:
# for n_q_power in range(1,12):
#     n_q_list.append(2**n_q_power)
#     dt = test_fastest_route(2**n_q_power,0.5)
#     dt_list.append(dt)
#     print("%d - %f"% (2**n_q_power,dt))

#plotting sensitiveness from nodes number
results =  [[2, 0.000000],
            [4, 0.001000],
            [8, 0.002000],
            [16, 0.008000],
            [32, 0.029000],
            [64, 0.116000],
            [128, 0.490000],
            [256 ,1.947000],
            [512, 7.828000],
            [1024, 31.756000],
            ]
r_T = map(list, zip(*results))
from bokeh.plotting import figure, output_file, show, save

# output to static HTML file
output_file("graph_fastest.html")

p = figure(plot_width=400, plot_height=400)

# add a circle renderer with a size, color, and alpha
p.circle(r_T[0],r_T[1], size=20, color="navy", alpha=0.5)

# show the results
show(p)
save(p)