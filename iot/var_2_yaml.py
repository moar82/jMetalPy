"""
.. module:: miniaturization
   :platform: Unix, Windows
   :synopsis: This class provides facilities to convert a VAR file generated
   by MoMIT (using jmetalPy) to yaml file (to configure a duktape JS interpreter)
.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""
import csv
import os
from collections import OrderedDict


class Convert_VAR_2_YAML:
    d = OrderedDict()
    cwd = os.getcwd()  # do not change
    solutions = dict()

    def __init__(self, wkDir, features_file, solution_file_name):
        if len(wkDir) > 0:
            self.cwd = wkDir
        self.filewithfeatures = features_file
        self.solution_file_name = solution_file_name


    def read_features_file (self)-> bool :
        with open (self.cwd + '/' + self.filewithfeatures) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)###to skip the header
            for row in readCSV:
                if len(row)>1:
                    tmplist =[row[1],row[2],row[4]]
                    self.d[int(row[6])]=tmplist
        return len(self.d)> 0


    def read_solution_file (self)-> bool :
        input_file = open(self.cwd + '/' + self.solution_file_name,'r')
        for index, row  in enumerate(input_file):
            list_features = str(row).split(',')
            list_features_bool = []
            for ft in list_features:
                list_features_bool.append(str(ft).replace('[','').replace(']','').lower())
            self.solutions[index] = list_features_bool
        input_file.close()
        return len(self.solutions.keys())>0

    def parse_solutions_file_to_yaml_files (self)->bool:
        for key in self.solutions:
            yaml_file_content = []
            for index, element in enumerate(self.solutions[key]):
                if str(self.d[index][1]).isdigit()==False:
                    #write feature name : element
                    #print (self.d[index][0] + ": " + element)
                    yaml_file_content.append(self.d[index][0] + ": " + str(element).strip())

                else:
                    #if the value is true take default value
                    if element=='true':
                        #print (self.d[index][0] + ":" + self.d[index][1])
                        yaml_file_content.append(self.d[index][0] + ": " + self.d[index][1])
                    #otherwise take tunned value
                    else:
                        yaml_file_content.append(self.d[index][0] + ": " + self.d[index][2])
                        #print(self.d[index][0] + ":" + self.d[index][2])
            fileoutname = self.solution_file_name + '_solution_' + str(key) + '.yaml'
            success = True
            try:
                fout = open (fileoutname,"w")
                for feature in yaml_file_content:
                    fout.write(feature + "\n")
            except:
                print ("Something went wrong when writing to the file: " + fileoutname)
                success = False
            finally:
                fout.close()

        return success


