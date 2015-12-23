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

# print(data)
# print(data['distance'])
# for key,value in data.keys():
#     print(key)
#     for k,v in value

def pretty(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)
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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

fig = plt.figure("caption",figsize=(10,10))
ax = fig.add_subplot(111)
# title_text = tr_ru(u"Характерные масштабы задачи управления распределением отходов")
# ax.set_title(title_text)
# ax.set_xlabel(tr_ru(u'Время, ч'))
# ax.set_ylabel(tr_ru(u'Вес, кг'))
x_coords = [origin['latt'],dest['latt']]
y_coords = [origin['long'],dest['long']]

annotations=[u"Source",u"Reciever\n%s\n%s" % (,)]
# annotations=[u"Масштаб\nотходов",u"Масштаб\nперевозок",u"Масштаб\nпроизводственных\nсмен",u"Масштаб\nпроизводственных\nциклов",u"Масштаб\nпланирования\nпроизводства"]
