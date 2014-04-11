# -*- coding: utf-8 -*-

import Storage_Classes



## stores a list of data_points and a tab-file header
##   (auto creates header from data_points, if not explecitly given)
class Data_Collection(object):
    def __init__(self, data_points, header=None):
        self.data_points = data_points

        ## BRANCH: write custom header        
        if ( header ):
            self.header = header
            
        ## BRANCH: auto-create header
        else:
            self.header = data_points[0].get_data_description()



## Exporter for Orange tab-files
##   (base class)
class Tab_Exporter:
    def __init__(self, outfile):
        self.outfile = open(outfile, "w")
        self.written_header = False
        
#        self.write_header()


    def set_header(self, header):
        ## BRANCH: not written yet --> write
        if ( not self.written_header ):
            self.written_header = header
            self.outfile.write(header)
            
        ## BRANCH: already written --> check consistence
        else:
            assert( self.written_header == header )
            
           
    def write(self, data):
        # do override this!
        assert(False)

    def close(self):
        self.outfile.close()
        self.outfile = False



## Tab_Exporter subclass for writing units (DEPRECATED)
##   (write mean and variance from units)
class Unit_Exporter(Tab_Exporter):
    def write_header(self):
        self.outfile.write("Activity\tmean\tvariance\n")
        self.outfile.write("discrete\tcontinuous\tcontinuous\n")
        self.outfile.write("class\t\t\n")

    def write(self, units):
        if ( not self.written_header ):
            self.write_header()
            self.written_header = True
            
        for unit in units:
#            if ( unit.start >= 20 and unit.start < 200 and unit.get_sampling_rate() > 80 ):
            if ( unit.get_sampling_rate() > 80 ):
                self.outfile.write(unit.label + "\t" + str(unit.calc_mean()) + "\t" + str(unit.calc_variance()) + "\n")
                
#            self.outfile.write(unit.label + "\t" + str(unit.calc_mean()) + "\t" + str(unit.calc_variance()) + "\n")



## Tab_Exporter subclass for writing generic data_points
##   (data is expected to be an instance of Data_Collection)
class Data_Point_Exporter(Tab_Exporter):
    def write(self, data_collection):
        self.set_header(data_collection.header)

        for point in data_collection.data_points:
            if ( not "INVALID" in point.label):
                self.outfile.write(point.label + "\t" + "\t".join(point.get_values_str()) + "\n")
            
            
