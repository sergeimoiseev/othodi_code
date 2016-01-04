 # -*- coding: utf-8 -*-

import numpy as np
import matplotlib
# matplotlib.use('nbagg')
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import mpld3
# matplotlib.use('nbagg')

def plot_route(coord_pairs,annotes):
    # matplotlib.use('nbagg')
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
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
    # mpld3.show() # bad rendering
    plt.show()

# plot_route(coord_pairs,annotations)
# plot_route(list_of_coords_pairs,annotes4points)

from mpl_toolkits.basemap import Basemap

def plot_route_on_basemap(coord_pairs,annotes,added_points_param_list=None):
    matplotlib.use('nbagg')
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    # matplotlib.use('nbagg')
    fig=plt.figure(figsize=(16,12))
    ax=fig.add_axes([0.05,0.05,0.95,0.95])

    lat_list, lng_list = zip(*coord_pairs)

    # setup mercator map projection.
    m = Basemap(llcrnrlon=min(lng_list)-2,llcrnrlat=min(lat_list)-2,urcrnrlon=max(lng_list)+2,urcrnrlat=max(lat_list)+2,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='merc',\
                lat_0=0.,lon_0=0.,lat_ts=0.)
    
    MIN_L_WIDTH=7
    POINT_SIZE=2*MIN_L_WIDTH

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
        if (i!=0 and i!=len(annotes)-1):
            plt.annotate(annotes[i], xy=(x,y), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec="none"))
    plt.annotate(annotes[-1], xy=(x_all[-1],y_all[-1]), xytext=(POINT_SIZE/2,POINT_SIZE), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7)))
    plt.annotate(annotes[0], xy=(x_all[0],y_all[0]), xytext=(POINT_SIZE/2,POINT_SIZE), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7)))

    plt.plot(x_all,y_all,ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='r')

    #----
    # plt, m = add_points_to_basemap_plot(plt,m,[1,1])
    #----
    with open("x.txt",'w') as f:
        pass
    if added_points_param_list!=None:
        added_points_coords = added_points_param_list[0]
        names = added_points_param_list[1]
        # x_added=[]
        # y_added=[]
        for i,point in enumerate(added_points_coords):
            lat = point[0]
            lon = point[-1]
            x,y = m(*[lon,lat])
            # x_added.append(x)
            # y_added.append(y)
            # if (i!=0 and i!=len(names)-1):
            # plt.annotate(names[i], xy=(x,y), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.5, 0.7), ec="none"))
            plt.annotate(names[i], xy=(x,y), xytext=(0,-POINT_SIZE*2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.5, 0.7)))
            plt.plot(x,y,ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='pink')
            with open("x.txt",'a') as f:
                f.write("plotted %f,%f\n" % (x,y))


    # draw parallels
    m.drawparallels(np.arange(-20,0,20),labels=[1,1,0,1])
    # draw meridians
    m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
    # ax.set_title('Great Circle from New York to London')
    # m.bluemarble()
    plt.show()
    # mpld3.show() # bad rendering

if __name__ == "__main__":
    print('No test yet.')