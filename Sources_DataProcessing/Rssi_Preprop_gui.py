'''
Created on Jan 28, 2014

@author: moby
'''
import Pcap_Parser
#import Storage_Classes
#import Data_Classes
#import Data_Grouping
#import Orange_Export
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

# main class

# most important fields for feature computation and classifier training are self.data_table (class Orange.data.Table) and self.domain_list
# if you want to add new features to data_table, first extend the domain field in the __init__() method (see comments in code below)
# in order to compute the values of your features and to add them to data_table, create a new class method and call it within the main() method 
class Pos_Rec:
	def __init__(self):
		# gui related code
		builder = gtk.Builder()
		builder.add_from_file("position_recognition.glade")
		hbox=builder.get_object("box1")
		self.dropbox=gtk.combo_box_entry_new_text()
		self.dropbox.append_text("corner1")
		self.dropbox.append_text("corner2")
		self.dropbox.append_text("corner3")
		self.dropbox.append_text("corner4")
		self.dropbox.set_active(0)
		self.dropbox.child.connect('changed', self.dropbox_changed)
		hbox.pack_start(self.dropbox)
		hbox.reorder_child(self.dropbox,3)
		builder.connect_signals(self)
		builder.get_object("pos_rec").show_all()
		self.entry=builder.get_object("entry1")
		self.pcap_file=self.entry.get_text()
		self.classifier=self.dropbox_entry="corner1"
		# define the domain of data_table
		rssi=Orange.feature.Continuous("rssi")
		# to add continuous features, e.g. mean or variance, just copy
		# the above line and change the feature name
		# e.g. mean=Orange.feature.Continuous("mean")
		time1=Orange.feature.Continuous("time1")
		time2=Orange.feature.Continuous("time2")
		self.clss_list=["corner1","corner2","corner3","corner4"]
		clss=Orange.feature.Discrete("corner",values=self.clss_list)
		# then add your features to domain_list
		# note: add your feutures at the beginning of the list!
		self.domain_list=[time1,time2,rssi,clss]
		self.domain=Orange.data.Domain(self.domain_list)
		self.data_table=Orange.data.Table(self.domain)
		self.textout=builder.get_object("textview1").get_buffer()
		self.closed=False
		self.parsing=False
	def print_txt(self,text):
		self.textout.insert(self.textout.get_end_iter(),text+'\n')	
	
	def dropbox_changed(self,entry):
		self.dropbox_entry=entry.get_text()

	def on_pos_rec_destroy(self,widget):
		self.closed=True

	def on_button1_clicked(self,widget):
		if self.parsing:
			widget.set_label("start parsing")
			self.parsing=False
		else:
			self.pcap_file=self.entry.get_text()
			if os.path.isfile(self.pcap_file):
				try:
					self.set_classifier()
					widget.set_label("stop parsing")
					self.parsing=True
				except Exception:
					print "invalid classifier"
					self.print_txt("invalid classifier")
			else:
				print "file not existing"
				self.print_txt("file not existing")
	
	def on_button2_clicked(self,widget):
		if not self.parsing:
			try:
				self.set_classifier()
			except Exception:
				print "invalid classifier"		
				self.print_txt("invalid classifier")			

	def set_classifier(self):
		entry=self.dropbox_entry
		if entry in self.clss_list:
			self.classifier=entry
		elif entry=="":
			raise Exception()
		else:
			self.classifier=entry
			self.clss_list.append(entry)
			clss=Orange.feature.Discrete("corner",values=self.clss_list)
			self.domain_list.pop()
			self.domain_list.append(clss)
			self.domain=Orange.data.Domain(self.domain_list)
			#self.data_table=Orange.data.Table(self.domain,self.data_table)
			self.data_table=self.data_table.translate(self.domain)
			self.dropbox.append_text(entry)
			self.dropbox.set_active(len(self.clss_list)-1)

	# main method
	# once started, it will loop until the GUI is closed
	# call the method for feature computation within this loop 
	def main(self):
		self.print_txt("ready...")
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
						# call your method here!
					else:
						f.close()
						time.sleep(0.1)
			
	def pcap_to_orange(self):
		data=Pcap_Parser.parse(self.pcap_file)
		mac_list=data.keys()
		mac=mac_list[1]
		features_dummy=[0]*(len(self.domain_list)-4)
		count_packets=0;
		for m in mac_list:
			if len((data[m]).samples)>count_packets:
				count_packets=len((data[m]).samples)
				mac=m
				sender=data[mac]
				sample_list=sender.samples
				entry=[features_dummy+[sample.timestamp[0],sample.timestamp[1],sample.rssi,self.classifier] for sample in sample_list]
				self.data_table.extend(entry)
				#print '[%s]' % ', '.join(map(str, self.data_table))	
			
			if __name__ == "__main__":
				pr=Pos_Rec()
				pr.main()