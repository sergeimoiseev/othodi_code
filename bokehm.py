#  to run by anaconda

# from bokeh.plotting import figure, output_file, show
import bokeh.plotting as bp
import bokeh_gmapm

class Figure(object):
    def __init__(self, *args, **kwargs):
        self._output_fname = kwargs.get('output_fname',"bokeh.html")
        bp.output_file(self._output_fname)
        self._use_gmap = kwargs.get('use_gmap',False)
        if self._use_gmap and kwargs.get('center_coords',False):
            self._p = bokeh_gmapm.create_plot(kwargs['center_coords'],zoom_level = 8)
        else:
            self._p = bp.figure(plot_width=640, plot_height=480)
    def add_line(self, *args,**kwargs):
        if self._use_gmap:
            c_size=kwargs.get('circle_size',15)
            c_color=kwargs.get('circles_color','red')
            bokeh_gmapm.add_line(self._p,args[0],circle_size=c_size,circles_color=c_color)
        else:
            if len(args[0])==0:
                lats = [0,1,2,3]
                lngs = [2,3,4,5]
            else:
                lats,lngs = [],[]
                print(type(args[0]))
                for coords_dict in args[0]:
                    lats.append(coords_dict[u'lat'])
                    lngs.append(coords_dict[u'lng'])
            self._p.line(lats,lngs,line_width=5,color='red')
        return True
    def save2html(self):
        bp.save(self._p)
        return self._output_fname
    def show(self):
        bp.show(self._p)
        return True

def plot_route_on_basemap(coord_pairs,annotes,added_points_param_list=None):
    bp.output_file("map_bokeh.html")
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
    p.line(x_all,y_all,line_width=5,color='red')

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

            p.circle(x,y,size=20,color='red',alpha=0.5)
    bp.save(p)

if __name__ == "__main__":
    tver_coords = {u'lat':56.8583600, u'lng':35.9005700}
    fig = Figure(output_fname='bokehm_test.html',use_gmap=True, center_coords=tver_coords)
    
    line_to_plot = []
    for i in range(10):
        line_to_plot.append({u'lat':tver_coords[u'lat']*(1+i*0.0001), u'lng':tver_coords[u'lng']*(1+i*0.0001)})
    print(type(line_to_plot[0]))
    fig.add_line(line_to_plot,circle_size=20, circles_color='green')
    fig.save2html()
    fig.show()
