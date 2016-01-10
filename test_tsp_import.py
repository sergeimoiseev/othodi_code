import sys, os
import tsp.tsp

print(dir(tsp.tsp))
# usage: python %s [-o <output image file>] [-v] [-m reversed_sections|swapped_cities] -n <max iterations> [-a hillclimb|anneal] [--cooling start_temp:alpha] <city file>" % sys.argv[0]
output_image_file_name = "out.html"
move_operator_name = "swapped_cities"
max_itterations = 10000
alg_type = "anneal"
start_temp = 25
alpha = 0.999
cooling_str = ''.join([str(start_temp),':',str(alpha)])
city_fname = "city100.txt"

sys.argv = ['tsp.py','-o',output_image_file_name,'-v','-m',move_operator_name,'-n',max_itterations,'-a',alg_type,'--cooling',cooling_str,city_fname]
os.chdir('tsp/')
tsp.tsp.main()
