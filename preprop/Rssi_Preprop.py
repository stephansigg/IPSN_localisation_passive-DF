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
import GUI


# main class

# most important fields for feature computation and class_val training are self.data_table (class Orange.data.Table) and self.domain_list
# if you want to add new features to data_table, first extend the domain field in the __init__() method (see comments in code below)
# in order to compute the values of your features and to add them to data_table, create a new class method and call it within the main() method 
class Pos_Rec:
    def __init__(self):

	
	

	rssi=Orange.feature.Continuous("rssi")
	max_v=Orange.feature.Continuous("max_v")
	min_v=Orange.feature.Continuous("min_v")
	w_time=Orange.feature.Continuous("w_time")
	mean=Orange.feature.Continuous("mean")
	var=Orange.feature.Continuous("var")
	time1=Orange.feature.Continuous("time1")
	time2=Orange.feature.Continuous("time2")
	#spec_e=Orange.feature.Continuous("spec_e")
	#self.clss_list=["corner1","corner2","corner3","corner4"]
	self.clss_list=[]
	clss=Orange.feature.Discrete("corner",values=self.clss_list)
	self.domain_list=[w_time,max_v,min_v,mean,var,time1,time2,rssi,clss]
	self.mask=[1,1,1,1,1,0,0,1,1]
	self.f_ind={"w_time":0,"max_v":1,"min_v":2,"mean":3,"var":4,"time1":5,"time2":6,"rssi":7,"clss":8}
	self.domain=Orange.data.Domain(self.domain_list)
	self.data_table_orange=Orange.data.Table(self.domain)
	self.data_table=[]
	
        self.closed=False
	self.parsing=False
	self.classifying=False
	self.clss_count=dict(zip(self.clss_list,[0]*len(self.clss_list)))
	self.w_size=30
	self.window_head=0
	self.window=deque()
	self.window_filled=False
	self.classifier=None
	self.GUI=GUI.GUI(self)
	self.class_val=""
	



	



    def mask_entry(self,entry):
	return [ i for i, flag in zip( entry, self.mask ) if flag == 1 ]

	

    def get_time(self,t1,t2,arity):
	res=t1*(10**arity)
	s=str(t2)
	if len(s)>=arity:
	  return res+int(s[:arity])
	else:
	  return res

    def convert_data(self,d_old,f_ind_old):
	not_eq=f_ind_old==self.f_ind
	if not_eq:
		t1_o=f_ind_old["time1"]
		t2_o=f_ind_old["time2"]
		r_o=f_ind_old["rssi"]
		c_o=f_ind_old["clss"]
		t1_n=self.f_ind["time1"]
		t2_n=self.f_ind["time2"]
		r_n=self.f_ind["rssi"]
		c_n=self.f_ind["clss"]
		d_new=[[0]*len(self.f_ind)]*len(d_old)
		for i in range(len(d_old)):
			d_new[i][t1_n]=d_old[i][t1_o]
			d_new[i][t2_n]=d_old[i][t2_o]
			d_new[i][r_n]=d_old[i][r_o]
			#d_new[i][c_n]=d_old[i][c_o]
		l=len(self.data_table)
		self.data_table.extend(d_new)
		if not self.window_filled:
			self.fill_window()
		self.push_window()
		for i in range(len(d_old)):
			self.data_table[i+l][c_n]=d_old[i][c_o]
	return not_eq
	

    def create_classifier(self):

	data=map(lambda e:self.mask_entry(e),self.data_table)
	self.domain=Orange.data.Domain(self.mask_entry(self.domain_list))
	self.data_table_orange=Orange.data.Table(self.domain,data)
	self.classifier=Orange.classification.knn.kNNLearner(self.data_table_orange,k=10)
	self.GUI.print_txt("classifier created")




    def set_class_val(self):
	entry=self.GUI.dropbox_entry
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
		self.GUI.dropbox.append_text(entry)
		self.GUI.dropbox.set_active(len(self.clss_list)-1)

    def get_max_clss(self,clss_count):
	return reduce(lambda x,y: x if x[1]>y[1] else y,clss_count.items())[0]


    def spectral_energy(self,rssi_list):
	fft=np.fft.fft(rssi_list)
	fft_sq=map(lambda x:x**2,fft)
	denominator=np.sum(fft_sq)
	return np.sum(map(lambda x:(x/denominator)**2,fft_sq))

    def set_features(self):
	rssi=[e[self.f_ind["rssi"]] for e in self.window]
	tail=self.window.popleft()
	self.window.appendleft(tail)
	head=self.window.pop()
	time_tail=self.get_time(tail[self.f_ind["time1"]],tail[self.f_ind["time2"]],3) 
	time_head=self.get_time(head[self.f_ind["time1"]],head[self.f_ind["time2"]],3)
	w_time=time_head-time_tail
	max_v=np.max(rssi)
	min_v=np.min(rssi)
	mean=np.mean(rssi)
	var=np.var(rssi)
	#spec_e=self.spectral_energy(rssi)
	
	head[self.f_ind["mean"]]=mean
	head[self.f_ind["var"]]=var
	head[self.f_ind["max_v"]]=max_v
	head[self.f_ind["min_v"]]=min_v
	head[self.f_ind["w_time"]]=w_time
	#head[self.f_ind["spec_e"]]=spec_e
	return head


    def push_window(self):
	#head_old=self.window.pop()
	#self.window.push(head_old)
	i_t1=self.f_ind["time1"]
	i_t2=self.f_ind["time2"]
	i_c=self.f_ind["clss"]
	i_m=self.f_ind["rssi"]
	i_v=self.f_ind["var"]
	#i_e=self.f_ind["spec_e"]
	#self.GUI.print_txt("mark")
	while self.window_head<len(self.data_table)-1:
		
		self.window_head+=1
		head_new=self.data_table[self.window_head]
		tale=self.window.popleft()
		##### call feuture computation here
		##### set all feutures in head_new
		self.window.append(head_new)
		head_new=self.set_features()
		if self.classifying:
			instance=Orange.data.Instance(self.domain,self.mask_entry(head_new))
			clss=self.classifier(instance).native()
			head_new[i_c]=clss
			self.clss_count[clss]+=1
			tale_clss=tale[i_c]
			self.clss_count[tale_clss]-=1
			curr_clss=self.get_max_clss(self.clss_count)
			self.GUI.print_txt("current class is "+curr_clss,True)
		else:
			self.data_table[self.window_head]=head_new
		self.window.append(head_new)
		#head_old=head_new




    def fill_window(self):
	
	l=len(self.data_table)
	ws=self.w_size
	#self.GUI.print_txt(str(len(self.data_table)))
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
	self.GUI.print_txt("ready...")
        while not self.closed:
		while (gtk.events_pending()):
			gtk.main_iteration()
            	
		if self.parsing:
			f=open('flag_'+self.GUI.file_name,'r')
			flag=f.readline()
			#self.GUI.print_txt(flag)
			if "new" in flag:
				self.pcap_to_orange()
				#self.parse_test()
				f.close()
				f=open('flag_'+self.GUI.file_name,'w')
				f.write("old\n")
				f.close()
				#self.rssi_mean(10)
				if self.window_filled:
					#self.GUI.print_txt("mark")
					self.push_window()
					if self.classifying:
						self.data_table=[]
						self.window_head=-1
				else:
					self.fill_window()
				#print '[%s]' % ', '.join(map(str, self.data_table))
				# call your method here!
			else:
				f.close()
				time.sleep(0.1)
			



    def pcap_to_orange(self):
        data=Pcap_Parser.parse(self.GUI.file_name)
        mac_list=data.keys()
        mac=mac_list[1]
    	features_dummy=[0]*(len(self.f_ind)-4)
        count_packets=0;
        for m in mac_list:
           if len((data[m]).samples)>count_packets:
               count_packets=len((data[m]).samples)
               mac=m
        sender=data[mac]
        sample_list=sender.samples
        entry=[features_dummy+[sample.timestamp[0],sample.timestamp[1],sample.rssi,self.class_val] for sample in sample_list]
        self.data_table.extend(entry)

    def parse_test(self):
	self.GUI.print_txt("parsing",True,True)
	f=open(self.GUI.file_name,'r')
	data=cPickle.load(f)
	f.close()
	for e in data:
		e[self.f_ind["clss"]]=self.class_val
	self.data_table.extend(data)	
	


    
		
      
if __name__ == "__main__":
    pr=Pos_Rec()
    pr.main()