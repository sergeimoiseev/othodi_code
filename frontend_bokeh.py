#  to run by anaconda

# from bokeh.plotting import figure, output_file, show
import bokeh.plotting as bp

def plot_route_on_basemap(coord_pairs,annotes,added_points_param_list=None):
    bp.output_file("map_bokeh.html")
    # matplotlib.use('nbagg')
    # import matplotlib.pyplot as plt
    # import matplotlib.cm as cm

    # matplotlib.use('nbagg')
    # fig=plt.figure(figsize=(16,12))
    # ax=fig.add_axes([0.05,0.05,0.95,0.95])

    p = bp.figure(plot_width=640, plot_height=480)

    lat_list, lng_list = zip(*coord_pairs)

    MIN_L_WIDTH=7
    POINT_SIZE=2*MIN_L_WIDTH

    x_all=[]
    y_all=[]
    for i,point in enumerate(coord_pairs):
        lon = point[-1]
        lat = point[0]
        x,y = lon,lat
        # x,y = m(*[lon,lat])
        x_all.append(x)
        y_all.append(y)
        if (i!=0 and i!=len(annotes)-1):
            pass
            # plt.annotate(annotes[i], xy=(x,y), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec="none"))
    # plt.annotate(annotes[-1], xy=(x_all[-1],y_all[-1]), xytext=(POINT_SIZE/2,POINT_SIZE), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7)))
    # plt.annotate(annotes[0], xy=(x_all[0],y_all[0]), xytext=(POINT_SIZE/2,POINT_SIZE), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7)))

    # p.circle(x_all,y_all,size=20,color='red')
    p.line(x_all,y_all,line_width=5,color='red')

    #----
    # plt, m = add_points_to_basemap_plot(plt,m,[1,1])
    #----
    # with open("x.txt",'w') as f:
    #     pass
    if added_points_param_list!=None:
        added_points_coords = added_points_param_list[0]
        names = added_points_param_list[1]
        x_added=[]
        y_added=[]
        for i,point in enumerate(added_points_coords):
            lat = point[0]
            lon = point[-1]
            # x,y = m(*[lon,lat])
            x,y = lon,lat
            x_added.append(x)
            y_added.append(y)
            if (i!=0 and i!=len(names)-1):
                p.text(x, y, text=[names[i]], text_color="#449944", text_align="left", text_font_size="10pt")
    #         # plt.annotate(names[i], xy=(x,y), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.5, 0.7), ec="none"))
    #         plt.annotate(names[i], xy=(x,y), xytext=(0,-POINT_SIZE*2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.5, 0.7)))
            # plt.plot(x,y,ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='pink')
            # (x,y,ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='pink')
            p.circle(x,y,size=20,color='red',alpha=0.5)
    #         with open("x.txt",'a') as f:
    #             f.write("plotted %f,%f\n" % (x,y))
    # p.multi_line([x_all[:5]],[y_all[:5]],line_width=5,color='green') #works


    # draw parallels
    # m.drawparallels(np.arange(-20,0,20),labels=[1,1,0,1])
    # draw meridians
    # m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
    # ax.set_title('Great Circle from New York to London')
    # m.bluemarble()
    bp.show(p)
    # plt.show()
    # mpld3.show() # bad rendering


if __name__ == "__main__":
    # output to static HTML file
    bp.output_file("line.html")

    p = bp.figure(plot_width=400, plot_height=400)

    # add a circle renderer with a size, color, and alpha
    p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

    # show the results
    bp.save(p)
    # bp.show(p)