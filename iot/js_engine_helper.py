import configparser
import sys,  os, subprocess, csv
from collections import deque
from random import random

"""
.. module:: miniaturization
   :platform: Unix, Windows
   :synopsis: This class provides facilities to evaluate the performance of a JS engine
   configuration

.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""

class ProgramPerformanceMetrics:
    ''' In this class we define the properties of the program to optimize'''
    def __init__(self) -> None:
        self.code_size, self.memory_us, self.execution_time = [],[],[]
    # @property
    # def code_size_delta(self,code_size_org) -> float:
    #     delta()


class ProgramLog():
    '''This class writes the log of the execution'''

    def __init__(self, cwd: str, experiment_name: str) -> None:
        super().__init__()
        self.logFile = cwd+"/benchmark_" + experiment_name +".log"

    def logError (self, logmessage: str):
        flog = open (self.logFile,"a")
        flog.write (logmessage)
        flog.close()
        return


class BenchmarkConfiguration ():
    ''' Here we read the configuration from a text file
        TODO: Add the properties of each device:memory capacity, storage capacity
        '''
    def __init__(self) -> None:
        super().__init__()
        '''if there is not  configuration file we create a new one'''
        if os.path.isfile('config.ini') == False:
            self.create_default_configuration_file()
        self.read_configuration_file()
        self.devices = []
        self.read_USR_file()
    def create_default_configuration_file(self):
        config = configparser.ConfigParser()
        config['DUKTAPE.OPTIONS'] = {'dukpath':'/home/moar82/duktape-2.3.0'}
        config['JS.FEATURES'] = {'filewithfeatures':'confOpt.csv'}
        config['PROGRAM.TO.TEST'] = {'experiment_name':'primeSimple',
                                    'idf':'optimize',
                                     'device':'laptop',
                                     'program':'harness',
                                     'script':'primeSimple.js',
                                     'jsfunction':'forTest',
                                     'runs':'10'
                                     }
        config['DEFAULT.PERFORMANCE.MEASUREMENTS'] = {'file_size': '555896.00',
                                     'mem_us': '104816.00',
                                     'use_time_avg': '0.82',
                                    'usr_file_path': 'USR.csv'      }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    def read_configuration_file(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.duk_path =  config['DUKTAPE.OPTIONS']['dukpath']
        self.experiment_name = config['PROGRAM.TO.TEST']['experiment_name']
        self.filewithfeatures = config['JS.FEATURES']['filewithfeatures']
        self.idf = config['PROGRAM.TO.TEST']['idf']
        self.device_benchmarked = config['PROGRAM.TO.TEST']['device']
        self.program = config['PROGRAM.TO.TEST']['program']
        self.script = config['PROGRAM.TO.TEST']['script']
        self.jsfunction = config['PROGRAM.TO.TEST']['jsfunction']
        self.runs = config['PROGRAM.TO.TEST']['runs']
        self.file_size_org = float(config['DEFAULT.PERFORMANCE.MEASUREMENTS']['file_size'])
        self.mem_us_org = float(config['DEFAULT.PERFORMANCE.MEASUREMENTS']['mem_us'])
        self.use_time_avg = float(config['DEFAULT.PERFORMANCE.MEASUREMENTS']['use_time_avg'])
        self.USR_file_path = config['DEFAULT.PERFORMANCE.MEASUREMENTS']['usr_file_path']

    def fitem(item):
        item = item.strip()
        try:
            item = float(item)
        except ValueError:
            pass
        return item


    def read_USR_file(self):
        with open(self.USR_file_path) as f:
            self.devices = [tuple(line) for line in csv.reader(f)]
        self.devices.pop(0)

        print("devices read from USR file:%d" %len(self.devices))

class JSEngineHelper ():
    """We use this as a public class for evaluating the performance of a JS engine configuration
		.. note:: Based on JerryScript, and the ID we assign to each of the features used

	"""

    def __init__(self, logError : ProgramLog , cwd: str, bc: BenchmarkConfiguration) -> None:
        super().__init__()
        self.feature_list = None
        self.defaultSolution = None
        self.plog = logError
        self.cwd = cwd
        self.bc = bc
        self.tested_solutions = {}
        self.run_id = None


    defaultSolution = []
    def repair_solution (self,asolution):
        """	the solution needs to be repaired when it is
            randomly generated, and transformed after
            applying transformation operators"""

        # f7-f10 requires to be disable together (one-index-based)
        if asolution[6]==True or asolution[7]==True or asolution[8]==True:
            if random()<0.2:
                asolution = self.defaultSolution.copy()
                asolution[6] = True
                asolution[7] = True
                asolution[8] = True
                asolution[9] = False
            else:
                asolution[6] = False
                asolution[7] = False
                asolution[8] = False
                #asolution[9] = True

        # f14 requires f11 to be disable too (one-index-based)
        if asolution[13]==False:
            asolution[10]=False
        # f27 requires f26 to be disable too (one-index-based)
        if asolution[26]==False:
            asolution[25]=False
        # f32 requires f34 to be disable too (one-index-based)
        if asolution[31]==False:
            asolution[33]=False
        # f72 requires f73 to have the same value to be effective (one-index-based)
        if asolution[71]==False or asolution[72]==False:
            asolution[71] = False
            asolution[72] = False
        # f16 requires f20 to be false
        if (asolution[15] & asolution[19])==False:
            asolution[15] = False
            asolution[19] = False
        # f17 requires f21 to be false
        if (asolution[16] & asolution[20])==False:
            asolution[16] = False
            asolution[20] = False
        #f31 requires f24 to be deactivated as well
        if asolution[30]==False:
            asolution[23] = False
        # f24 requires f30 to be deactivated as well
        if asolution[23] == False:
            asolution[29] = False
        return asolution


    def evaluate_solution_performance_(self, asolution):
        ''' Create a new object to record the measurements'''
        ppm = ProgramPerformanceMetrics()
        ''' validate if the solution was not already evaluated to avoid reevaluting solutions'''
        string_sol = ''.join(str(int(e)) for e in asolution)
        decimal_rep_asolution = int(string_sol,2)
        if decimal_rep_asolution in self.tested_solutions:
            ppm.code_size =  self.tested_solutions.get(decimal_rep_asolution)[0]
            ppm.memory_us = self.tested_solutions.get(decimal_rep_asolution)[1]
            ppm.execution_time = self.tested_solutions.get(decimal_rep_asolution)[2]
        else:
            '''Find the positions in which asolution differs from default solution'''
            differences = [
                (inner_idx)
                for inner_idx, (a_element, b_element) in enumerate(zip(asolution, self.defaultSolution))
                if a_element != b_element
            ]

            '''Now let's iterate over the differences to generate a new config.yaml file'''
            os.system('mkdir -p ' + self.cwd + '/configFiles/' + self.bc.idf)
            fileoutname =  self.cwd +"/configFiles/" + self.bc.idf + "/" + self.bc.idf + ".yaml"
            fout = open(fileoutname, "w")
            for feature_idx in differences:
                features = list(self.feature_list.items())
                feature = features[feature_idx][1][0] + ': ' + features[feature_idx][1][2]
                fout.write(feature + "\n")
            fout.close()
            '''Now we need to compile the new config file'''
            os.system('mkdir -p ' + self.cwd + '/duktape-src/' + self.bc.idf + self.run_id)
            os.system('rm -f ' + self.cwd + '/duktape-src/' + self.bc.idf + self.run_id+ '/*')
            '''Because using ROM requires special parameter for the config script
                we detect when this happens'''
            if asolution[6]==True:
                os.system('python '+ self.bc.duk_path+ '/tools/configure.py --output-directory ' + \
                          self.cwd + '/duktape-src/' + self.bc.idf + self.run_id + ' --rom-support --option-file ' +  fileoutname)
            else:
                os.system('python '+ self.bc.duk_path+ '/tools/configure.py --output-directory ' + \
                           self.cwd + '/duktape-src/' + self.bc.idf + self.run_id + ' --option-file '  + fileoutname)
            ###Copy the source code, since I have problems when compiling when the headers are in a different dir
            ###Now the next step is to compile the code
            os.system('cp -f ' + self.cwd + '/{' + self.bc.program + '.c,' + self.bc.script + '} ' + self.cwd + '/duktape-src/' + self.bc.idf + self.run_id + '/')
            os.chdir(self.cwd + '/duktape-src/' + self.bc.idf + self.run_id + '/')
            compileSucc = os.system('gcc -std=c99 -o ' + self.bc.program + ' -Iduktape-src duktape.c ' + self.bc.program + '.c -lm')
            if compileSucc == 0:
                ####Now let's measure the size of the file
                returned_out = subprocess.check_output(["stat", "-c", "\"%s\"", self.bc.program])
                try:
                    feature_size = float(returned_out.decode("utf-8").replace("\"", "").strip())
                except ValueError:
                    # here we should log an error with the corresponding feature
                    self.plog.logError(
                        "When measuring file size: " + self.bc.program + ". configuration file: " + fileoutname + ". errorMsg: " + returned_out.decode(
                            "utf-8").replace("\"", "").strip() + "\n")
                    self.plog.logError(
                        "When executing program: " + self.bc.program + ". configuration file: " + fileoutname + "\n")
                    os.chdir(self.cwd)  # always return to the original path
                    ppm.memory_us.append(float('inf'))
                    self.tested_solutions[decimal_rep_asolution] = [float('inf'), float('inf'), float('inf')]
                    return ppm

                ppm.code_size.append(feature_size)
                """ Now it is time to execute the script to the harness and collect memory usage and execution time """
                time_lines_count = 1  # how many lines /usr/bin/time produces
                for count in range(0, int(self.bc.runs)):
                    p = subprocess.Popen(['/usr/bin/time', '-f \" %U , %S , %P\"', \
                                          './' + self.bc.program, self.bc.script, self.bc.jsfunction], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    with p.stdout:
                        r = deque(iter(p.stdout.readline, b''), maxlen=time_lines_count)
                    with p.stderr:
                        q = deque(iter(p.stderr.readline, b''), maxlen=time_lines_count)
                    rc = p.wait()
                    # print(b''.join(q).decode().strip())
                    coltemp = str(b''.join(r).decode().strip()).split(',') + str(b''.join(q).decode().strip()).split(',')
                    print  (coltemp)
                    try:
                        ppm.memory_us.append(float(coltemp[0].replace("\"", "").strip()))
                    except:
                        self.plog.logError("When executing program: " + self.bc.program + ". configuration file: " + fileoutname + ". errorMsg: " +
                                           coltemp[0].replace("\"", "").strip() + "\n")
                        ppm.memory_us.append  (float('inf'))
                        break
                    ppm.execution_time.append(float(coltemp[1].replace("\"","").strip()))
                self.tested_solutions[decimal_rep_asolution]= [ppm.code_size,ppm.memory_us,ppm.execution_time]
            else:
                self.plog.logError(
                    "When compiling program: " + self.bc.program + ". configuration file: " + fileoutname + "\n")
                ppm.memory_us.append(float('inf'))
                self.tested_solutions[decimal_rep_asolution] = [float('inf'), float('inf'), float('inf')]
            os.chdir(self.cwd)  # always return to the original path
        return ppm

