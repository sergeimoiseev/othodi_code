# -*- coding: UTF-8 -*-
#  to run by anaconda

# from bokeh.plotting import figure, output_file, show
import bokeh.plotting as bp
import bokeh_gmapm
import logging
logger = logging.getLogger(__name__)


class Figure(object):
    def __init__(self, *args, **kwargs):
        self._output_fname = kwargs.get('output_fname',"bokeh.html")
        bp.output_file(self._output_fname)
        self._use_gmap = kwargs.get('use_gmap',False)
        if self._use_gmap and kwargs.get('center_coords',False):
            self._p = bokeh_gmapm.create_plot(kwargs['center_coords'],zoom_level = 7)
        else:
            self._p = bp.figure(plot_width=640, plot_height=480)
    def add_line(self, *args,**kwargs):
        logger.info("starting line add with points num = %d" % (len(args[0])))
        if self._use_gmap:
            bokeh_gmapm.add_line(self._p,args[0],**kwargs)
        else:
            if len(args[0])==0:
                lats = [0,1,2,3]
                lngs = [2,3,4,5]
            else:
                c_size=kwargs.get('circle_size',15)
                c_color=kwargs.get('circles_color','red')
                self._p.line([d['lat'] for d in args[0]],
                            [d['lng'] for d in args[0]],
                            size=c_size,color=c_color,alpha=0.5)
                self._p.circle([d['lat'] for d in args[0]],
                            [d['lng'] for d in args[0]],
                            line_width=c_size/2,color=c_color,alpha=0.5)
            return True
    def save2html(self):
        bp.save(self._p)
        return self._output_fname
    def show(self):
        bp.show(self._p)
        return True

    def add_errorbar(self, x, y, xerr=None, yerr=None, color='red', point_kwargs={}, error_kwargs={}):
        fig = self._p
        fig.circle(x, y, color=color, **point_kwargs)

        if xerr is not None:
            x_err_x = []
            x_err_y = []
            for px, py, err in zip(x, y, xerr):
                x_err_x.append((px - err, px + err))
                x_err_y.append((py, py))
            fig.multi_line(x_err_x, x_err_y, color=color, **error_kwargs)

        if yerr is not None:
            y_err_x = []
            y_err_y = []
            for px, py, err in zip(x, y, yerr):
                y_err_x.append((px, px))
                y_err_y.append((py - err, py + err))
            fig.multi_line(y_err_x, y_err_y, color=color, **error_kwargs)


# def plot_route_on_basemap(coord_pairs,annotes,added_points_param_list=None):
#     bp.output_file("map_bokeh.html")
#     p = bp.figure(plot_width=640, plot_height=480)

#     lat_list, lng_list = zip(*coord_pairs)

#     MIN_L_WIDTH=7
#     POINT_SIZE=2*MIN_L_WIDTH

#     x_all=[]
#     y_all=[]
#     for i,point in enumerate(coord_pairs):
#         lon = point[-1]
#         lat = point[0]
#         x,y = lon,lat
#         # x,y = m(*[lon,lat])
#         x_all.append(x)
#         y_all.append(y)
#         if (i!=0 and i!=len(annotes)-1):
#             pass
#             # plt.annotate(annotes[i], xy=(x,y), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec="none"))
#     p.line(x_all,y_all,line_width=5,color='red')

#     if added_points_param_list!=None:
#         added_points_coords = added_points_param_list[0]
#         names = added_points_param_list[1]
#         x_added=[]
#         y_added=[]
#         for i,point in enumerate(added_points_coords):
#             lat = point[0]
#             lon = point[-1]
#             # x,y = m(*[lon,lat])
#             x,y = lon,lat
#             x_added.append(x)
#             y_added.append(y)
#             if (i!=0 and i!=len(names)-1):
#                 p.text(x, y, text=[names[i]], text_color="#449944", text_align="left", text_font_size="10pt")

#             p.circle(x,y,size=20,color='red',alpha=0.5)
#     bp.save(p)
def test_simple_bokeh_plot():
    tver_coords = {u'lat':56.8583600, u'lng':35.9005700}
    fig = Figure(output_fname='bokehm_simple_test.html',use_gmap=False, center_coords=tver_coords)
    line_to_plot = [{u'lat':tver_coords[u'lat']*(1+i*0.0001),
                     u'lng':tver_coords[u'lng']*(1+i*0.0001)} \
                    for i in range(10)]
    fig.add_line(line_to_plot,circle_size=20, circles_color='green')
    fig.save2html()
    fig.show()

def test_gmap_bokeh_plot():    
    tver_coords = {u'lat':56.8583600, u'lng':35.9005700}
    fig = Figure(output_fname='bokehm_test.html',use_gmap=True, center_coords=tver_coords)
    line_to_plot = []
    for i in range(10):
        line_to_plot.append({u'lat':tver_coords[u'lat']*(1+i*0.0001), u'lng':tver_coords[u'lng']*(1+i*0.0001)})
    print(type(line_to_plot[0]))
    fig.add_line(line_to_plot,circle_size=20, circles_color='green')
    fig.save2html()
    fig.show()


def main():
    pass
if __name__ == "__main__":
    main()