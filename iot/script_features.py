import csv, os
from collections import OrderedDict
from random import random
from js_engine_helper import JSEngineHelper, ProgramLog, BenchmarkConfiguration

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
    cwd = os.getcwd() #do not change

    @property
    def run_id(self) -> str:
        return self.__run_id

    @run_id.setter
    def run_id(self, run_id) -> None:
        self.__run_id = run_id
        self.js_engine_helper.run_id = run_id
    def __init__(self, wkDir, script):
        if len(wkDir)>0:
            self.cwd = wkDir
        self.bc = BenchmarkConfiguration(script)
        self.plog = ProgramLog(self.cwd, self.bc.experiment_name)
        self.js_engine_helper = JSEngineHelper(self.plog,self.cwd, self.bc)
        self.filewithfeatures = self.bc.filewithfeatures

    def read_features_file (self):
        with open (self.cwd + '/' + self.filewithfeatures) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)###to skip the header
            for row in readCSV:
                if len(row)>1:
                    tmplist =[row[1],row[2],row[4]]
                    self.d[row[6]]=tmplist
        self.js_engine_helper.feature_list=self.d
        self.js_engine_helper.defaultSolution = self.get_base_individual()

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
				  