# -*- coding: utf-8 -*-

import pcapy
import Storage_Classes
from collections import defaultdict

#from scapy.layers.all import *
from scapy.layers.dot11 import Dot11, RadioTap

################################################################

VERBOSE = 1


### auxiliary functions ###

def show_short(p, label):
    if ( VERBOSE >= 1 ):
        ## show
        #print p.num, p.timestamp, p.dot11.addr2, \
              #label, "[" + str(p.dot11.type) + ", " + str(p.dot11.subtype) + "]", \
              #p.get_rssi(), "dBm"
 ###################################################################################
 ### modified: # ETH- 'public': 00:0f:61:5d:5c:01   00:0f:61:4f:3e:e1 / ETH - 'eth':00:0f:61:5d:5c:00
        #if (str(p.dot11.addr2) == '00:0b:0e:83:a5:86'):
	 print p.timestamp, p.get_rssi(), "dBm"  # das time-format hier sind microseconds als kleinste Einheit. Damit ist die letzte Zahl vor dem Komma die Sekunde.
################################################################

### ANALYZE FUNCTIONS ###

def analyze_beacon(p):
    #print p.num, p.timestamp, p.dot11.addr2, "BEACON:", p.get_rssi(), "dBm"
    show_short(p, "BEACON")

#    ## sanity check  ## FIXME won't work!! is this a wrong sanity check..?
#    if ( not p.dot11.addr2 == p.dot11.addr3 ):
#        print
#        print "ERR: BEACON INVALID"
#        p.show()
#        raise Exception("ERR: BEACON INVALID")
#    if ( p.dot11.addr2 == "00:00:00:00:00:00" ):
#        print
#        print "ERR: BEACON INVALID"
#        p.show()
#        raise Exception("ERR: BEACON INVALID")
        
    ## store
    senders[p.dot11.addr2].store(p)



def analyze_regular(p):
    ## some packet types are not correctly dissected
    ##      ---> e.g. Block ACK Req
    ##      ---> TODO (what shall we do with them?)
    if ( not p.dot11.addr2 ):
      #####################################
#####      THIS IS COMPLETELY UNCOMMENTED TO STOP THIS DISSECTION EXCEPTTION !!! (stephan)
      #####################################
        #show_short(p, "<<not recognized>>.")
        #p.show_stephan()
        #show_short(p, "Packet.")
        ##############################
        ##was: show(p.dot11) ... just guessing
        ##############################
        #print
#        dat = raw_input()
        ######################raise Exception("uncorrect dissection exception")
        return
        
        
    ## BRANCH: "no" sender..
    ##    ---> some packets have no proper sender information
    ##    ---> just ignore them!!
    if ( p.dot11.addr2 == "00:00:00:00:00:00" ):
        show_short(p, "<<ignored>>")
        return


    ## BRANCH: regular packet
    else:
        show_short(p, "Packet.")
        
        ## store
        senders[p.dot11.addr2].store(p)



### general analyze function 
###    --> hands packets over to specialized ones
def analyze(p):
    ## Control frames have no useful sender information
    ##    ---> we don't want them. just drop it.
    ## BRANCH: control frames
    try:
        if ( p.dot11.type == 1 ):
            # BRANCH: ACK (sender unclear...)
            if ( p.dot11.subtype == 13 ):
                if ( VERBOSE >= 1 ):
		  macheNix=1
		  ################################################################################################
		  ###modified:
                    #print p.num, "ignoring ACK (1, 13)", p.get_rssi(), "dBm"
		  ################################################################################################
                return
            if ( p.dot11.subtype == 12 ):
                if ( VERBOSE >= 1 ):
		  macheNix=1
		  ################################################################################################
		  ###modified:
                    #print p.num, "ignoring CTS (1, 12)", p.get_rssi(), "dBm"
		  ################################################################################################
                return
            if ( p.dot11.subtype == 8 ):
                if ( VERBOSE >= 1 ):
		  macheNix=1
		  ################################################################################################
		  ###modified:
                    #print p.num, "ignoring Block ACK Req (1, 12)", p.get_rssi(), "dBm"
                  ################################################################################################  
                return

        ## BRANCH: managemet frames
        if ( p.dot11.type == 0 ):
            # BRANCH: BEACON
            if ( p.dot11.subtype == 8 ):
                analyze_beacon(p)
                return

#    elif ( p.dot11.type == 2 ):
#        if ( p.dot11.subtype == 4 ):
#            analyze_regular(p)
#            dat = raw_input()
#            return

    except AttributeError:
        if ( VERBOSE >= 1 ):
            print p.num, "ignoring malformed packet", p.get_rssi(), "dBm"
        return

        
    ## default
    ##   ---> most packets can just be treated the same..    
    analyze_regular(p)
    
#    show(p.dot11)
#    print
#    dat = raw_input()




################################################################

### PCAP READING AND DECODING ###

## TODO do they have to be global?
pcapy_reader = False
packet_num = False
senders = False

def get_next():
    global packet_num
    
    pkt = pcapy_reader.next()
    if ( type(pkt[0]) == type(None)):
        return None
    
    p = Storage_Classes.Packet()
    packet_num += 1
    p.num = packet_num
    
    p.timestamp = pkt[0].getts()
    p.tap = RadioTap()
    p.tap.dissect(pkt[1])
    
    p.dot11 = p.tap.payload
    
    #print "----->", ord(pkt[1][14])
    p.rssi = ord(pkt[1][14]) - 256
    
    return p


### public ###

def parse(file_name, num=100):
    global pcapy_reader
    global senders

    ## init    
    pcapy_reader = pcapy.open_offline(file_name)
    packet_num = 0
    senders = defaultdict(Storage_Classes.Sender)
    
    print "Reading", file_name, "..."
    
    i = 0
    while ( i != num):  ## like a for loop, but e.g. -1 means "to infinity"
        if ( i % 20000 == 0 ):
            print i
        p = get_next()
        
        if ( p == None ):
            print "EOF", i
            break
        
        analyze(p)
        
        i += 1
    #        dat = raw_input()

    ## FIXME how to close this?
    #pcapy.close()
    
    
    ### statictics
    print
    print "----------------------------------------"
    print "Senders:", len(senders)
    ## TODO count total in this module not in the Sender class
    print "used packets:", Storage_Classes.Sender.total ## TODO maybe this shuld also be returned from "parse"

    return senders
    
