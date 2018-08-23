import csv, os
from collections import OrderedDict
from random import random
from typing import List
from js_engine_helper import JSEngineHelper

"""
.. module:: script features
   :platform: Unix, Windows
   :synopsis: This module support operations to read the csv
   features file .

.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""

class ScriptFeatures():
    """We use this as a public class for reading the
        features csv files to optimize a JS
        .. note::

    """
    d = OrderedDict ()
    filewithfeatures ='confOpt.csv'
    cwd = os.getcwd() #do not change
    logFile = cwd+"/logbenchmark_primeSimple" + filewithfeatures.split(".")[0] +".log"
    def __init__(self, wkDir):
        if len(wkDir)>0:
            self.cwd = wkDir
        self.js_engine_helper = JSEngineHelper()
        feature = "" #do not change
        idf = "" #do not change
        #fileoutname ="" #name of the configuration file
        device ="laptop"
        program ="harness" #name of the c executable that embeds the JS engine
        script  ="primeSimple.js" #name of the script that we execute
        jsfunction = "forTest" #name of the js function to execute
        report_file="results_benchmark_primeSimple"+ self.filewithfeatures.split(".")[0] + ".csv"
        ####When using  ROM built-in objects, it is necessary to provide an additional parameter to the python's duktape configuration tool
        useROM=False
        ####force to recompile
        recompileDukTape = True
        file_size_org = 555896.00 #B
        mem_us_org = 104816.00 #B
        use_time_avg =0.82 #in seconds, median for the original system
        num_of_runs = 10
        feature_size = 0.00 # do not change
        printheader = 1 # do not change
    # now = time.strftime("%c")
    # print (now)
    # logError(now+"\n")
    # logError("features file: "+ filewithfeatures +"\n")
    # start_time = time.time()

    def logError (self, logmessage):
        flog = open (self.logFile,"a")
        flog.write (logmessage)
        flog.close()
        return

    #here my idea is to save the values in a dictionary structure
    #so I can easily generate the baseline individual
    def read_features_file (self):
        with open (self.cwd + '/' + self.filewithfeatures) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)###to skip the header
            for row in readCSV:
                if len(row)>1:
                    tmplist =[row[1],row[2],row[4]]
                    self.d[row[6]]=tmplist
        self.js_engine_helper.feature_list=self.d

    def get_base_individual (self):
        """ This method returns the individual with default values.
            Note that for the continuous variables, we assume that
            default value means=1/on and tunning the value 0/off"""
        BitSet = []
        for k, v in self.d.items():
            if v[1]=='false':
                BitSet.append(False)
            else:
                BitSet.append(True)
        return BitSet

    def get_random_individual (self):
        randBinList = lambda n: [random() < 0.5 for _ in range(n)]
        num_of_features = len(self.d)
        individual = randBinList(num_of_features)
        return  individual
				  