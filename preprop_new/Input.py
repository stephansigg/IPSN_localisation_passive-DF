# -*- coding: utf-8 -*-

from Input_Classes import *

def get_input():
        files = list()
        groups = list()
        
#/## Session1   -- ignore!
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session1/ruhe1.pcap", "sitting") )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session1/laufen1.pcap", "walking") )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session1/stehen1.pcap", "standing") )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session1/ruhe2.pcap", "sitting") )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session1/laufen2.pcap", "walking") )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session1/stehen2.pcap", "standing") )


## Session2
        # 2.1
        session2_1 = Group("Session2_1")
        session2_1.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/session2"
        session2_1.orange_file = "/home/mario/Wifi/Recordings/Orange/session2/data1.tab"
        groups.append(session2_1)
        
        files.append( Input_Data("/home/mario/Wifi/Recordings/session2/empty1.pcap", "empty", session2_1) )
        files.append( Input_Data("/home/mario/Wifi/Recordings/session2/reading1.pcap", "reading", session2_1) )
        files.append( Input_Data("/home/mario/Wifi/Recordings/session2/typing1.pcap", "typing", session2_1) )


        # 2.2
        session2_2 = Group("Session2_2")
        session2_2.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/session2"
        session2_2.orange_file = "/home/mario/Wifi/Recordings/Orange/session2/data2.tab"
        groups.append(session2_2)

        files.append( Input_Data("/home/mario/Wifi/Recordings/session2/empty4.pcap", "empty", session2_2) )
        files.append( Input_Data("/home/mario/Wifi/Recordings/session2/reading4.pcap", "reading", session2_2) )
        files.append( Input_Data("/home/mario/Wifi/Recordings/session2/typing4.pcap", "typing", session2_2) )


### Session3
#        session3 = Group("Session3")
#        session3.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/session3"
#        session3.orange_file = "/home/mario/Wifi/Recordings/Orange/session3/data1.tab"
#        groups.append(session3)

#        files.append( Input_Data("/home/mario/Wifi/Recordings/session3/empty3-1.pcap", "empty", session3) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session3/reading3-1.pcap", "reading", session3) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session3/typing3-1.pcap", "typing", session3) )


### Session4
#        session4 = Group("Session4")
#        session4.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/session4"
#        session4.orange_file = "/home/mario/Wifi/Recordings/Orange/session4/data1.tab"
#        groups.append(session4)

#        files.append( Input_Data("/home/mario/Wifi/Recordings/session4/empty4-1.pcap", "empty", session4) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session4/reading4-1.pcap", "reading", session4) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session4/typing4-1.pcap", "typing", session4) )



### Session5_Antonia1
#        session5 = Group("Session5_Antonia1")
#        session5.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/session5_antonia1"
#        session5.orange_file = "/home/mario/Wifi/Recordings/Orange/session5_antonia1/data1.tab"
#        groups.append(session5)

#        files.append( Input_Data("/home/mario/Wifi/Recordings/session5_antonia1/empty5_1.pcap", "empty", session5) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session5_antonia1/reading5_1.pcap", "reading", session5) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session5_antonia1/typing5_1.pcap", "typing", session5) )
#    
#    
### Session6
#        session6 = Group("Session6")
#        session6.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/session6"
#        session6.orange_file = "/home/mario/Wifi/Recordings/Orange/session6/data1.tab"
#        groups.append(session6)

#        files.append( Input_Data("/home/mario/Wifi/Recordings/session6/empty6-1.pcap", "empty", session6) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session6/reading6-1.pcap", "reading", session6) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session6/typing6-1.pcap", "typing", session6) )


### Session7_Antonia2
#        session7 = Group("Session7_Antonia2")
#        session7.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/session7_antonia2"
#        session7.orange_file = "/home/mario/Wifi/Recordings/Orange/session7_antonia2/data1.tab"
#        groups.append(session7)

#        files.append( Input_Data("/home/mario/Wifi/Recordings/session7_antonia2/empty7-1.pcap", "empty", session7) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session7_antonia2/reading7-1.pcap", "reading", session7) )
#        files.append( Input_Data("/home/mario/Wifi/Recordings/session7_antonia2/typing7-1.pcap", "typing", session7) )

        # return
        return files, groups







