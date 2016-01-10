# -*- coding: utf-8 -*-
import numpy as np
import time
import random
import sys
# import numbers
#---- old
# adjacency_matrix =np.array([[0,1,1,1,0], # матрица смежности
#                             [1,0,1,0,1],
#                             [1,1,0,1,1],
#                             [1,0,1,0,1],
#                             [0,1,1,1,0]])
# am = adjacency_matrix
# potentials_matrix = np.zeros(am.shape,dtype='f')
# pm = potentials_matrix

# nodes_num = len(adjacency_matrix)  # число вершин

# # filling index_matrix

# pm[0][1], pm[0][2], pm[0][3] = 30, 40, 50
# pm[1][2], pm[2][3] = 10, 20
# pm[4][1], pm[4][2], pm[4][3] = 80, 60, 70
# pm = pm + pm.T - np.diag(pm.diagonal())
# # print(pm)
# # finding shortest route
#--- end old

def fastest_route(pm):
    nodes_num = len(pm)
    dt = np.dtype([('edges', np.float32,(nodes_num,2)),('dur', np.int32)])
    lm = np.zeros((nodes_num),dtype=dt)
    mpm = np.ma.masked_equal(pm, 0.0, copy=False) # mask zero elements
    for i in range(1,nodes_num):  # select new current node
        sums = np.empty((0))
        idxs = []
        for ii in range(0,i):
            if mpm[ii][i] is np.ma.masked:
                sums = np.append(sums,1e5) # if there`s no route - set its duration to a big number
            else:
                sums = np.append(sums,lm[ii]['dur']+mpm[ii][i])  # sum previouse node`s treavel duration and last edge`s duration
            idxs.append([ii,i]) # append indeses of the last edge

        i_min = np.argmin(sums)  # find route with minimal duration (fastest route to current node)
        lm[i]['dur']=sums[i_min] # set current node`s treavel duration to the min duration found
        lm[i]['edges'][0] = idxs[i_min] # set current node`s last edge in the route to the last edge of fastest route
        for step in range(nodes_num):  # loop through previouse nodes 
            prev_node = lm[i]['edges'][step][0]
            if prev_node != 0:
                lm[i]['edges'][step+1] = lm[prev_node]['edges'][0]  # append previouse nodes` last edges to current node`s route
            else:
                break  # stop copying if an edge starts at first node
    return lm

def fastest_route_from_masked(mpm):
    nodes_num = len(mpm)
    dt = np.dtype([('edges', np.float32,(nodes_num,2)),('dur', np.int32)])
    lm = np.zeros((nodes_num),dtype=dt)
    # mpm = np.ma.masked_equal(pm, 0.0, copy=False) # mask zero elements
    for i in range(1,nodes_num):  # select new current node
        sums = np.empty((0))
        idxs = []
        for ii in range(0,i):
            if mpm[ii][i] is np.ma.masked:
                sums = np.append(sums,1e5) # if there`s no route - set its duration to a big number
            else:
                sums = np.append(sums,lm[ii]['dur']+mpm[ii][i])  # sum previouse node`s treavel duration and last edge`s duration
            idxs.append([ii,i]) # append indeses of the last edge

        i_min = np.argmin(sums)  # find route with minimal duration (fastest route to current node)
        lm[i]['dur']=sums[i_min] # set current node`s treavel duration to the min duration found
        lm[i]['edges'][0] = idxs[i_min] # set current node`s last edge in the route to the last edge of fastest route
        for step in range(nodes_num):  # loop through previouse nodes 
            prev_node = lm[i]['edges'][step][0]
            if prev_node != 0:
                lm[i]['edges'][step+1] = lm[prev_node]['edges'][0]  # append previouse nodes` last edges to current node`s route
            else:
                break  # stop copying if an edge starts at first node
    return lm

# print(fastest_route(pm,nodes_num))

def test_fastest_route(nodes_num,density=1):
    n = nodes_num
    pm = np.zeros((n,n))
    # for the_random in np.random.randint(0,10,(n*density)): #  very slow!!!
    #     np.put(pm, np.random.choice(range(n*n), 1, replace=False),the_random)
    # print(pm)

    pm = np.random.randint(0,10, size=(nodes_num, nodes_num))
    np.fill_diagonal(pm, 0)
    pm = np.triu(pm)
    pm = pm + pm.T
    print(pm)
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

    return t_stop-t_start, fr_res

def different_tests_run():
    # density sensitive? No
    nodes_quantity = 100
    density = 0.5
    # dt_list = []
    # density_list = []
    # for density in range(1,50):
    #     density_list.append(density/10.)
    #     dt = test_fastest_route(nodes_quantity,density=1)[0]
    #     dt_list.append(dt)
    #     print("%d - %f"% (density,dt))

    dt_list = []
    n_q_list = []
    # nodes number sensitiveness measure:
    # for n_q_power in range(1,12):
    #     n_q_list.append(2**n_q_power)
    #     dt = test_fastest_route(2**n_q_power,density=0.5)[0]
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
                [2048, 128.411000]
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

if __name__ == "__main__":
    # creating random map
    nodes_num = 10
    NO_WAY = 9999
    m = np.random.randint(-1,2, size=(nodes_num, nodes_num))
    np.fill_diagonal(m, 0)
    m = np.triu(m)
    m = m + m.T
    #  m - зеркальная матрица
    
    mpm = np.ma.masked_equal(m, 0.0)
    n_roads = mpm.count()
    print("Total roads quantity = %i" % n_roads)
    # mpm - матрица pm с маской

    # indices = np.where(mpm == np.ma.masked)  # indices contains two arrays, the column and row indices
    # unmasked_indices = np.transpose(np.array(indices))
    # print(unmasked_indices)
    # sys.exit(0)
    pm_mask = np.ma.getmaskarray(mpm) # the mask
    
    pm = np.copy(mpm)
    pm = np.ma.filled(mpm,NO_WAY)
    indices = np.where(pm != NO_WAY)  # indices contains two arrays, the column and row indices
    unmasked_indices = np.transpose(np.array(indices))

    for i_pair in unmasked_indices:
        pm[i_pair[0],i_pair[1]] = random.randint(6,9)
        mpm[i_pair[0],i_pair[1]] = random.randint(6,9)

    print(pm)
    routes_full = fastest_route(pm)
#-----------------
    nodes_num = 10
    cars_quantity = 5
    if (nodes_num % cars_quantity != 0):
        print("nodes number must be dividable by %i. Quitting." % cars_quantity)
        sys.exit(0)
    nodes_by_part = nodes_num//cars_quantity
    
    for car_num in range(cars_quantity):
        print("car number: %i" % car_num)
        start_i = car_num*nodes_by_part
        stop_i = (car_num+1)*nodes_by_part
        print("\tstart part from node No %i" % (start_i))
        print("\tstop part before node No %i" % (stop_i))
        i_range = range(start_i,stop_i)
        j_range = range(start_i,stop_i)
        print(i_range)
        car_mask = np.zeros((nodes_num,nodes_num))
        for i in i_range:
            for j in j_range:
                if i>=j:
                    print("idxs pair : %i;%i" % (i,j))
                    car_mask[:,j]=1
                    # car_mask[:j,]=1
                else:
                    car_mask[:,j]=0
                    # car_mask[:j,]=0
        # print(rng[car_num*nodes_by_part:(car_num+1)*nodes_by_part])

        car_mask = np.ma.masked_where(car_mask == 0, car_mask)
        # print(car_mask)
        mul_pm = np.multiply(mpm,car_mask)
        print(mul_pm)
        print(fastest_route_from_masked(mul_pm))
    sys.exit(0)
