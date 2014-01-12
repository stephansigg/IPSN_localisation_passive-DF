# -*- coding: utf-8 -*-

import Storage_Classes
import Data_Classes

import math
import numpy
from collections import deque, Counter

## just for testing
import Visualization


### multi purpose calculater functions ###

## calc mean
def calc_mean(values, select = (lambda x : x)):
    sum = 0
    
    for v in values:
        sum += select(v)
        
    return float(sum) / len(values)

## calc median
def calc_median(values, select = (lambda x : x)):
    sum = 0
    
    V = [select(v) for v in values]
    
    return numpy.median(V)


## calc variance    ## ---> in fact this seems to be the "Sample standard deviation"
def calc_variance(values, select = (lambda x : x)):
#    ## empty
#    if ( len(self.samples) < 2 ):
#        return 0

    mean = calc_mean(values, select)
    sum = 0
    
    for v in values:
        sum += (select(v) - mean) ** 2
        
    return math.sqrt( sum / (len(values) - 1) )


## calc distance (mario's personal feature..)
def calc_distance(values, select = (lambda x : x)):
    sum = 0
    for i in range(len(values)-1):
        sum += abs(select(values[i]) - select(values[i+1]))

    return (float(sum) / len(values))

## calc distance2 (variant of mario's personal feature..)
def calc_distance2(values, select = (lambda x : x)):
    sum = 0
    for i in range(len(values)-1):
        sum += (select(values[i]) - select(values[i+1])) ** 2

    return math.sqrt(float(sum) / len(values))

## calc trend
def calc_trend(values, select = (lambda x : x)):
    sum = 0
    for i in range(len(values)-1):
        sum += numpy.sign(select(values[i]) - select(values[i+1]))

    return sum

## calc minimum
def calc_min(values, select = (lambda x : x)):
    sum = 0
    for i in range(len(values)-1):
        sum += numpy.sign(select(values[i]) - select(values[i+1]))

    return sum



## calculates how many units have a sampling rate greater than "desired_sampling_rate" (in Hertz)
def analyze_sampling_rate(units, desired_sampling_rate):
    good = 0
    bad = 0
    
    for unit in units:
        if ( unit.get_sampling_rate() >= desired_sampling_rate ):
            good += 1
        else:
            bad += 1
            
    print
    print "Good:", good
    print "Bad:", bad
    print "--->", good / float(good+bad)
    



#######################################################################################################    


### feature calculation ###

class InvalidWindowException(Exception):
    pass


## variance    
def feature_variance(cal_means):
    ## * calculate variance *
    try:
        variance = calc_variance(cal_means)
    except ZeroDivisionError:
        raise InvalidWindowException()
                
    return variance

    
## count levels
def feature_levels(window):
    v = window.get_values_flat()
    levels = len(set(v))
    
    return levels


def feature_test(window):
    return " ".join([str(u.start) for u in window.units])



def calculate_features(part):
    data_points = list()

    ## calc features for every window
    for window in part.windows:
        ## preprocessing & calibration
        means = [unit.calc_mean() for unit in window.units]
        cal_means = [-m + part.calibration_info for m in means]
        cal_means = means  ## <--- XXX deactivate calibration

        ## init data_point
        p = Data_Classes.Data_Point()
        p.start = window.get_start()
        p.length = window.get_length()
        p.label = window.get_common_label(off_by_max=1)
        
        if ( "INVALID" in p.label ):
            p.invalid = True

            
        ## feature calculation
        try:
#            f1 = feature_test(window, cal)
#            print "///", f1

#            p.add_feature("mean", "continuous", calc_mean(cal_means, lambda x: abs(x)))   # <--- would be strange...
            p.add_feature("mean", "continuous", calc_mean(cal_means))
            p.add_feature("median", "continuous", calc_median(cal_means))
            p.add_feature("variance", "continuous", feature_variance(cal_means))
            p.add_feature("distance", "continuous", calc_distance(cal_means))
            p.add_feature("diff", "continuous", cal_means[0] - cal_means[-1])
            p.add_feature("sign", "discrete", numpy.sign(cal_means[0] - cal_means[-1]))
            p.add_feature("levels", "continuous", feature_levels(window))
            p.add_feature("trend","continuous", calc_trend(cal_means))
	    p.add_feature("distance2","continuous", calc_distance2(cal_means))
	    p.add_feature("distance", "continuous", calc_distance(cal_means))
            
            
        except InvalidWindowException:
            p.invalid = True
            
            ## XXX testing..
            print "||| WINDOW INVALID"
            assert(False)
            
        data_points.append(p)
        
    return data_points
    
