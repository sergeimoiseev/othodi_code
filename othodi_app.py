# -*- coding: utf-8 -*-
import shutil
import locm, routem, mapm, dropboxm, gmaps, tools

if __name__ == "__main__":

    cities_fname = 'cities_from_dropbox.txt'
    # dr_fname = '/othodi/cities_few.txt'
    # dc = dropboxm.DropboxConnection()
    # with dc.open_dropbox_file(dr_fname) as dropbox_file:
    #     address_list = [line.strip() for line in dropbox_file]
    with open(cities_fname,'r') as cities_file:
        address_list = [line.strip() for line in cities_file.readlines()]
        
    locs_list = [locm.Location(addr) for addr in address_list]
    moscow = locm.Location('Moscow')
    routes_list = [routem.Route(moscow.coords,dest.coords) for dest in locs_list]
    for route,loc in zip(routes_list,locs_list):
        print(loc.address)
        print(route.to_str())