from __future__ import print_function

# from bokeh.util.browser import view
# from bokeh.document import Document
# from bokeh.embed import file_html
from bokeh.plotting import show, save, output_file
from bokeh.models.glyphs import Circle
from bokeh.models import (
    GMapPlot, Range1d, ColumnDataSource, PanTool, WheelZoomTool, BoxSelectTool, GMapOptions)
# from bokeh.resources import INLINE

def main(plot_fname="gmap_example_bokeh.html"):
    output_file(plot_fname)
    tver_coords = {u'lat':56.8583600, u'lng':35.9005700}
    plot_created = create_plot(tver_coords,zoom_level = 13)
    save(plot_created)
    # doc = Document()
    # doc.add_root(plot)

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
        title="Austin"
    )

    # source = ColumnDataSource(
    #     data=dict(
    #         lat=[30.2861, 30.2855, 30.2869],
    #         lon=[-97.7394, -97.7390, -97.7405],
    #         fill=['orange', 'blue', 'green']
    #     )
    # )

    # circle = Circle(x="lon", y="lat", size=15, fill_color="fill", line_color="black")
    # plot.add_glyph(source, circle)

    pan = PanTool()
    wheel_zoom = WheelZoomTool()
    box_select = BoxSelectTool()

    plot.add_tools(pan, wheel_zoom, box_select)
    return plot

if __name__ == "__main__":
    main()