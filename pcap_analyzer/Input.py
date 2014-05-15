# -*- coding: utf-8 -*-
from Input_Classes import *
import ConfigParser as cPars
# Configure Parser for loading the configuration
conf = cPars.ConfigParser()
# reads the configuration from config_file and generates according lists for files and groups
# may need to addapt this later on
def get_input(config_file):
        files = list()
        groups = list()
        # parse config file
        conf.read(config_file)
        # obtained all sections in config file, that contain the label Data
        dataLists = [s for s in conf.sections() if "Data" in s]
        # read static information in config file
        session = Group(conf.get('SessionConf', 'SessionName'))
        session.plot_base_dir = conf.get('SessionConf', 'PlotBaseDir')
        session.orange_file = conf.get('SessionConf', 'OrangeFile')
        groups.append(session)
        # read variable information about data sets
        # may need to addapt here later
        for data in dataLists:
            files.append( Input_Data(conf.get(data, 'PcapFile'), conf.get(data, 'Label'), session))
        # EXIT_SUCCESS
        return files, groups
    
