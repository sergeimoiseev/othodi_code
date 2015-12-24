 # -*- coding: utf-8 -*-
 # 55.7522200 широта
 # 37.6155600 долгота
 # working google key for google maps directions API!
 # AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog
 # example request 
 # https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog

import json, requests#, ittertools

url = 'https://maps.googleapis.com/maps/api/directions/json'

origin = {'latt':55.7522200,'long':37.6155600}
dest = {'latt':59.9386300,'long':30.3141300}

params = dict(
    # origin='Toronto',
    origin='%f,%f' % (origin["latt"],origin["long"]),
    # origin='55.7522200,37.6155600',
    # destination='Montreal',
    destination='%f,%f' % (dest["latt"],dest["long"]),
    # destination='59.9386300,30.3141300',
    # waypoints='Joplin,MO|Oklahoma+City,OK',
    sensor='false',
    key='AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog'
)

resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

# def pretty(d, indent=0):
#    for key, value in d.iteritems():
#       print '\t' * indent + str(key)
#       if isinstance(value, dict):
#          pretty(value, indent+1)
#       else:
#          print '\t' * (indent+1) + str(value)
# pretty(data,  indent=1)

routes = data["routes"]
print(len(routes[0]))    
print(type(routes[0]))
for key, val in routes[-1].iteritems():
    print(key)
# print("routes[0]['bounds']")    
# print(routes[0]['bounds']) 
# print("routes[0]['legs']")    
# print(routes[0]['legs'])
# print(type(routes[0]['legs'][-1]))
# print(len(routes[0]['legs'][-1]))
# for key,val in (routes[0]['legs'][-1]).iteritems():
#     print(key, len(val),type(val))

print(routes[0]['legs'][-1][u'duration'])
print(routes[0]['legs'][-1][u'distance'])

duration_text = routes[0]['legs'][-1][u'duration']['text']
distance_text = routes[0]['legs'][-1][u'distance']['text']

# title_text = tr_ru(u"Характерные масштабы задачи управления распределением отходов")
# ax.set_title(title_text)
# ax.set_xlabel(tr_ru(u'Время, ч'))
# ax.set_ylabel(tr_ru(u'Вес, кг'))
coord_pairs = [(origin['latt'],origin['long']),(56.8583600,35.9005700),(dest['latt'],dest['long'])]
# coord_pairs = [(origin['latt'],origin['long']),(dest['latt'],dest['long'])]

import sys
# sys.exit(0)
# y_coords = [origin['long'],dest['long']]
annotations=[u"Source",u"Tver",u"Reciever\n%s\n%s" % (duration_text,distance_text)]
# annotations=[u"Source",u"Reciever\n%s\n%s" % (duration_text,distance_text)]
# print(annotations[-1])

# import itertools
# def pairwise(iterable):
#     "s -> (s0,s1), (s1,s2), (s2, s3), ..."
#     a, b = itertools.tee(iterable)
#     next(b, None)
#     return itertools.izip(a, b)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
MIN_L_WIDTH=10
POINT_SIZE=2*MIN_L_WIDTH

fig = plt.figure("caption",figsize=(10,10))
ax = fig.add_subplot(111)

# colors_list = cm.rainbow(np.linspace(0,1,len(coord_pairs)))
ax.plot(*zip(*coord_pairs),ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='r')
for i, txt in enumerate(annotations):
	ax.annotate(txt, (coord_pairs[i][0],coord_pairs[i][1]), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points')
	# ax.annotate(txt, (coord_pairs[i][0],coord_pairs[i][1]), xytext=(1,1))
ax.set_xlim([0.5*min(zip(*coord_pairs)[0]),1.5*max(zip(*coord_pairs)[0])]) # must be after plot
ax.set_ylim([0.5*min(zip(*coord_pairs)[1]),1.5*max(zip(*coord_pairs)[1])])

plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
# color_iter_lines=iter(cm.rainbow(np.linspace(0,1,len(coord_pairs))))
# color_iter_points=iter(cm.rainbow(np.linspace(0,1,len(coord_pairs))))
# for points_pair in pairwise(coord_pairs):
# 	x_list = [points_pair[0][0],points_pair[1][0]]
# 	y_list = [points_pair[0][1],points_pair[1][1]]
# 	c=next(color_iter_lines)
# 	ax.loglog(x_list,y_list,ls='-',lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color=c)

# for pair in coord_pairs:
# 	c=next(color_iter_points)
# 	print("color = %s" % c)
# 	ax.loglog(pair[0],pair[1],marker='o',ms=point_size,mec='None',alpha=1,color=c)

# for i, txt in enumerate(annotations):
#     ax.annotate(txt, (coord_pairs[i][0],coord_pairs[i][1]))

plt.show()