# -*- coding: utf-8 -*-
"""class Waste
	properties
		mass
		wtype"""

from catalog_of_wastes import wac

class Waste(object):
	"""Class Waste describes a fixed ammount of waste"""
	def __init__(self, *args, **kwargs):
		# super(ClassName, self).__init__() # this is a base class
		self._mass = kwargs.get('mass',0.)
		test_wtype = kwargs.get('wtype',None)
		if test_wtype:
			if wac.search(test_wtype):
				self._wtype = test_wtype
			else:
				raise ValueError("can`t create waste of wtype not from catalog")

		else:
			raise ValueError("define waste type by 'wtype=' argument")
	@property
	def wtype(self):
	    return self._wtype
	@property
	def mass(self):
	    return self._mass

if __name__ == "__main__":
	w1 = Waste(mass=10.,wtype='paper')
	print(w1.wtype)
		
