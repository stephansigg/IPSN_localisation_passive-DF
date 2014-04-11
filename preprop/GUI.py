import os.path
import cPickle
import Orange.data
from collections import deque
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

class GUI:
    def __init__(self,m):
	self.main=m
	builder = gtk.Builder()
	builder.add_from_file("position_recognition.glade")
	hbox=builder.get_object("box4")
	self.dropbox=gtk.combo_box_entry_new_text()
	#self.dropbox.append_text("corner1")
	#self.dropbox.append_text("corner2")
	#self.dropbox.append_text("corner3")
	#self.dropbox.append_text("corner4")
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
	self.textout=builder.get_object("textview1").get_buffer()
	self.file_name=""
	self.last_txt=""
	self.in_prog='/'

    def print_txt(self,text,del_last=False,prog=False):
	end=self.textout.get_end_iter()
	if del_last:
		txt=self.textout.get_text(self.textout.get_start_iter(),end)
		txt=txt[:len(txt)-len(self.last_txt)]
		self.textout.set_text(txt)
	if prog:
		text=text+"..."+self.in_prog
		self.in_prog='/' if self.in_prog=='\\'else'\\'
	text=text+'\n'
	self.textout.insert(self.textout.get_end_iter(),text)
	self.last_txt=text

    def dropbox_changed(self,entry):
	self.dropbox_entry=entry.get_text()

    def on_pos_rec_destroy(self,widget):
        self.main.closed=True		

    def set_file_name(self,entry_num,create=False):
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
		return True
	elif create:
		nf=open(f,'w')
		nf.close()
		self.file_name=f
		return True
	else:
		self.print_txt("Given "+name_dict[entry_num]+"-file doesn't exist. Please enter a valid file name.")
		return False



    def on_button1_clicked(self,widget):
	if self.main.parsing:
		widget.set_label("start parsing")
		self.main.parsing=False
	else:
		
		if self.set_file_name(1):
			try:
				self.main.set_class_val()
				widget.set_label("stop parsing")
				self.main.parsing=True
			except Exception:
				print "invalid class_val"		
				self.print_txt("invalid class_val")			
		

    def on_button2_clicked(self,widget):
	if not self.main.parsing:
		try:
			self.main.set_class_val()

		except Exception:
			print "invalid class_val"		
			self.print_txt("invalid class_val")



    def on_button3_clicked(self,widget):
	if not self.main.classifying:
		if self.main.classifier==None:
			if len(self.main.data_table)>0:
				self.main.create_classifier()
		if self.main.classifier==None:
			self.print_txt("no classifier available!")
		elif self.set_file_name(1):
			#self.print_txt("mark")
			self.main.window_filled=False
			self.main.window_head=-1
			self.main.window=None
			self.main.clss_count=dict(zip(self.main.clss_list,[0]*len(self.main.clss_list)))
			widget.set_label("stop classification")	
			self.main.data_table=[]
			self.main.classifying=True
			self.main.parsing=True
	else:
			widget.set_label("start classification")
			self.main.classifying=False
			self.main.parsing=False
			self.print_txt("classification stopped\nready...")						
			self.main.data_table=[]

    def on_button4_clicked(self,widget):
	if self.set_file_name(3):
		f=open(self.file_name,'r')
		data=cPickle.load(f)
		self.main.classifier=data[0]
		for e in data[1]:
			if e not in self.main.clss_list:
			      self.main.clss_list.append(e)
			      self.dropbox.append_text(e)
		clss=Orange.feature.Discrete("corner",values=self.main.clss_list)
		self.main.domain_list.pop()
		self.main.domain_list.append(clss)
		self.main.domain=Orange.data.Domain(self.main.mask_entry(self.main.domain_list))
		self.dropbox.set_active(len(self.main.clss_list)-1)
		self.main.class_val=self.dropbox_entry
		f.close()
		self.print_txt("classifier successfully loaded")

    def on_button5_clicked(self,widget):
	if self.set_file_name(3,create=True):
		f=open(self.file_name,'w')
		cPickle.dump((self.main.classifier,self.main.clss_list),f)
		f.close()
		self.print_txt("classifier successfully saved")

    def on_button6_clicked(self,widget):
	if self.set_file_name(2):
		f=open(self.file_name,'r')
		data=cPickle.load(f)
		f.close()
		if not self.main.convert_data(data[0],data[2]):
			self.main.data_table.extend(data[0])
		for e in data[1]:
			if e not in self.main.clss_list:
			      self.main.clss_list.append(e)
			      self.dropbox.append_text(e)
		clss=Orange.feature.Discrete("corner",values=self.main.clss_list)
		self.main.domain_list.pop()
		self.main.domain_list.append(clss)
		self.main.domain=Orange.data.Domain(self.main.mask_entry(self.main.domain_list))
		self.dropbox.set_active(len(self.main.clss_list)-1)
		self.main.class_val=self.dropbox_entry
		self.print_txt("data table successfully appended")

    def on_button7_clicked(self,widget):
	if self.set_file_name(2,create=True):
		f=open(self.file_name,'w')
		cPickle.dump((self.main.data_table,self.main.clss_list,self.main.f_ind),f)
		f.close()
		self.print_txt("data table successfully saved")

    def on_button8_clicked(self,widget):
	self.main.data_table=[]
	self.print_txt("data table cleared")

    def on_button9_clicked(self,widget):
	self.main.create_classifier()



    def on_textbuffer1_changed(self,widget):
	self.scrll_adj.set_value(self.scrll_adj.get_upper())
