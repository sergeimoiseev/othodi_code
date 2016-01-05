# -*- coding: utf-8 -*-
import numpy as np
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

def min_and_idxs(np_arr):
    upper_tri = np.triu(np_arr)
    m_a = np.ma.masked_equal(upper_tri, 0.0, copy=False)
    idxs_min_T = np.where(m_a == m_a.min())
    idxs_min = np.asarray(idxs_min_T).T
    idxs_min_tuples = [tuple(idx_pair) for idx_pair in idxs_min]
    # print(idxs_min_tuples)
    # return {'min':np_arr[idxs_min_tuples[0]], 'idxs':idxs_min_tuples}
    try:
        return {'min':np_arr[idxs_min_tuples[0]], 'idxs':idxs_min_tuples[0]}
    except IndexError:
        return {'min':0, 'idxs':[(0,0)]}


def mask_from_index(np_arr,idx):
    shape = np_arr.shape
    m_a_i = np.fromfunction(lambda i, j: i==idx, shape, dtype=int)
    m_a_j = np.fromfunction(lambda i, j: j==idx, shape, dtype=int)
    # m_a_i = np.fromfunction(lambda i, j: i>idx, shape, dtype=int)
    # m_a_j = np.fromfunction(lambda i, j: j>idx, shape, dtype=int)
    m_a_or = np.ma.mask_or(m_a_i,m_a_j)
    return np.ma.masked_array(np_arr, np.logical_not(m_a_or))  # creates a copy
    # return np.ma.masked_array(np_arr, m_a_or)  # creates a copy

# print(mask_from_index(pm,2))
# print(min_and_idxs(mask_from_index(pm,1)))


lambdas_matrix = np.zeros((nodes_num+1),dtype='f')
lm = lambdas_matrix
fastest_route = []
for i in range(1,nodes_num+1):
    print(i)
    sums, idxs = [], []
    for ii in range(0,i):
        mask = mask_from_index(pm,ii)
        print('ii=%i'% ii)
        print(mask)
        print('lm[%i] = %i' % (ii,lm[ii]))
        masked_min = min_and_idxs(mask)
        print("masked_min['min'] = %i" % masked_min['min'])
        # masked_min = pm[:,i]
        sums.append(lm[ii]+masked_min['min'])
        idxs.append(masked_min['idxs'])
    print(sums)
    print(idxs)
    lm[i]+=min(sums)
    print('new lm = %s' % lm)
    # min_idxs = min_and_idxs(mask_from_index(pm,i))
    # print(min_idxs['min'])
print(lm)