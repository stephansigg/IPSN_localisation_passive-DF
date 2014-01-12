# -*- coding: utf-8 -*-

#from scapy.layers.all import *
from scapy.layers.dot11 import Dot11, RadioTap
from struct import unpack

from collections import deque


## holds one rssi value + meta data
class Sample(object):
    def __init__(self, rssi, timestamp, pkg_type, datarate):
        self.rssi = rssi
        self.timestamp = timestamp
        self.type = pkg_type
        self.datarate = datarate
        
    def show(self):
        print self.timestamp, "\t", self.rssi, "dBm\t\t", "(" + str(self.datarate) + " MBit/s)"

    ## takes another timestamp, calculates the difference and converts the format to float
    ##    (---> looks a little complicated, this is for not loosing precision)
    def get_normalized_timestamp(self, offset):
        gt1 = self.timestamp[0] - offset[0]
        lt1 = self.timestamp[1] - offset[1]
        return gt1 + lt1 / 1000000.0
        
        
    def get_timestamp_as_float(self):
        return self.timestamp[0] + self.timestamp[1] / 1000000.0
        

    ## timediff
    @staticmethod
    def Get_Timediff(earlier, later):
        return later.get_normalized_timestamp(earlier.timestamp)

## struct, stores an dissected packet
class Packet(object):
    TO_DS = 0x1
    FROM_DS = 0x2

    def __init__(self):
        self.timestamp = False
        self.tap = False
        self.dot11 = False
        self.num = False
        self.beacon = False
        self.rssi = False

    ## get the rssi from raw radiotap data
    def get_rssi(self):
#        print
#        print ord(self.tap.notdecoded[-4])
#        print ord(self.tap.notdecoded[6])
#        print
#        for x in self.tap.notdecoded:
#            print ord(x)
#        x = raw_input()
#        return ord(self.tap.notdecoded[-4]) - 256
        return self.rssi

    ## get datarate in Mbit/s
    def get_datarate(self):
        return ord(self.tap.notdecoded[1])/2.0
        
    def get_freq(self):
        return unpack("<h", self.tap.notdecoded[2:4])[0]
        

    ## some classifications ##     
    def is_beacon(self):
        return self.dot11.type == 0 and self.dot11.subtype == 8
    
    #
    def is_to_ds(self):
        return self.dot11.FCfield & Packet.TO_DS
    
    #    
    def is_from_ds(self):
        return self.dot11.FCfield & Packet.FROM_DS
        
    ## TODO not fully tested (just a guess)... --> but looking not bad atm
    #
    def is_sent_from_ap(self):
        return self.is_beacon() or \
                (self.is_from_ds() and not self.is_to_ds())

    ## TODO not fully tested (just a guess)... --> but looking not bad atm
    #
    def is_sent_from_station(self):
        return not self.is_from_ds() and self.is_to_ds()

        
    ## produce some human readable output
    def show(self):
        print
        print "###[ Radio TAP ]###"
        print "RSSI:    ", self.get_rssi(), "dBm"
        print "Datarate:", self.get_datarate(), "Mbit/s"
        print "Freq:    ", self.get_freq(), "MHz"
        print
        print "###[ 802.11 ]###"
        print "  type      =", self.dot11.type
        print "  subtype   =", self.dot11.subtype
        print "  proto     =", self.dot11.proto
        print "  FCfield   =", self.dot11.FCfield
        if ( self.is_from_ds() ):
            print "    (from_ds)"
        if ( self.is_to_ds() ):
            print "    (to_ds)"
        print "  ID        =", self.dot11.ID
        print "  addr1     =", self.dot11.addr1
        print "  addr2     =", self.dot11.addr2
        print "  addr3     =", self.dot11.addr3
        print "  SC        =", self.dot11.SC
        print "  addr4     =", self.dot11.addr4
        
        if ( self.is_sent_from_ap() ):
            print "---> sent from AP"
            
        if ( self.is_sent_from_station() ):
            print "---> sent from STATION"        


    ## produce some useful output for dissected packets
    def show_stephan(self):
            print self.timestamp, self.get_rssi(), "dBm", self.dot11.addr1


## holds rssi data and additional information from one sender
class Sender(object):
    ## enum
    class TYPE:
        UNKNOWN = 0
        AP      = 1
        STATION = -1
        
    total = 0
        
    def __init__(self):
        self.type = Sender.TYPE.UNKNOWN
        self.address = None
        self.samples = deque()
        self.ssid = None
        
        
    ## sets type of this sender to AP or Station
    def set_type(self, t):
        # already set, nothing to do
        if ( self.type == t ):
            return
            
        # not set before, set
        if ( self.type == Sender.TYPE.UNKNOWN ):
            self.type = t
            return
        
        # miss match !!
        #######################
        ##### commented to stop this exception (stephan)
        #####raise Exception("inconsisten type")
	#######################
    # sets ssid name of an AP        
    def set_ssid(self, ssid):
        # already set, nothing to do
        if ( self.ssid == ssid ):
            return
            
        # not set before, set
        if ( self.ssid == None ):
            self.ssid = ssid
            return
        
        # miss match !!
        raise Exception("inconsisten SSID")
        
        
    ## ** stores a new rssi value for this sender **
    ##    ---> and checks about the sender type
    def store(self, p):
        # is ap?
        if ( p.is_sent_from_ap() ):
            self.set_type(Sender.TYPE.AP)
            
            # ssid
            if ( p.is_beacon() ):
                self.set_ssid(p.dot11.payload.payload.info)
 
        
        # is station?    
        if ( p.is_sent_from_station() ):
            self.set_type(Sender.TYPE.STATION)

        ## XX-X
#        if ( p.get_datarate() > 2 ):
#            p.show()
#            xx = raw_input()
        x = Sample(p.get_rssi(), p.timestamp, p.dot11.type, p.get_datarate())
        self.samples.append(x)
        Sender.total += 1

        
    def set_addr(self, addr):
        self.address = addr
    
    ## human readable information about this sender
    ##      ---> to be called in the end
    def show(self, addr=None):
        ## set address
        if ( addr ):
            self.address = addr
            
        ## BRANCH: is AP
        if ( self.type == Sender.TYPE.AP ):
            print "AP", self.address, len(self.samples), "\t\t[" + str(self.ssid) + "]"
            print "Recording length:", Sample.Get_Timediff(self.samples[0], self.samples[-1]), "s"

        ## BRANCH: is station or unknown
        elif ( self.type == Sender.TYPE.STATION ):
            print "STA", self.address, len(self.samples)
            
        else:
            print "<<unknown>>", self.address, len(self.samples)

    ## human readable output of the samples
    def show_data(self):
        for x in self.samples:
            x.show()
            
