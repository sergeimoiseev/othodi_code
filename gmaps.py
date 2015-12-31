# -*- coding: utf-8 -*-
"""
module gmaps
	methods
        get_lat_lon(address_string)
        get_address(location_object)
        get_route(start, finish)
"""
import json, requests
import tools
# import time

def get_lat_lon(address_string):
    url = "http://maps.google.com/maps/api/geocode/json"
    # ?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false
    address_string+=',Russia'
    params = dict(
        address=address_string,
        sensor='false',
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    print(address_string)
    # print(data)
    # for key,val in (data[u'results'][0]).iteritems():
    #     print(key, len(val),type(val))
    try:
        geo = (data[u'results'][0][u'geometry'])
    except Exception as e:
        print(len(data))
        print('error while parcing geo data:\n%s' % e)
        print(data[u'results'])
        print(data)
        return {}
    # for key,val in (geo).iteritems():
    #     print(key, len(val),type(val))
    location_dict = geo[u'location']
    # print(location_dict)
    return location_dict
    # return {'lat':None,'lon':None}
    # raise NotImplementedError("Should be implenmented with googlemaps.")
    # return None

def get_address(coords_dict):
    # raise NotImplementedError("Should be implenmented with googlemaps.")
    return 'no address recognition yet'

def get_route(origin, dest):
    # return 'get_route is to be implemented in gmaps module.'
# def get_route_from_gmaps(origin,dest): #- original func (worked)
    url = 'https://maps.googleapis.com/maps/api/directions/json'
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
    # print(len(routes[0]))    
    # print(type(routes[0]))
    # for key, val in routes[-1].iteritems():
    #     print(key)
    # for key,val in (routes[0]['legs'][-1]).iteritems():
    #     print(key, len(val),type(val))
    a_step = routes[0]['legs'][-1][u'steps'][0]
    # print("a_step")
    # print(type(a_step), len(a_step))
    # for key,val in (a_step.iteritems()):
    #     print(key, len(val),type(val))

    duration_text = routes[0]['legs'][-1][u'duration']['text']
    total_duration_value = routes[0]['legs'][-1][u'duration']['value']
    distance_text = routes[0]['legs'][-1][u'distance']['text']
    total_distance_value = routes[0]['legs'][-1][u'distance']['value']
    annotations=[u"Source",u"Tver",u"Reciever\n%s\n%s" % (duration_text,distance_text)]

    coord_pairs = [(origin[u'lat'],origin[u'lng']),(56.8583600,35.9005700),(dest[u'lat'],dest[u'lng'])]

    coords_list_of_dicts = []
    annotes4points = []
    coords_list_of_dicts.append(origin)
    annotes4points.append(u"Source")
    for i,step in enumerate(routes[0]['legs'][-1][u'steps']):
        # print("step No %i: %s" % (i,str(step[u'end_location'])))
        coords_list_of_dicts.append(step[u'end_location'])
        annotes4points.append(step[u'duration']['text'])
    print("route lat=%.03f lng=%.03f - > lat=%.03f lng=%.03f" % (origin[u'lat'],origin[u'lng'],dest[u'lat'],dest[u'lng']))
    coords_list_of_dicts.append(dest)
    annotes4points.append(u"Reciever\n%s\n%s" % (duration_text,distance_text))
    # print(annotes4points)

    list_of_coords_pairs = tools.get_pairs_list_from_dicts_list(coords_list_of_dicts)

    # print("total points_count = %i" % len(coords_list_of_dicts))
    # print("total annotes count = %i" % len(annotes4points))

    return list_of_coords_pairs, annotes4points, total_distance_value, total_duration_value
