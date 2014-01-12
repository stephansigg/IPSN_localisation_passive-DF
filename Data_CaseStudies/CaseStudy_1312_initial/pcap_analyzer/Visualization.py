# -*- coding: utf-8 -*-

import Storage_Classes
import matplotlib.pyplot as plt
import Features

## display AP which sent most packets
def show_biggest_ap(senders):
    ## find biggest
    max_s = Storage_Classes.Sender()
    for addr in senders:
        s = senders[addr]
        if ( s.type == Storage_Classes.Sender.TYPE.AP ):
            if ( len(s.samples) > len(max_s.samples) ):
                max_s = s

    ## print        
    print
    print "Biggest sender:"
    max_s.show()

    print "-------------------------------------------------------"
#    max_s.show_data()
    plot_raw_rssi(max_s)


## plot data of one sender
def plot_raw_rssi(sender):
    ## timestamp normalization (TODO be careful when using multi-plots)
    beginning = sender.samples[0].timestamp
    
    x_axis = [sample.get_normalized_timestamp(beginning) for sample in sender.samples]
    y_axis = [sample.rssi for sample in sender.samples]
#    print x_axis, y_axis
    
    plt.plot(x_axis, y_axis)
    plt.show()
    
    
    
    
### plot features ###

### mean
#def plot_mean(units):
#    x_axis = [unit.start for unit in units]
#    y_axis = [unit.calc_mean() for unit in units]

#    plt.plot(x_axis, y_axis)
#    plt.show()

### variance
#def plot_variance(units):
#    x_axis = [unit.start for unit in units]
#    y_axis = [unit.calc_variance() for unit in units]

#    plt.plot(x_axis, y_axis)
#    plt.show()

### mean and variance
#def plot_mean_and_variance_interactive(units):
#    x_axis = [unit.start for unit in units]
#    y_axis_A = [unit.calc_variance() for unit in units]
#    y_axis_B = [unit.calc_mean() for unit in units]

#    plt.plot(x_axis, y_axis_A)
#    plt.plot(x_axis, y_axis_B)
#    plt.show()
#    
### mean an variance into png    
#def plot_mean_and_variance_into_file(units, xlim, ylim, filename):
#    plt.xlim(xlim)
#    plt.ylim(ylim)

#    x_axis = [unit.start for unit in units]
#    y_axis_A = [unit.calc_variance() for unit in units]
#    y_axis_B = [unit.calc_mean() for unit in units]

#    plt.plot(x_axis, y_axis_A)
#    plt.plot(x_axis, y_axis_B)
##    plt.show()
#    plt.savefig(filename)
#    plt.close()


### mean an variance into png    
#def plot_min_max_rssi(units, xlim, ylim, filename):
#    plt.xlim(xlim)
#    plt.ylim(ylim)

#    x_axis = [unit.start for unit in units]
#    y_axis_A = [unit.get_min_value() for unit in units]
#    y_axis_B = [unit.get_max_value() for unit in units]
#    y_axis_C = [unit.calc_mean() for unit in units]

#    plt.plot(x_axis, y_axis_A)
#    plt.plot(x_axis, y_axis_B)
#    plt.plot(x_axis, y_axis_C)
##    plt.show()
#    plt.savefig(filename)
#    plt.close()

    
    
## plot data points
##   @param dims: list dimensions to plot (default: all)
def plot_data_points(data_points, xlim, ylim, filename, dims=None, invalid_points = tuple()):
    if ( xlim ):
        plt.xlim(xlim)
    if ( ylim ):
        plt.ylim(ylim)

    # if no dims are given, show all dimensions
    if ( not dims ):
        dims = range(len(data_points[0].get_values()))
    
    ## valid points
    x_axis = [p.start for p in data_points]
    for i in dims:
        y_axis = [p.get_values()[i] for p in data_points]
        plt.plot(x_axis, y_axis)
        
    ## invalid points
    for x in invalid_points:
        plt.axvspan(x.start, x.start+x.length, facecolor='r', alpha=0.5)
        
#    plt.show()   ## XXX testing..
    if ( filename ):
        plt.savefig(filename)
    plt.close()


## XXX just some quick changes to handle windows XXX not working!!
def plot_data_pointsXX(data_points, xlim, ylim, filename, dims=None, invalid_points = tuple()):
    if ( xlim ):
        plt.xlim(xlim)
    if ( ylim ):
        plt.ylim(ylim)

#    # if no dims are given, show all dimensions
#    if ( not dims ):
#        dims = range(len(data_points[0].get_values()))
    
    ## valid points
    x_axis = [p.get_start() for p in data_points]
    y_axis = [p.get_values() for p in data_points]
    plt.plot(x_axis, y_axis)
        
#    ## invalid points
#    for x in invalid_points:
#        plt.axvspan(x.start, x.start+x.length, facecolor='r', alpha=0.5)
        
#    plt.show()   ## XXX testing..
    if ( filename ):
        plt.savefig(filename)
    plt.close()



## experimental...
def plot_window(window, ylim=None):
    if ( ylim ):
        plt.ylim(ylim)
    
    x_axis = range(len(window))
    y_axis = window
    
    plt.plot(x_axis, y_axis)
    plt.show()
#    plt.close()

