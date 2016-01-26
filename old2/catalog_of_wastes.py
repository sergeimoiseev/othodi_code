# -*- coding: utf-8 -*-
"""structure WasteTypes
	{'type_name':{'code':3d4fw; 'physical_state':'solid/liquid/paste'; ... };
	 'other_type_name'}"""

# import warnings
class WastesCatalog(dict):
	def __init__(self, *args, **kwargs):
		super(dict, self).__init__()
		self._catalog_filename = kwargs.get('catalog_filename','waste_types.txt')
	@property
	def catalog_filename(self):
	    return self._catalog_filename
	

	def read_waste_types(self, file_name=None,mode='a'):
		if mode == 'a' and not file_name:
			with open(self._catalog_filename,'r') as catalog_file:
				for line in catalog_file:
					parts=line.strip().split(',')
					self[parts[0]] = {'physical_state':parts[1]}
		else:
			raise NotImplementedError("reading additional catalogs is not implemented yet")
	def search(self,waste_type_name):
		if waste_type_name in self.keys():
			return True
		else:
			return False


wac = WastesCatalog()
wac.read_waste_types()

if __name__ == "__main__":
	wcat_test = WastesCatalog()
# else:
	# return wac