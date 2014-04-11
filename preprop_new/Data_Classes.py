# -*- coding: utf-8 -*-

import itertools
import Storage_Classes
import math
from collections import Counter

class Unit (object):
    def __init__(self, label, start, length, normalization):
        self.label = label
        self.start = start
        self.length = float(length)
        self.normalization = normalization  # (time)
        self.samples = list()
        
    def add_sample(self, sample):
        ## keine Ausreißer   ## qwe1  <-- nur zum schnell suchen..
#        if ( sample.rssi > -40 ):
#            self.samples.append(sample)

        self.samples.append(sample)
        
    def get_values(self):
        return [x.rssi for x in self.samples]

        
    ## statistical analyzations ##
    def get_sampling_rate(self):
        return len(self.samples) / self.length
    
    def get_max_gap(self):
        max_gap = float("-inf")
        for i in range(1, len(self.samples) - 1):
            gap = Storage_Classes.Sample.Get_Timediff(self.samples[i-1], self.samples[i])
            
            if ( gap > max_gap ):
                max_gap = gap

        ## doesn't work..
##        # corner cases  (not that nicely programmed.. :-/ TODO create suitable functions in Sample-class)
##        gap = self.samples[0].get_normalized_timestamp(self.normalization)
##        if ( gap > max_gap ):
##            max_gap = gap
##        gap = - self.samples[-1].get_normalized_timestamp(self.normalization + self.length)
##        if ( gap > max_gap ):
##            max_gap = gap
        

        
#        assert(max_gap != float("-inf"))   XXX
        
        return max_gap
    
    
    def get_min_gap(self):
        min_gap = float("inf")
        for i in range(1, len(self.samples) - 1):
            gap = Storage_Classes.Sample.Get_Timediff(self.samples[i-1], self.samples[i])
            
            if ( gap < min_gap ):
                min_gap = gap
                
#        assert(min_gap != float("inf"))  XXX
        
        return min_gap
        
        
    def show(self):
        print
        print "Unit:", self.start, "-", self.start + self.length
        
        if ( len(self.samples) < 2 ):
            print "EMPTY"
        else:
            print "Avg. sampling rate:", self.get_sampling_rate(), "Hz"
            print "Gaps [ms]:", self.get_min_gap() * 1000, 1000 / self.get_sampling_rate(), self.get_max_gap() * 1000




    ## XXX testing with smallest and 2nd smallest rssi value
    def get_min_value(self):
        min1 = 0
        min2 = 0
        
        for x in self.samples:
            if ( x.rssi <= min1 ):
                min2 = min1
                min1 = x.rssi
            elif ( x.rssi < min2 ):
                min2 = x.rssi
                
        return min1


    def get_max_value(self):
        max = -255
        
        for x in self.samples:
            if ( x.rssi > max ):
                max = x.rssi
                
        return max
        


    ## feature calculation ##
    # mean
    def calc_mean(self):
        ## empty
        if ( len(self.samples) == 0 ):
            return 0

        ## calc mean
        sum = 0
        
        for x in self.samples:
            sum += x.rssi
            
        return float(sum) / len(self.samples)
        
    # variance
    def calc_variance(self):
        ## empty
        if ( len(self.samples) < 2 ):
            return 0

        ## calc variance
        mean = self.calc_mean()
        sum = 0
        
        for x in self.samples:
            sum += (x.rssi - mean) ** 2
            
        return math.sqrt( sum / (len(self.samples) - 1) )



#######################################################################################################

## struct: feature value
class feature_value:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value


class Data_Point(object):
    ## constructor
    def __init__(self, label=None, start=None, length=None):
        self.label = label
        self.start = start
        try:
            self.length = float(length)
        except TypeError:
            self.length = None
       
        self.features = list()
        self.invalid = False
        
        
    def add_feature(self, name, type, value):
        self.features.append( feature_value(name, type, value) )
        
        
    ## returns tuple of all values
    def get_values(self):
        return [ x.value for x in self.features ]

    ## returns "get_values()" converted as strings
    def get_values_str(self):
        return [str(x) for x in self.get_values() ]
        
    def get_data_description(self):
        names = [ "\t" + x.name for x in self.features ]
        types = [ "\t" + x.type for x in self.features ]
        dim = len(names)
        
        out = list()
        out.append("Activity" + "".join(names))
        out.append("discrete" + "".join(types))
        out.append("class" + "\t"*dim)
        out.append("")
        
        return "\n".join(out)

    def __str__(self):
        return ", ".join(self.get_values_str())
        


#######################################################################################################


class Recording_Part(object):
    def __init__(self):
        self.units = None
        self.windows = None
        self.calibration_info = None
    
class Window(object):
    def __init__(self, units):
        self.units = units
        self.labels = Counter([x.label for x in units])

#        self.invalid = False


    def get_start(self):
        return self.units[0].start
        
    def get_length(self):
        try:
            return float(self.units[-1].start + self.units[-1].length - self.units[0].start)
        except IndexError:
            return 0.0
        
        
    def get_common_label(self, off_by_max=0):
        l = self.labels.most_common(1)[0]
        
        ## OK: return most common label
        if ( l[1] >= len(self.units) - off_by_max ):
            return l[0]
        ## ERR: mixed labels --> INVALID
        else:
            return "INVALID (" + str(l[0]) + ": " + str(l[1]) + ")"
            

    def get_values(self):
        return [unit.get_values() for unit in self.units]

    def get_values_flat(self):
        return list(itertools.chain(*self.get_values()))
        
#    def get_means(self):
#        try:
#            return self.means
#        except AttributeError:
#            self.means = [unit.calc_mean() for unit in self.units]
#            return self.means

