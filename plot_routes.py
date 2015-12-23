 # -*- coding: utf-8 -*-
 # 55.7522200 широта
 # 37.6155600 долгота
 # working google key for google maps directions API!
 # AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog
 # example request 
 # https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog

test_json_url = "https://maps.googleapis.com/maps/api/directions/xml?origin=Toronto&destination=Montreal&key=AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog"
# test_url = "https://maps.googleapis.com/maps/api/directions/xml?origin=Toronto&destination=Montreal&key=AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog"
import urllib
answer = urllib.urlopen(test_url).read()
# print(doc[:350])

from bs4 import BeautifulSoup, SoupStrainer
line=answer
# line='<City_State>PLAINSBORO, NJ 08536-1906</City_State>'
soup = BeautifulSoup(line,'lxml')
# print(soup.find('distance').text)
# print(soup.find('distance').text)

def find_total_dur_dist_in_soup(soup_obj):
    # for duration in 
    distance_list = soup_obj.find_all('distance')
    duration_list = soup_obj.find_all('duration')
    total_duration, total_distance = max(duration_list), max(distance_list)
    return total_duration, total_distance
print(find_total_dur_dist_in_soup(soup))

# print(soup.find('duration').text)
# print(soup.find('value').text)
# print(soup.find('city_state').text)
# print(soup)
# for link in BeautifulSoup(answer, parseOnlyThese=SoupStrainer('text')):
#     print(link)
    # if link.has_attr('href'):
    #     print link['href']

# import re
# def parse_get_treavel_time(urllib_read_data):
#     groups = re.search('>.*<', urllib_read_data)
#     return groups
    # return treaver_time
# list_of_things_between_tags = parse_get_treavel_time(answer)
# print(list_of_things_between_tags)