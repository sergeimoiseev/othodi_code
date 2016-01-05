# -*- coding: utf-8 -*-
import numpy as np
adjacency_matrix =np.array([[0,1,1,1,0], # матрица смежности
                            [1,0,1,0,1],
                            [1,1,0,1,1],
                            [1,0,1,0,1],
                            [0,1,1,1,0]])
am = adjacency_matrix
index_matrix = np.zeros(am.shape,dtype='f')
im = index_matrix

nodes_num = len(adjacency_matrix)  # число вершин

# filling index_matrix

im[0][1], im[0][2], im[0][3] = 30, 40, 50
im[1][0], im[2][0], im[3][0] = 30, 40, 50
im[1][2], im[2][3] = 10, 20
im[2][1], im[3][2] = 10, 20
im[4][1], im[4][2], im[4][3] = 80, 60, 70
im[1][4], im[2][4], im[3][4] = 80, 60, 70

# finding shortest route
indeces = [(i, j) for i, j in numpy.ndindex(am.shape)] # list storen in memory

