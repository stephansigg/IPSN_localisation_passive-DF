# -*- coding: utf-8 -*-

import Annotation

## struct, holds metadata for a group of activities
class Group:
    def __init__(self, name):
        self.name = name
        self.plot_base_dir = None
        self.orange_file = None
        self.results = list()
        
    def add_result(self, res):
        self.results.append(res)
        
    
## struct to hold all meta data for parsing
##  backward compatibility: still accepts a label,
##    - but converts it into an Annotation
##    - use "annotation" as kwarg
class Input_Data:
    def __init__(self, infile, label, group, packets=-1, **kwargs):
        self.infile = infile
#        self.label = label
        self.group = group
        self.packets = packets
        
        ## use annotation file, (backward compatible for single labels)
        try:
            self.annotation = Annotation.Annotation(kwargs["annotation"])
        except KeyError:
            self.annotation = Annotation.Single_Label_Annotation(label)

