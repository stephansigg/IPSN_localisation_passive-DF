#!/usr/bin/python
# -*- coding: utf-8 -*-

import cPickle as pickle
import matplotlib.pyplot as plt
from collections import deque, defaultdict, Counter
import time

import Features

# ## XXX testing...
import Visualization

## input
#IN = "/home/mario/public/Recordings/Plots/AH/Day2/rec1_features.pickle"
#IN = "/home/mario/public/Recordings/Plots/AH/Day2/rec2_features.pickle"
#IN = "/home/mario/public/Recordings/Plots/AH/Day4/rec1_features.pickle"

#IN = "/home/mario/public/Recordings/Plots/session2/typing1_features.pickle"
#IN = "/home/mario/public/Recordings/Plots/session2/reading1_features.pickle"
#IN = "/home/mario/public/Recordings/Plots/session2/empty1_features.pickle"
#IN = "/home/mario/public/Recordings/Plots/session2/typing4_features.pickle"

#IN = "/home/mario/public/Recordings/Plots/AH/Clean1/rec1_features.pickle"
#IN = "/home/mario/public/Recordings/Plots/AH/Clean1/rec2_features.pickle"

IN = "/tmp/paper/plots/ETH_officeH81_activity_CH5_5min_2videoStreams_130712_features.pickle"

## experimental histogram feature
def histogram(data):
    c = Counter(data)
    total = float(len(data))
    
    return [x[1] / total for x in c.most_common()]
    
def sum_histograms(h1, h2):
    h_sum = list()
    
    for i in range(max(len(h1), len(h2))):
        try:
            a = h1[i]
        except IndexError:
            a = 0

        try:
            b = h2[i]
        except IndexError:
            b = 0
            
        h_sum.append(a + b)
        
    return h_sum
    
    
def feature_histogram1(units):
    h_all = list()
    
    for unit in units:
        h_u = histogram(unit.get_values())
        h_all = sum_histograms(h_all, h_u)
        
    return h_all
    



class Struct(object):
    pass
    
class Data_Source(object):
    def __init__(self, infile):
        self.infile = infile
        self.part = self._unpickle()
        self.i = -1

        self.activities = False
#        self.activities = set(["empty", "sit", "type"])
#        self.activities = set(["up", "down"])
        
        self.colormapping = defaultdict(lambda: "orange")
#        self.colormapping = defaultdict(lambda: "black")
        self.colormapping["INVALID"] = "gray"
        
        self.colormapping["empty"] = "black"
        self.colormapping["type"] = "green"
        self.colormapping["sit"] = "blue"
        self.colormapping["up"] = "red"
        self.colormapping["down"] = "red"
#        self.colormapping["down"] = "green"
        
        
    def _unpickle(self):
        print "Unpickling:", self.infile
        print

        pickle_input = open(self.infile, 'rb')
        part = pickle.load(pickle_input)
        pickle_input.close()
        
        return part
        
        
    def _map_color(self, label):
        if "INVALID" in label:
            return self.colormapping["INVALID"]
            
        return self.colormapping[label]
        
    
    ## return plot data
    def get(self):
        try:
            window = self.part.windows[self.i]
        except IndexError:
            raise StopIteration

        ## XXX MARIO
        label = window.get_common_label(1)
#        means = [ u.calc_mean() for u in window.units ]
        flat = window.get_values_flat()
#        histo = histogram(window.get_values_flat())
#        histo1 = feature_histogram1(window.units)
        
        s = Struct()
#        s.points = means
#        s.points = (0, means[0] - means[-1], 0, means[3] - means[-1], 0)
        s.points = flat
#        s.points = histo
#        s.points = histo1
        s.label = unicode(label, encoding="utf-8")
        s.color = self._map_color(label)
        s.progress = (self.i, len(self.part.windows)) 
        
        ## XXX debug output
#        print s.points
        
        return s
        
    
    ## return next window
    def next(self):
        self.i += 1
        
        return self.get()
    

    ## XXX MARIO testing...
    def next_in_selection(self):
        point = self.next()

        if self.activities:
            while ( not point.label in self.activities ):
                point = self.next()
            
        return point
    
    
    def show_all(self):
        Visualization.plot_data_pointsXX(self.part.windows, xlim=None, ylim=None, filename=False, dims=None)
    
########################################################################



class Video(object):
    def __init__(self, data):
        ## XXX MARIO
        self.line_type = "."
#        self.line_type = ""
        
        self.data = data
        self.lines = deque()
        
        self.timer_handle = None

        ## init matplotlib
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.manager = plt.get_current_fig_manager()
#        fig.canvas.mpl_connect('key_press_event', key_press)  # <- register key_press event handler

        
        ## XXX
#        plt.xlim(0, 3)
#        plt.ylim(0, 1)
        
        self.status_label = plt.figtext(0.02, 0.02, "STATUS")
#        self.label = self.ax.text(0.02, 0.02, "label")

#        self.label = self.ax.text(0.95, 0.01, 'colored text in axes coords',
#        verticalalignment='bottom', horizontalalignment='right',
#        transform=self.ax.transAxes,
#        color='green', fontsize=15)

        self.label = self.ax.text(0.02, 0.98, "label",
             horizontalalignment='left',
             verticalalignment='top',
#             color=data.color,
             fontsize=16,
             transform = self.ax.transAxes)


    ## timer event
    def timer_event(self):
        # get next window
        try:
            ## XXX MARIO
#            data = self.data.next()
            data = self.data.next_in_selection()
        # --> video finished
        except StopIteration:
            return

        y = data.points
        x = range(len(y))


        ## remove old line
        try:
            old_line = self.lines.popleft()

            ## XXX MARIO                        
            for l in old_line:
                self.ax.lines.remove(l)
        
        # --> no old lines, so we don't have to remove any
        except IndexError:
            pass
            
            
        ## * draw new line *
        line = self.ax.plot( x, y, self.line_type, c=data.color )
        self.lines.append(line)
        
        ## draw label
#        self.label = self.ax.text(0.02, 0.98, data.label,
#             horizontalalignment='left',
#             verticalalignment='top',
#             color=data.color,
#             transform = self.ax.transAxes)

        self.label.set_text(data.label)
        self.label.set_color(data.color)
        
        ## progress
        self.status_label.set_text(str(data.progress[0]) + " / " + str(data.progress[1])
             + ", " + data.label )

        
#        print data.label, Features.calc_mean(y)
        plt.draw()
        
        
        ## XXX
        if ( data.label in ("up", "down")):
            time.sleep(2)
        
        ## set new timer
        self._set_timer(self.speed)


    def _set_timer(self, time):
        # clear timer, if any
        if (self.timer_handle):
            self.manager.window.after_cancel(self.timer_handle)

        # * set timer *
        self.timer_handle = self.manager.window.after(time, self.timer_event)

    def play(self, speed):
        self.speed = speed
        
        self._set_timer(speed)
        plt.show()
        print "quit."
        



#####################################################################################



if __name__ == "__main__":
    # pickled data
    data = Data_Source(IN)
#    data.show_all()  ## XXX testing: old plot feautre..
    
    # video
    video = Video(data)
    video.play(200)
    

