'''
Created on Jan 28, 2014

@author: moby
'''
import Pcap_Parser
import Storage_Classes
import Data_Classes
import Data_Grouping
import Orange_Export
import sys
import time
import os.path
import Orange.data
import Orange.feature
try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
except:
	sys.exit(1)

class Pos_Rec:
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("position_recognition.glade")
        builder.connect_signals(self)
	builder.get_object("pos_rec").show_all()
	self.entry=builder.get_object("entry1")
	self.dropbox=builder.get_object("combobox1")
	self.pcap_file=self.entry.get_text()
	self.classifier=self.dropbox.get_active_text()
	rssi=Orange.feature.Continuous("rssi")
	clss=Orange.feature.Discrete("corner",values=["corner1","corner2","corner3","corner4"])
	self.domain=Orange.data.Domain([rssi,clss])
	self.data_table=Orange.data.Table(self.domain)
        self.closed=False
	self.parsing=False

    def on_pos_rec_destroy(self,widget):
        self.closed=True
    def on_button1_clicked(self,widget):
	if self.parsing:
		widget.set_label("start")
		self.parsing=False
	else:
		self.pcap_file=self.entry.get_text()
		if os.path.isfile(self.pcap_file):
			widget.set_label("stop")
			self.parsing=True		
			self.classifier=self.dropbox.get_active_text()
		else:
			print "file not existing"

    def main(self):
        while not self.closed:
		while (gtk.events_pending()):
			gtk.main_iteration()
            	
		if self.parsing:
			f=open('flag_'+self.pcap_file,'r')
			flag=f.readline()
			if flag=="new\n":
				self.pcap_to_orange()
				f.close()
				f=open('flag_'+self.pcap_file,'w')
				f.write("old\n")
				f.close()
			else:
				f.close()
				time.sleep(0.1)




    def pcap_to_orange(self):
        data=Pcap_Parser.parse(self.pcap_file)
        mac_list=data.keys()
        mac=mac_list[1]
    
        count_packets=0;
        for m in mac_list:
           if len((data[m]).samples)>count_packets:
               count_packets=len((data[m]).samples)
               mac=m
        sender=data[mac]
        sample_list=sender.samples
        entry=[[sample.rssi,self.classifier] for sample in sample_list]
        self.data_table=Orange.data.Table(self.domain,entry)	
   
        
    
if __name__ == "__main__":
 #   import sys
 #   pcap_to_orange(sys.argv[1],sys.argv[2],sys.argv[3])
    pr=Pos_Rec()
    pr.main()
