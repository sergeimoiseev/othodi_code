# -*- coding: utf-8 -*-
import sys, os
import tsp.tsp
import time, random, itertools

# tour_length = 20
# tour=range(1,tour_length-1)
# random.shuffle(tour)
# tour = [0]+tour+[tour_length-1]
# print(tour)

# start_city = tour[0]
# finish_city = tour[-1]
# tour = tour[1:-1]
# # for ii in range(100):
# #     all_pairs = [list(pair) for pair in itertools.combinations(tour,2)]
# #     print("len of all_pairs = %d" % len(all_pairs))
# all_pairs = [list(pair) for pair in itertools.combinations(tour,2)]
# print("all_pairs = %s" % str(all_pairs))

# usage: python %s [-o <output image file>] [-v] [-m reversed_sections|swapped_cities] -n <max iterations> [-a hillclimb|anneal] [--cooling tart_temp:alpha] <city file>" % sys.argv[0]

output_image_file_name = "out.html"
move_operator_name = "swapped_cities"
max_itterations = 100000
alg_type = "anneal"
start_temp = 25
alpha = 0.9999
cooling_str = ''.join([str(start_temp),':',str(alpha)])
city_fname = "city20.txt"
os.chdir('tsp/')

enable_plotting = False


def plot_log_data(sa_log_data, enable_plotting):
    if enable_plotting:
        from bokeh.plotting import figure, output_file, show, save
        import bokeh.plotting as bp
        import numpy as np
        # output to static HTML file
        IMG_FILE_NAME = 'way_down.html'
        bp.output_file(IMG_FILE_NAME)

        p = figure(plot_width=400, plot_height=400)

        points_num = len(sa_log_data)
        color_list = ["#%02x%02x%02x" % (r, g, 255./points_num) for r, g in zip(np.arange(0,255,255./points_num),  np.arange(0,255,255./points_num))]
        # print(color_list)
        # color_list = ["#%02x%02x%02x" % (r, g, points_num) for r, g in zip(np.floor(50+2*x), np.floor(30+2*y))]


        import numpy as np
        nparr = np.array(sa_log_data)
        x_list = list(range(points_num))
        p.circle(x_list,nparr[:,1],color=color_list)
        t_np_arr = np.array(x_list)+nparr[:,0]
        p.circle(t_np_arr,nparr[:,1],color=color_list)

        # show the results
        show(p)
        save(p)

def run(max_itt, a,enable_plotting = False):
    alpha = a
    max_itterations = max_itt
    # print("max_itterations = %d" % (max_itterations))
    # sys.argv = ['tsp.py','-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,city_fname]
    if enable_plotting:
        sys.argv = ['tsp.py','-o',output_image_file_name,'-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,city_fname]
    else:
        sys.argv = ['tsp.py','-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,city_fname]
    # sys.argv = ['tsp.py','-o',output_image_file_name,'-v','-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,city_fname]

    start_time = time.time()
    tsp_result = tsp.tsp.main()
    stop_time = time.time()

    # -- обработка--
    log_file_name = ""
    with open('last_log_file_name.txt','r') as log_fname_file:
        log_file_name = log_fname_file.read().strip()

    lines_list = []
    with open(log_file_name,'r') as input_fname:
        lines_list = input_fname.readlines()
    # points_num= len(lines_list)

    sa_log_data = []
    for line in lines_list:
        line_parts = line.split(';')
        line_values_list = []
        for part in line_parts:
            line_values_list.append(float(part.split('=')[-1].strip()))
        sa_log_data.append(line_values_list)

    # print(sa_log_data[-1])
    # print('points_num = %d' % points_num)
    # print('delta t = %.04f' % (stop_time - start_time))
    plot_log_data(sa_log_data,enable_plotting)
    return tsp_result,sa_log_data

def optimize_run_times(max_itt,cycles_num,a):
    res_list = []
    for runs in range(cycles_num):
        res_list.append(run(max_itt,a)[1])

    # alpha = 0.9999
    # 10 times 100 000  - best score -2525.38746204
    # 100 times 10 000  - best score -2229.49214494 , -2296.61038395
    # 1 000 times 1 000  - best score -2482.26776269
    # 10 000 times 100  - best score -2683.69343233

    # alpha = 0.999
    # 100 times 10 000  - best score -2340.09099989, -2253.20618323
    # alpha = 0.99
    # 100 times 10 000  - best score -2347.87068895, -2327.06489542
    # alpha = 0.99999
    # 100 times 10 000  - best score -2270.94014931, -2236.13488074

    # best settings for 20 cities:
    # alpha = 0.999 run 100 times with max_ittertions=10 000
    # init temp = 25

    print(max(res_list))

if __name__ == "__main__":
    # max_itt_num = 10000
    # cycles_num = 100
    # alpha = 0.99999
    # optimize_run_times(max_itt_num,cycles_num,alpha)
    
    cycles_num = 10
    alpha = 0.8
    max_itt_num = 100000
    res_list = []
    sa_logs_list = []
    for runs in range(cycles_num):
        print("%d runs from %d cycles" % (runs, cycles_num))
        tsp_result, sa_log_data = run(max_itt_num,alpha)
        res_list.append(list(tsp_result))
        sa_logs_list.append(sa_log_data)
        print(tsp_result[1])

    import numpy as np
    scores_list = []
    for i in range(len(res_list)):
        scores_list.append(res_list[i][1])
    npa = np.array(scores_list)
    max_index = npa.argmax()
    # print(npa[max_index])
    # print(res_list[max_index])
    best_results = res_list[max_index]

    import tsp.tsp as tsp
    coords=tsp.read_coords(file(city_fname))
    best_tour = best_results[-1]
    title = ""
    img_fname = 'best_of_%d_cycles_alpha_%.4f_itt_num_%d.html' % (cycles_num,alpha,max_itt_num)
    tsp.write_tour_to_img(coords,best_tour,title,img_fname) # coords,tour,title,img_file_name):
    plot_log_data(sa_logs_list[max_index],True)