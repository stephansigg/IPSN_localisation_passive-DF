'''
Created on Jan 28, 2014

@author: moby
'''
from __future__ import division
import Pcap_Parser
import numpy as np
#import Storage_Classes
#import Data_Classes
#import Data_Grouping
#import Orange_Export
import sys
import time
import os.path
import cPickle
from collections import deque
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

# most important fields for feature computation and class_val training are self.data_table (class Orange.data.Table) and self.domain_list
# if you want to add new features to data_table, first extend the domain field in the __init__() method (see comments in code below)
# in order to compute the values of your features and to add them to data_table, create a new class method and call it within the main() method 
class Gen:
    def __init__(self):
	# gui related code
        builder = gtk.Builder()
        builder.add_from_file("position_recognition.glade")
	hbox=builder.get_object("box4")
	self.dropbox=gtk.combo_box_entry_new_text()
	self.dropbox.append_text("corner1")
	self.dropbox.append_text("corner2")
	self.dropbox.append_text("corner3")
	self.dropbox.append_text("corner4")
	self.dropbox.set_active(0)
	self.dropbox.child.connect('changed', self.dropbox_changed)
	hbox.pack_start(self.dropbox)
	hbox.reorder_child(self.dropbox,7)
        builder.connect_signals(self)
	builder.get_object("pos_rec").show_all()
	self.scrll_adj=builder.get_object("adjustment1")
	self.entry1=builder.get_object("entry1")
	self.entry2=builder.get_object("entry2")
	self.entry3=builder.get_object("entry3")
	#self.pcap_file=""
	#self.data_file=""
	#self.class_file=""
	self.file_name=""
	self.class_val=self.dropbox_entry="corner1"
	# define the domain of data_table
	rssi=Orange.feature.Continuous("rssi")
	# to add continuous features, e.g. mean or variance, just copy
	# the above line and change the feature name
	mean=Orange.feature.Continuous("mean")
	var=Orange.feature.Continuous("var")
	spec_e=Orange.feature.Continuous("spec_e")
	#time1=Orange.feature.Continuous("time1")
	#time2=Orange.feature.Continuous("time2")
	self.clss_list=["corner1","corner2","corner3","corner4"]
	clss=Orange.feature.Discrete("corner",values=self.clss_list)
	# then add your features to domain_list
	# note: add your feutures at the beginning of the list!
	self.domain_list=[mean,var,spec_e,rssi,clss]
	self.f_ind={"mean":0,"var":1,"spec_e":2,"time1":3,"time2":4,"rssi":5,"clss":6}
	self.domain=Orange.data.Domain(self.domain_list)
	self.data_table_orange=Orange.data.Table(self.domain)
	self.data_table=[]
	self.textout=builder.get_object("textview1").get_buffer()
        self.closed=False
	self.parsing=False
	self.classifying=False
	self.clss_count=dict(zip(self.clss_list,[0]*len(self.clss_list)))
	self.w_size=30
	self.window_head=0
	self.window=deque()
	self.window_filled=False
	self.classifier=None
	self.dist_dict={"corner1":(200,10),"corner2":(2000,10),"corner3":(70,10),"corner4":(500,40)}
	self.size=10
	self.data=[[0]*7]*self.size



    def print_txt(self,text):
	self.textout.insert(self.textout.get_end_iter(),text+'\n')	
    def dropbox_changed(self,entry):
	self.dropbox_entry=entry.get_text()

    def on_pos_rec_destroy(self,widget):
        self.closed=True


    def set_file_name(self,entry_num):
	entry_dict={1:self.entry1,2:self.entry2,3:self.entry3}
	#file_dict={1:self.pcap_file,2:self.data_file,3:self.class_file}
	name_dict={1:"pcap",2:"data table",3:"classifier"}
	f=entry_dict[entry_num].get_text()
	if os.path.isfile(f):
		self.file_name=f
		if entry_num==1:
		      fl=open('flag_'+self.file_name,'w')
		      fl.write("old\n")
		      fl.close()
		#self.print_txt("test"+f)
		return True
	else:
		self.print_txt("Given "+name_dict[entry_num]+"-file doesn't exist. Please enter a valid file name.")
		return False	


    def on_button1_clicked(self,widget):
	if self.parsing:
		widget.set_label("start parsing")
		self.parsing=False
	else:
		
		if self.set_file_name(1):
			try:
				self.set_class_val()
				widget.set_label("stop parsing")
				self.parsing=True
			except Exception:
				print "invalid class_val"		
				self.print_txt("invalid class_val")			
		

    def on_button2_clicked(self,widget):
	if not self.parsing:
		try:
			self.set_class_val()

		except Exception:
			print "invalid class_val"		
			self.print_txt("invalid class_val")

    def on_button3_clicked(self,widget):
	if not self.classifying:
		if self.classifier==None:
			if len(self.data_table)>0:
				self.create_classifier()
		if self.classifier==None:
			self.print_txt("no classifier available!")
		elif self.set_file_name(1):
			#self.print_txt("mark")
			self.window_filled=False
			self.window_head=-1
			self.window=None
			self.clss_count=dict(zip(self.clss_list,[0]*len(self.clss_list)))
			widget.set_label("stop classification")	
			self.data_table=[]
			self.classifying=True
			self.parsing=True
	else:
			widget.set_label("start classification")
			self.classifying=False
			self.parsing=False
			self.print_txt("classification stopped\nready...")						
			self.data_table=[]
    def on_button4_clicked(self,widget):
	if self.set_file_name(3):
		f=open(self.file_name,'r')
		self.classifier=cPickle.load(f)
		f.close()
		self.print_txt("classifier successfully loaded")

    def on_button5_clicked(self,widget):
	if self.set_file_name(3):
		f=open(self.file_name,'w')
		cPickle.dump(self.classifier,f)
		f.close()
		self.print_txt("classifier successfully saved")

    def on_button6_clicked(self,widget):
	if self.set_file_name(2):
		f=open(self.file_name,'r')
		self.data_table.extend(cPickle.load(f))
		f.close()
		self.print_txt("data table successfully appended")

    def on_button7_clicked(self,widget):
	if self.set_file_name(2):
		f=open(self.file_name,'w')
		cPickle.dump(self.data_table,f)
		f.close()
		self.print_txt("data table successfully saved")

    def on_button8_clicked(self,widget):
	self.data_table=[]
	self.print_txt("data table cleared")

    def create_classifier(self):
	i_t1=self.f_ind["time1"]
	i_t2=self.f_ind["time2"]
	data=map(lambda e:e[:i_t1]+e[i_t2+1:],self.data_table)
	self.data_table_orange=Orange.data.Table(self.domain,data)
	self.classifier=Orange.classification.knn.kNNLearner(self.data_table_orange,k=10)
	self.print_txt("classifier created")

    def on_button9_clicked(self,widget):
	self.create_classifier()



    def on_textbuffer1_changed(self,widget):
	self.scrll_adj.set_value(self.scrll_adj.get_upper())


    def set_class_val(self):
	entry=self.dropbox_entry
	if entry in self.clss_list:
		self.class_val=entry
	elif entry=="":
		raise Exception()
	else:
		self.class_val=entry
		self.clss_list.append(entry)
		clss=Orange.feature.Discrete("corner",values=self.clss_list)
		self.domain_list.pop()
		self.domain_list.append(clss)
		self.domain=Orange.data.Domain(self.domain_list)
		#self.data_table=Orange.data.Table(self.domain,self.data_table)
		#self.data_table_orange=self.data_table_orange.translate(self.domain)
		self.dropbox.append_text(entry)
		self.dropbox.set_active(len(self.clss_list)-1)

    def get_max_clss(self,clss_count):
	return reduce(lambda x,y: x if x[1]>y[1] else y,clss_count.items())[0]


    def spectral_energy(self,rssi_list):
	fft=np.fft.fft(rssi_list)
	fft_sq=map(lambda x:x**2,fft)
	denominator=np.sum(fft_sq)
	return np.sum(map(lambda x:(x/denominator)**2,fft_sq))

    def set_features(self):
	rssi=[e[self.f_ind["rssi"]] for e in self.window]
	mean=np.mean(rssi)
	var=np.var(rssi)
	spec_e=self.spectral_energy(rssi)
	head=self.window.pop()
	head[self.f_ind["mean"]]=mean
	head[self.f_ind["var"]]=var
	head[self.f_ind["spec_e"]]=spec_e
	return head


    def push_window(self):
	#head_old=self.window.pop()
	#self.window.push(head_old)
	i_t1=self.f_ind["time1"]
	i_t2=self.f_ind["time2"]
	i_c=self.f_ind["clss"]
	self.print_txt("mark")
	while self.window_head<len(self.data_table)-1:
		
		self.window_head+=1
		head_new=self.data_table[self.window_head]
		tale=self.window.popleft()
		##### call feuture computation here
		##### set all feutures in head_new
		self.window.append(head_new)
		head_new=self.set_features()
		if self.classifying:
			instance=Orange.data.Instance(self.domain,head_new[:i_t1]+head_new[i_t2+1:])
			clss=self.classifier(instance).native()
			head_new[i_c]=clss
			self.clss_count[clss]+=1
			tale_clss=tale[i_c]
			self.clss_count[tale_clss]-=1
			curr_clss=self.get_max_clss(self.clss_count)
			self.print_txt("current class is "+curr_clss)
		else:
			self.data_table[self.window_head]=head_new
		self.window.append(head_new)
		#head_old=head_new




    def fill_window(self):
	l=len(self.data_table)
	ws=self.w_size
	if l>=ws:
		self.window=deque(self.data_table[0:ws])	
		head=self.set_features()		
		self.window.append(head)
		if self.classifying:
			for e in self.window:
				clss=e[self.f_ind["clss"]]
				self.clss_count[clss]+=1
		self.window_filled=True
		self.window_head=ws-1


    # main method
    # once started, it will loop until the GUI is closed
    # call the method for feature computation within this loop 
    def main(self):
	self.print_txt("ready...")
        while not self.closed:
		while (gtk.events_pending()):
			gtk.main_iteration()
            	
		if self.parsing:
			f=open('flag_'+self.file_name,'r')
			flag=f.readline()
			#self.print_txt(flag)
			if "old" in flag:
				#self.generate_data()
				f.close()
				f=open('flag_'+self.file_name,'w')
				f.write("new\n")
				f.close()
				#self.rssi_mean(10)
				
			else:
				f.close()
				time.sleep(0.1)
			



    def generate_data(self):

	param=self.dist_dict[self.class_val]
	mean=param[0]
	var=param[1]
	features_dummy=[0]*(len(self.f_ind)-4)
	
	for i in range(len(self.data)):
		rssi=np.random.normal(mean,var,1)
		self.data[i]=features_dummy+[int(time.time()),0,rssi[0]," "]
		time.sleep(1/self.size)
	f=open(self.file_name,'w')
	cPickle.dump(self.data,f)
	f.close()	
	#print '[%s]' % ', '.join(map(str, self.data))
    
		
      
if __name__ == "__main__":
    pr=Gen()
    pr.main()
