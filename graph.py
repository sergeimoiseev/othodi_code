# -*- coding: utf-8 -*-
import numpy as np
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
print(pm)
# finding shortest route
indices = [(i, j) for i, j in np.ndindex(am.shape)] # list storen in memory


def fastest_route(pm,nodes_num):
    dt = np.dtype([('edges', np.float32,(nodes_num,2)),('dur', np.int32)])
    lm = np.zeros((nodes_num),dtype=dt)
    # lambdas_matrix = np.zeros((nodes_num),dtype='f')
    # lm = lambdas_matrix
    # fastest_route = []
    mpm = np.ma.masked_equal(pm, 0.0, copy=False)
    for i in range(1,nodes_num):
        print('i=%i' % i)
        sums = np.empty((0))
        idxs = []
        for ii in range(0,i):
            # print("ii=%i" % ii)
            if mpm[ii][i]  is np.ma.masked:
                # continue
                sums = np.append(sums,np.finfo(np.float64).max)
            else:
                sums = np.append(sums,lm[ii]['dur']+mpm[ii][i])
            idxs.append([ii,i])
        i_min = np.argmin(sums)
        lm[i]['dur']=sums[i_min]
        print('idxs pair to put to lm:'+str(idxs[i_min]))
        offset = 0
        print('edges_set')
        lm[i]['edges'][0] = idxs[i_min]
        for step in range(nodes_num):
            print("step = %d" % step)
            prev_node = lm[i]['edges'][step][0]
            print(prev_node)
            if prev_node != 0:
                print(("  lm[%d]['edges'][0] = "% prev_node)+str( lm[prev_node]['edges'][0]))
                lm[i]['edges'][step+1] = lm[prev_node]['edges'][0]
    return lm

print(fastest_route(pm,nodes_num))
