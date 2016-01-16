# -*- coding: UTF-8 -*-
from __future__ import print_function

# from bokeh.util.browser import view
# from bokeh.document import Document
# from bokeh.embed import file_html
from bokeh.plotting import show, save, output_file
from bokeh.models.glyphs import Circle, Line
from bokeh.models import (
    GMapPlot, Range1d, ColumnDataSource, PanTool, WheelZoomTool, BoxSelectTool, GMapOptions)
# from bokeh.resources import INLINE
import logging, inspect  # for logger
logger = logging.getLogger(__name__)

def create_plot(center_coords,zoom_level = 8):

    x_range = Range1d()
    y_range = Range1d()

    # JSON style string taken from: https://snazzymaps.com/style/1/pale-dawn
    map_options = GMapOptions(lat=center_coords['lat'], lng=center_coords['lng'], map_type="roadmap", zoom=zoom_level, styles="""
    [{"featureType":"administrative","elementType":"all","stylers":[{"visibility":"on"},{"lightness":33}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2e5d4"}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#c5dac6"}]},{"featureType":"poi.park","elementType":"labels","stylers":[{"visibility":"on"},{"lightness":20}]},{"featureType":"road","elementType":"all","stylers":[{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry","stylers":[{"color":"#c5c6c6"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#e4d7c6"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#fbfaf7"}]},{"featureType":"water","elementType":"all","stylers":[{"visibility":"on"},{"color":"#acbcc9"}]}]
    """)

    plot = GMapPlot(
        x_range=x_range, y_range=y_range,
        map_options=map_options,
        title=u"Тверь"
    )

    pan = PanTool()
    wheel_zoom = WheelZoomTool()
    box_select = BoxSelectTool()

    plot.add_tools(pan, wheel_zoom, box_select)
    return plot

def add_line(plot, coords_dict_list, circle_size=15,circles_color='blue',alpha= 0.5):
    caller_name, func_name, func_args = inspect.stack()[1][3], inspect.stack()[0][3], inspect.getargvalues(inspect.currentframe())[3]
    logger.debug("%s called %s with args = %s" % (caller_name, func_name, func_args))

    if type(circle_size)!=type([]):
        c_size = [circle_size for c_dict in coords_dict_list]
        l_width = [circle_size/2 for c_dict in coords_dict_list]
    else:
        c_size = circle_size
        l_width = [circle_size[-1]/2 for c_dict in coords_dict_list]
    source_data = { 
                'lat':[c_dict['lat'] for c_dict in coords_dict_list],
                'lng':[c_dict['lng'] for c_dict in coords_dict_list],
                'fill':[circles_color for c_dict in coords_dict_list],
                'alpha':[alpha for c_dict in coords_dict_list],
                'circle_size':c_size,
                'line_width':l_width,
                }
    source = ColumnDataSource(data=source_data)
    circle = Circle(x="lng", y="lat", size="circle_size", fill_color="fill", line_color="black",fill_alpha = "alpha")
    line = Line(x="lng", y="lat", line_width="line_width", line_color="fill", line_alpha = "alpha",line_join='round',line_cap = 'round')
    plot.add_glyph(source, line)
    plot.add_glyph(source, circle)

def main(plot_fname="gmap_example_bokeh.html"):
    output_file(plot_fname)
    tver_coords = {u'lat':56.8583600, u'lng':35.9005700}
    plot_created = create_plot(tver_coords,zoom_level = 13)

    lats=[56.8583600, 56.8583600*1.0001, 56.8583600*1.0002]
    lngs=[35.9005700, 35.9005700*1.0001, 35.9005700*1.0002]
    coords_dict_list = [{u'lat':la, u'lng':ln} for la,ln in zip(lats,lngs)]

    add_line(plot_created,coords_dict_list,circle_size=10)
    save(plot_created)
    # doc = Document()
    # doc.add_root(plot)

if __name__ == "__main__":
    main()