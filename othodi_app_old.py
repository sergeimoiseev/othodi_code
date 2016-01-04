# -*- coding: utf-8 -*-
import shutil
import locm, mapm, dropboxm, gmaps, tools

t_raw_routes00 = [(55.755826, 37.6173), (55.7572652, 37.6186384), (55.75741840000001, 37.6190388), (55.75856830000001, 37.6183535), (55.75958259999999, 37.6247176), (55.7607021, 37.6268833), (55.7664304, 37.6313237), (55.7726528, 37.6323991), (55.81617319999999, 37.638654), (55.8490433, 37.6746007), (55.9082709, 37.76991950000001), (55.9130634, 37.7747146), (55.9210429, 37.7622377), (55.9198661, 37.7652923), (55.9198471, 37.7654985)]
t_raw_routes01 = [u'Source', u'1 min', u'1 min', u'1 min', u'1 min', u'1 min', u'3 mins', u'3 mins', u'7 mins', u'5 mins', u'10 mins', u'1 min', u'2 mins', u'1 min', u'Reciever\n33 mins\n22.9 km']
t_add_points_coords_list = [(55.7981904, 37.9679867), (55.8940553, 37.44394870000001), (55.4312453, 37.5457647), (55.9316797, 37.8518552), (55.9198471, 37.7654985), (55.686462, 37.8981554), (55.7835532, 38.4551611), (55.0937517, 38.7688618), (55.67337449999999, 37.2818569), (55.73737569999999, 38.0095391)]
t_add_points_annotes_list = ['Balashiha', 'Himki', "Podol'sk", 'Koroljov', 'Mytishhi', 'Ljubercy', "Jelektrostal'", 'Kolomna', 'Odincovo', 'Zheleznodorozhnyj']

def write_plotting_data_to_file(dropbox_filename = '/othodi/cities_few.txt',out_fname = 'data4plotting.txt'):
    m1=mapm.Map()
    m1.add_locations_from_file(fname=dropbox_filename,dropbox=True)
    print(len(m1.locations))

    origin = locm.Location("Moscow",name='Moscow')
    raw_routes = []
    for location in [locn for locn in m1.locations if locn.name != origin.name]:
        if 'lat' in location.coords and 'lng' in location.coords:
            try:
                raw_routes.append(gmaps.get_route(origin.coords, location.coords))
            except Exception as e:
                print('Warning: Error in get_route for location %s: no data from gmaps?\n%s' % (location.address,e))


    from operator import itemgetter
    raw_routes.sort(key=itemgetter(-1)) # sort by duration
    # for i,point in enumerate(m1.locations):
    #     print("%i: %s" % (i,str(point.coords)))
    add_points_coords_list = [(point.coords['lat'],point.coords['lng']) for point in m1.locations]
    add_points_annotes_list = [point.name for point in m1.locations]
    with open(out_fname,'w') as f:
        f.write(str(raw_routes[0][0]))
        f.write('\n')
        f.write(str(raw_routes[0][1]))
        f.write('\n')
        f.write(str(add_points_coords_list))
        f.write('\n')
        f.write(str(add_points_annotes_list))
    return raw_routes[0][0],raw_routes[0][1],add_points_coords_list,add_points_annotes_list

def test_plot(frontend='bokeh',data_list=[]):
    if frontend=='bokeh':
        import frontend_bokeh as frontend
    frontend.plot_route_on_basemap(data_list[0], data_list[1], [data_list[2],data_list[3]])
    shutil.copyfile('map_bokeh.html', 'templates/index.html')
    

# def update_plot()

if __name__ == "__main__":
    data4plotting = write_plotting_data_to_file(dropbox_filename='/othodi/cities.txt')
    test_plot(data_list = data4plotting)
    ## import frontend_mpl_basemap as frontend
    # frontend.plot_route_on_basemap(raw_routes[0][0], raw_routes[0][1], [add_points_coords_list,add_points_annotes_list]) # plots nearest route
  