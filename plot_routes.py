 # -*- coding: utf-8 -*-
 # 55.7522200 широта
 # 37.6155600 долгота
 # working google key for google maps directions API!
 # AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog
 # example request 
 # https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog

import json, requests#, ittertools

url = 'https://maps.googleapis.com/maps/api/directions/json'

params = dict(
    origin='Toronto',
    destination='Montreal',
    # waypoints='Joplin,MO|Oklahoma+City,OK',
    # sensor='false'
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
# test_json_url = "https://maps.googleapis.com/maps/api/directions/xml?origin=Toronto&destination=Montreal&key=AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog"
# test_url = "https://maps.googleapis.com/maps/api/directions/xml?origin=Toronto&destination=Montreal&key=AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog"
# import urllib
# answer = urllib.urlopen(test_json_url)
# answer = urllib.urlopen(test_json_url).read()
# print(answer)
# json_ans=json.loads(answer.text)
# for i in json_ans:
    # print(i)

