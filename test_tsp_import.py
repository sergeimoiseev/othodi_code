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

def run():
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
    points_num= len(lines_list)

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

    if enable_plotting:
        from bokeh.plotting import figure, output_file, show, save
        import bokeh.plotting as bp
        import numpy as np
        # output to static HTML file
        IMG_FILE_NAME = 'way_down.html'
        bp.output_file(IMG_FILE_NAME)

        p = figure(plot_width=400, plot_height=400)

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
    return tsp_result

def optimize_run_times(max_itterations):
    res_list = []
    max_itterations = 100
    for runs in range(10000):
        res_list.append(run()[1])

    # 10 times 100 000  - best score -2525.38746204
    # 100 times 10 000  - best score -2229.49214494
    # 1 000 times 1 000  - best score -2482.26776269
    # 10 000 times 100  - best score -2683.69343233

    print(max(res_list))

if __name__ == "__main__":
    global max_itterations
    optimize_run_times(max_itterations)