## ----------------------------------------------------------------------------------------------------------------- ##







def get_input_ah():
        files = list()
        groups = list()

### Aufstehen Hinsetzen Test2
#        ah2 = Group("AH_Test2")
#        ah2.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Test2"
#        ah2.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/test2.tab"
#        groups.append(ah2)
#        
##        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen_tests/test1.pcap", "TESTING", ah1, annotation="/tmp/mouse.csv") )
##        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen_tests/annotation_test_no_activities.pcap", None, ah1, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen_tests/mouse.csv") )
#        
#        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen_tests/test2.pcap", None, ah2, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen_tests/test2_ann.csv") )


### Aufstehen Hinsetzen Test3
#        ah3 = Group("AH_Test3")
#        ah3.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Test3"
#        ah3.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/test3.tab"
#        groups.append(ah3)
#        
#        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen_tests/test3.pcap", None, ah3, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen_tests/test3_ann.csv") )
        

## ----------------------------------------------------------------------- ##

        
## Aufstehen Hinsetzen Day2 - 1
        ah21 = Group("AH_Test21")
        ah21.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Day2"
        ah21.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/Day2/rec1.tab"
        groups.append(ah21)
        
        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day2/rec1.pcap", None, ah21, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day2/rec1_ann.csv") )


## Aufstehen Hinsetzen Day2 - 2
        ah22 = Group("AH_Test22")
        ah22.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Day2"
        ah22.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/Day2/rec2.tab"
        groups.append(ah22)
        
        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day2/rec2.pcap", None, ah22, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day2/rec2_ann.csv") )



### Aufstehen Hinsetzen Day3 - 1
#        ah31 = Group("AH_Test31")
#        ah31.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Day3"
#        ah31.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/Day3/rec1.tab"
#        groups.append(ah31)
#        
#        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day3/rec1.pcap", None, ah31, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day3/rec1_ann.csv") )

### Aufstehen Hinsetzen Day3 - 2
#        ah32 = Group("AH_Test32")
#        ah32.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Day3"
#        ah32.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/Day3/rec2.tab"
#        groups.append(ah32)
#        
#        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day3/rec2.pcap", None, ah32, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day3/rec2_ann.csv") )


### Aufstehen Hinsetzen Day3 - 4
#        ah34 = Group("AH_Test34")
#        ah34.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Day3"
#        ah34.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/Day3/rec4.tab"
#        groups.append(ah34)
#        
#        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day3/rec4.pcap", None, ah34, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day3/rec4_ann.csv") )


## Aufstehen Hinsetzen Day4 - 1
        ah41 = Group("AH_Test41")
        ah41.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Day4"
        ah41.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/Day4/rec1.tab"
        groups.append(ah41)
        
        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day4/rec1.pcap", None, ah41, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day4/rec1_ann.csv") )


# Aufstehen Hinsetzen Day4 - 2
        ah42 = Group("AH_Test42")
        ah42.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Day4"
        ah42.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/Day4/rec2.tab"
        groups.append(ah42)
        
        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day4/rec2.pcap", None, ah42, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen/day4/rec2_ann.csv") )


## Aufstehen Hinsetzen Clean1 - 1
        ah_clean11 = Group("AH_Clean11")
        ah_clean11.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Clean1"
        ah_clean11.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/Clean1/rec1.tab"
        groups.append(ah_clean11)
        
        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen/clean1/rec1.pcap", None, ah_clean11, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen/clean1/rec1_ann.csv") )


## Aufstehen Hinsetzen Clean1 - 2
        ah_clean12 = Group("AH_Clean12")
        ah_clean12.plot_base_dir = "/home/mario/Wifi/Recordings/Plots/AH/Clean1"
        ah_clean12.orange_file = "/home/mario/Wifi/Recordings/Orange/AH/Clean1/rec2.tab"
        groups.append(ah_clean12)
        
        files.append( Input_Data("/home/mario/Wifi/Recordings/aufstehen_hinsetzen/clean1/rec2.pcap", None, ah_clean12, annotation="/home/mario/Wifi/Recordings/aufstehen_hinsetzen/clean1/rec2_ann.csv") )



        # return
        return files, groups
