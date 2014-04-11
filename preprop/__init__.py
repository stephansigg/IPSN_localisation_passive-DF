#!/usr/bin/python
# -*- coding: utf-8 -*-

import Storage_Classes
import Data_Classes
import Data_Grouping
import Pcap_Parser
import Visualization
import Features
import Orange_Export
#import Annotation
import Input

import os.path
import cPickle as pickle

from multiprocessing import Pool


## constants
#PLOT_BASE_DIR = "/home/mario/Wifi/Recordings/Plots/session2"
#ORANGE_BASE_DIR = "/home/mario/Wifi/Recordings/Orange/session2"
#PACKETS = 100000
#PACKETS = 1000
PACKETS = -1
USE_PCAP_CACHE = True
PICKLE_FEATURES = True


## display AP which sent most packets
def get_biggest_ap(senders, ssid=None):
    ## find biggest
    max_s = Storage_Classes.Sender()
    for addr in senders:
        s = senders[addr]
        if ( s.type == Storage_Classes.Sender.TYPE.AP ):
            # ssid filter
            if ( ssid and s.ssid != ssid ):
                continue
            
            if ( len(s.samples) > len(max_s.samples) ):
                max_s = s

    return max_s



## creates a dir if nescessary
def prepare_dir(path):
    ## BRANCH: ok, dir exists
    if ( os.path.isdir(path) ):
        return
        
    ## BRANCH: not existant --> create dir
    ##  --> will throw OSError if fails to create dir
    if ( not os.path.exists(path) ):
        os.makedirs(path)
        


## for multiprocessing
def parse_one_file(input_data):
    # looking for cached results
    cache_filename = input_data.infile + '.cache'
    
    ## BRANCH: parsed infile already cached
    if ( USE_PCAP_CACHE and os.path.isfile(cache_filename) ):
        print "Reading cache:", cache_filename
        pickle_input = open(cache_filename, 'rb')
        senders = pickle.load(pickle_input)
        pickle_input.close()
    
    ## BRANCH: no cache
    else:
        ## * parse pcap file *
        senders = Pcap_Parser.parse(input_data.infile, PACKETS)  # 100000
    
        ## caching parser results
        if ( USE_PCAP_CACHE ):
            pickle_output = open(cache_filename, 'wb')
            pickle.dump(senders, pickle_output, pickle.HIGHEST_PROTOCOL)
            pickle_output.close()



    ##
#    types = (   Storage_Classes.Sender.TYPE.AP, \
#                Storage_Classes.Sender.TYPE.STATION, \
#                Storage_Classes.Sender.TYPE.UNKNOWN)
    types = (   Storage_Classes.Sender.TYPE.AP, )
            
#    ## FIXME at the moment "s.show(addr)" is important for proper functionality
    for t in types:
        for addr in senders:
            s = senders[addr]
            if ( s.type == t ):
#                s.show(addr)
                s.set_addr(addr)


    
    ## Visualization
#        Visualization.show_biggest_ap(senders)

    ## Units
    sender = get_biggest_ap(senders)
#    sender = get_biggest_ap(senders)
    print
    print "Using:"
    sender.show()

    # window sizes
#    UNIT_WINDOW = 0.1
    UNIT_WINDOW = 1.0
    DATA_POINT_WINDOW = 6.0
#    DATA_POINT_WINDOW = 5.0

#    SKIP_FRONT = 20
    SKIP_FRONT = 0
    
    OVERLAPPING = True
    
    
    ## Data Grouping ##
    units = Data_Grouping.build_units(sender, input_data.annotation, UNIT_WINDOW, SKIP_FRONT)
    print "created units:", len(units), "(" + str(len(units) * units[0].length) + "s)"
    parts = Data_Grouping.separation(units)

    part = parts[0]    
    part.windows = Data_Grouping.windowing(part, DATA_POINT_WINDOW, OVERLAPPING)
    part.features = Features.calculate_features(part)

#    ## XXX
#    for x in units:
#        print x.show()

    ## XXX    
#    for x in part.features:
#        if ( not x.invalid ):
#            print "|||", x
    print "new features:", len(part.features)
    


    

    ## plot into file
    prepare_dir(input_data.group.plot_base_dir)
    filename = input_data.group.plot_base_dir + "/" + os.path.splitext(os.path.basename(input_data.infile))[0] + ".pdf"
    
    
    ## XXX do pickles in the plot dir, too
    if ( PICKLE_FEATURES ):
        pick_path = input_data.group.plot_base_dir + "/" + os.path.splitext(os.path.basename(input_data.infile))[0] + "_features.pickle"
        pickle_output = open(pick_path, 'wb')
        pickle.dump(part, pickle_output, pickle.HIGHEST_PROTOCOL)
        pickle_output.close()

    
##    xlim = [units[0].start, 200]
#    xlim = [20, 200]
#    ylim = [-75, -15]
#    print ">>>>>>> Plotting into:", filename
#    Visualization.plot_mean_and_variance_into_file(units, xlim, ylim, filename)
#    Visualization.plot_min_max_rssi(units, xlim, ylim, filename)


    ## plot data_points into file
#    xlim = [0, 350]
#    ylim = [-5, 10]
    xlim = None
    ylim = None
#    Visualization.plot_data_points(data_points, xlim, ylim, filename)
#    Visualization.plot_data_points(merged_points, xlim, ylim, filename, invalid_points = invalid_points)
    Visualization.plot_data_points(part.features, xlim, ylim, filename)
#    ylim = [0, 2]
#    Visualization.plot_data_points(level_points, xlim, ylim, filename)

    ## XXX visualize raw rssi data (interactive)
    ##   -- BE CAREFUL: this will not work in parallel processing mode
    Visualization.plot_raw_rssi(sender)
    
    print "-----------------------------------------------------------------------"
    
    
    header = None
#    header = \
#'''Activity\tmean\tvariance\tdistance\tdiff\tsign\tlevels
#discrete\tcontinuous\tcontinuous\tcontinuous\tcontinuous\tdiscrete\tcontinuous
#class\t\t\t\t\t
#'''

#    orange_data = Orange_Export.Data_Collection(merged_points, header)
    orange_data = Orange_Export.Data_Collection(part.features, None)

    ## return
#    return units
    return orange_data


## Export to Orange
def export(group):
    orange_dir = os.path.dirname(group.orange_file)
    prepare_dir(orange_dir)
    
#    exporter = Orange_Export.Unit_Exporter(group.orange_file)
    exporter = Orange_Export.Data_Point_Exporter(group.orange_file)

    for x in group.results:
        exporter.write(x)
        
    exporter.close()
    del exporter


### main ###
if __name__ == "__main__":

    

    try:
        ## input files
        files, groups = Input.get_input()
#        files, groups = Input.get_input_ah()


        ## process in parallel
#        pool = Pool(processes=2)
#        pool = Pool()
#        results = pool.map(parse_one_file, files)

#        ## XXX non-parallel, to be able to use interactive plots
        results = list()
        for f in files:
            results.append(parse_one_file(f))
        
        ## grouping the results
        print
        for i in xrange(len(files)):
            print "Group:", files[i].group.name, "-- adding:", files[i].infile
            files[i].group.add_result(results[i])

        ## export to Orange
        for group in groups:
            export(group)
        
        
        
        

                
    except KeyboardInterrupt:
        print
        print "bye."
        
