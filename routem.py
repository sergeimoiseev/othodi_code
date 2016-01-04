# -*- coding: utf-8 -*-
import gmaps

class Route(object):
    def __init__(self, *args, **kwargs):
        if len(args)==2 and all(isinstance(point, dict) for point in args):
            self._start = args[0]
            self._finish = args[1]
            gdata = gmaps.get_route(self._start, self._finish)
            main_dict = gdata["routes"][0]['legs'][-1]
            self._duration = main_dict[u'duration']
            self._distance = main_dict[u'distance']
            self._waypoints, self._wp_durations = [self._start], [0] 
            for step in main_dict[u'steps']:
                self._waypoints.append(step[u'end_location'])
                self._wp_durations.append(step[u'duration']['value'])
        else:
            raise ValueError('Wrong arguments passed to constructor.')

    @property
    def start(self):
        return self._start        
    @property
    def finish(self):
        return self._finish
    @property
    def duration(self):
        return self._duration
    @property
    def distance(self):
        return self._distance
    @property
    def waypoints(self):
        return self._waypoints
    @property
    def wp_durations(self):
        return self._wp_durations

    def to_str(self):
        out_str = "From %f|%f To %f|%f\n" % (self._start['lat'],self._start['lng'],self._finish['lat'],self._finish['lng'])
        out_str += "through %i steps with total distance %s\nand total duration %s." % (len(self._waypoints)-2, self._distance['text'], self._duration['text'])
        return out_str

if __name__ == "__main__":
    print('Default test of Route class.')
    c1_dict = {'lat':55.755826, 'lng':37.6173}
    c2_dict = {'lat':55.4312453,'lng': 37.5457647}
    r = Route(c1_dict,c2_dict)
    print(r.to_str())
    print(r.waypoints)
    print(r.wp_durations)
    print("duration check sum: %i min" % (sum(r.wp_durations)/(60)))