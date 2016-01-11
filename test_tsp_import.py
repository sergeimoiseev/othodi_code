import sys, os
import tsp.tsp

print(dir(tsp.tsp))
# usage: python %s [-o <output image file>] [-v] [-m reversed_sections|swapped_cities] -n <max iterations> [-a hillclimb|anneal] [--cooling tart_temp:alpha] <city file>" % sys.argv[0]
output_image_file_name = "out.html"
move_operator_name = "swapped_cities"
max_itterations = 10000
alg_type = "anneal"
start_temp = 25
alpha = 0.9
cooling_str = ''.join([str(start_temp),':',str(alpha)])
city_fname = "city100.txt"

sys.argv = ['tsp.py','-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,city_fname]
# next gives error in plotting func
# sys.argv = ['tsp.py','-o',output_image_file_name,'-v','-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,city_fname]
os.chdir('tsp/')
tsp.tsp.main()

from bokeh.plotting import figure, output_file, show, save
import bokeh.plotting as bp
import numpy as np
# output to static HTML file
IMG_FILE_NAME = 'way_down.html'
bp.output_file(IMG_FILE_NAME)

p = figure(plot_width=400, plot_height=400)



# num_cities=len(tour)
# color_list = ["#%02x%02x%02x" % (r, g, num_cities) for r, g in zip(np.arange(0,255,255/num_cities),  np.arange(0,255,255/num_cities))]
# print(color_list)
# color_list = ["#%02x%02x%02x" % (r, g, num_cities) for r, g in zip(np.floor(50+2*x), np.floor(30+2*y))]
for i in range(num_cities):
    # print(color_list[i])
    j=(i+1)%num_cities
    city_i=tour[i]
    city_j=tour[j]
    x1,y1=coords[city_i]
    x2,y2=coords[city_j]
    p.line([x1,x2],[y1,y2],color=color_list[i])
    p.circle([x1,x2],[y1,y2],color=color_list[i])
    # d.line((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
    # d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(32,32,32))
# add a circle renderer with a size, color, and alpha
# p.circle(coords, size=20, color="navy", alpha=0.5)

# show the results
show(p)
save(p)