 # -*- coding: utf-8 -*-
 # 55.7522200 широта
 # 37.6155600 долгота
 # working google key for google maps directions API!
 # AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog
 # example request 
 # https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog

import json, requests#, ittertools
import sys

url = 'https://maps.googleapis.com/maps/api/directions/json'

origin = {u'lat':55.7522200,u'lng':37.6155600}
dest = {u'lat':59.9386300,u'lng':30.3141300}

params = dict(
    # origin='Toronto',
    origin='%f,%f' % (origin[u'lat'],origin[u'lng']),
    # origin='55.7522200,37.6155600',
    # destination='Montreal',
    destination='%f,%f' % (dest[u'lat'],dest[u'lng']),
    # destination='59.9386300,30.3141300',
    # waypoints='Joplin,MO|Oklahoma+City,OK',
    sensor='false',
    key='AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog'
)

resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

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
for key,val in (routes[0]['legs'][-1]).iteritems():
    print(key, len(val),type(val))
a_step = routes[0]['legs'][-1][u'steps'][0]
print("a_step")
print(type(a_step), len(a_step))
for key,val in (a_step.iteritems()):
    print(key, len(val),type(val))


# print(len(routes[0]['legs']))
# print(routes[0]['legs'][-1])
# sys.exit(1)
def get_pairs_list_from_dicts_list(coords_list_of_dicts):
    p_list = []
    for a_dict in coords_list_of_dicts:
        p_list.append((a_dict[u'lat'],a_dict[u'lng']))
    return p_list

duration_text = routes[0]['legs'][-1][u'duration']['text']
distance_text = routes[0]['legs'][-1][u'distance']['text']
annotations=[u"Source",u"Tver",u"Reciever\n%s\n%s" % (duration_text,distance_text)]

coord_pairs = [(origin[u'lat'],origin[u'lng']),(56.8583600,35.9005700),(dest[u'lat'],dest[u'lng'])]

coords_list_of_dicts = []
annotes4points = []
coords_list_of_dicts.append(origin)
annotes4points.append(u"Source\n\n")
print(origin)
for i,step in enumerate(routes[0]['legs'][-1][u'steps']):
    print("step No %i: %s" % (i,str(step[u'end_location'])))
    coords_list_of_dicts.append(step[u'end_location'])
    annotes4points.append(step[u'duration']['text'])
print(dest)
coords_list_of_dicts.append(dest)
annotes4points.append(u"Reciever\n%s\n%s\n\n" % (duration_text,distance_text))
print(annotes4points)

list_of_coords_pairs = get_pairs_list_from_dicts_list(coords_list_of_dicts)

print("total points_count = %i" % len(coords_list_of_dicts))
print("total annotes count = %i" % len(annotes4points))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def plot_route(coord_pairs,annotes):
    MIN_L_WIDTH=10
    POINT_SIZE=2*MIN_L_WIDTH
    fig = plt.figure("caption",figsize=(10,10))
    ax = fig.add_subplot(111)

    # colors_list = cm.rainbow(np.linspace(0,1,len(coord_pairs)))
    ax.plot(*zip(*coord_pairs),ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='r')
    for i, txt in enumerate(annotes):
        ax.annotate(txt, (coord_pairs[i][0],coord_pairs[i][1]), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points')
        # ax.annotate(txt, (coord_pairs[i][0],coord_pairs[i][1]), xytext=(1,1))
    ax.set_xlim([0.9*min(zip(*coord_pairs)[0]),1.1*max(zip(*coord_pairs)[0])]) # must be after plot
    ax.set_ylim([0.9*min(zip(*coord_pairs)[1]),1.1*max(zip(*coord_pairs)[1])])

    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.show()

# plot_route(coord_pairs,annotations)
# plot_route(list_of_coords_pairs,annotes4points)

from mpl_toolkits.basemap import Basemap
# import numpy as np
# import matplotlib.pyplot as plt
# create new figure, axes instances.
def plot_route_on_basemap(coord_pairs,annotes):
    fig=plt.figure()
    ax=fig.add_axes([0.05,0.05,0.95,0.95])
    # setup mercator map projection.
    m = Basemap(llcrnrlon=29.,llcrnrlat=53.,urcrnrlon=42.,urcrnrlat=62.,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='merc',\
                lat_0=0.,lon_0=0.,lat_ts=0.)
    # nylat, nylon are lat/lon of New York
    # nylat = 55.7522200; nylon = 37.6155600
    # lonlat, lonlon are lat/lon of London.
    # lonlat = 59.9386300; lonlon = 30.3141300
    # draw great circle route between NY and London
    # m.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='b')
    
    MIN_L_WIDTH=10
    POINT_SIZE=2*MIN_L_WIDTH
    # lon_msk = 37.6155600
    # lat_msk = 55.7522200


    m.drawcoastlines()
    m.fillcontinents()
    x_all=[]
    y_all=[]
    for i,point in enumerate(coord_pairs):
        lon = point[-1]
        lat = point[0]
        x,y = m(*[lon,lat])
        x_all.append(x)
        y_all.append(y)
        # plt.plot(x,y,marker='o',linestyle ='-',lw=5,color= 'r')
        plt.annotate(annotes[i], xy=(x,y), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points')
    plt.plot(x_all,y_all,ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='r')
    # plt.plot(x_all,y_all,marker='o',linestyle ='-',lw=5,color= 'r')
    # draw parallels
    m.drawparallels(np.arange(-20,0,20),labels=[1,1,0,1])
    # draw meridians
    m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
    # ax.set_title('Great Circle from New York to London')
    plt.show()

plot_route_on_basemap(list_of_coords_pairs,annotes4points)