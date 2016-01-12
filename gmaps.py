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
import time

def get_lat_lon(address_string):
    url = "http://maps.google.com/maps/api/geocode/json"
    address_string+=',Russia'
    params = dict(
        address=address_string,
        sensor='false',
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    # print(address_string)
    try:
        geo = (data[u'results'][0][u'geometry'])
    except Exception as e:
        print(len(data))
        print('error while parcing geo data:\n%s' % e)
        print(data[u'results'])
        print(data)
        return {}
    location_dict = geo[u'location']
    time.sleep(0.2)
    return location_dict

def get_address(coords_dict):
    # raise NotImplementedError("Should be implenmented with googlemaps.")
    return 'no address recognition yet'

def get_route(origin, dest):
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = dict(
        origin='%f,%f' % (origin[u'lat'],origin[u'lng']),
        destination='%f,%f' % (dest[u'lat'],dest[u'lng']),
        sensor='false',
        key='AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog'
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data
