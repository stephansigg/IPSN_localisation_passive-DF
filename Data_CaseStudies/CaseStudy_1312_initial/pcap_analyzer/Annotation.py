# -*- coding: utf-8 -*-

## event / activity
class Event():
    def __init__(self, rel_start, rel_end, start, end, label):
        self.rel_start = float(rel_start)
        self.rel_end = float(rel_end)
        self.start = float(start)
        self.end = float(end)
        self.label = str(label)

    def __str__(self):
        return str(self.rel_start) + " - " + str(self.rel_end) + ":\t" + str(self.label)


## all events corresponding to one pcam-file
class Annotation:
    ## constructor: creates the events from a csv-file (given by path)
    def __init__(self, csv_file):
        self.events = list()
        
        ## read events from file
        f = open(csv_file, 'r')
        
        # header
        print f.readline()
        
        
        # data
        for line in f:
            e = Event(*line.strip().split(","))
            self.events.append(e)
            
            ## XXX debug output
            print e
            
            
    ## returns the label for a given time
    def get_label_for(self, start, length):
        ## too early
        if ( start < self.events[0].start ):
            return "INVALID (early)"
            
        ## too late
        if ( start > self.events[-1].end ):
            return "INVALID (late)"
        
        ## find label
        for e in self.events:
            if ( e.start <= start and e.end >= start ):
                return e.label
        

## backward compatibility: acts like annotation but always gives the same label        
class Single_Label_Annotation:
    def __init__(self, label):
        self.label = label
        
    def get_label_for(self, *args):
        return self.label
            
            
## XXX testing
if __name__ == "__main__":
    Annotation("/tmp/mouse.csv")

