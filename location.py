# -*- coding: utf-8 -*-
import ast
def type_of_value(var):
    try:
       return type(ast.literal_eval(var))
    except Exception:
       return str

def get_lat_lon(addr_str):
    raise NotImplementedError("Should be implenmented with googlemaps.")
    # return None

def get_address(location_object):
    # raise NotImplementedError("Should be implenmented with googlemaps.")
    return 'address recognition is not implemented yet.'

class Location:
    def __init__(self, *args, **kwargs):
    # def __init__(self, object_name=None, address=None, *args, **kwargs):
        #args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
        print("len(args)")
        print(len(args))
        if type_of_value(args[0])!=str and type_of_value(args[1])!=str:
            self.lat = float(args[0])
            self.lon = float(args[1])
        elif kwargs.get('address',None)!=None:
            self.lat, self.lon = get_lat_lon(kwargs['address'])
        elif type_of_value(args[0])==str:
            self.lat, self.lon = get_lat_lon(args[0])
        self.name = kwargs.get('object_name',None)
        self.address = get_address(self)
        self.id = id(self)

    # def area(self):
    #     return self.x * self.y

    # def perimeter(self):
    #     return 2 * self.x + 2 * self.y

    # def describe(self, text):
    #     self.description = text

    # def authorName(self, text):
    #     self.author = text

    # def scaleSize(self, scale):
    #     self.x = self.x * scale
    #     self.y = self.y * scale


if __name__ == "__main__":
    s1 = Location("54.8","88.6")