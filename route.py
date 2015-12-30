# -*- coding: utf-8 -*-

"""
class Route
	properties
		s = {'lat':67.89, 'lon':78.78}
		f = {'lat':69.89, 'lon':79.78}
		distance
		duration
		points_list = [{'lat':..,'lon':...},{'lat':..,'lon':...},...]
		points_annotes = [u'dur',u'dur',...]
"""
import gmaps

class Route(object):
	def __init__(self, *args, **kwargs):
		if len(args)==2 and all(isinstance(point, dict) for point in args):
		self._start = args[0]
		self._finish = args[1]
		dict_from_gmaps = gmaps.get_route(self._start, self._finish)
