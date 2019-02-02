from __future__ import division

from deap import base, creator, tools
import re
import os
from  script_features import ScriptFeatures
import requests
import pdb
from statistics import median, mean


sign = lambda x: '1' if x > 0 else '0'

def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped
def load_product_url(fm_name):
    feature_names = []
    featureNum = 0
    cnfNum = 0
    cnfs = []

    feature_name_pattern = re.compile(r'c (\d+)\$? (\w+)')
    stat_line_pattern = re.compile(r'p cnf (\d+) (\d+)')

    features_names_dict = dict()
    filen = os.path.dirname(os.path.abspath(__file__)) + '/dimacs/' + fm_name + '.dimacs'
    source = open(filen, 'r').read().split('\n')

    for line in source:
        if line.startswith('c'):  # record the feature names
            m = feature_name_pattern.match(line)
            """
            m.group(1) id
            m.group(2) name
            """
            features_names_dict[int(m.group(1))] = m.group(2)

        elif line.startswith('p'):
            m = stat_line_pattern.match(line)
            """
            m.group(1) feature number
            m.group(2) cnf
            """
            featureNum = int(m.group(1))
            cnfNum = int(m.group(2))

            # transfer the features_names into the list if dimacs file is valid
            assert len(features_names_dict) == featureNum, "There exists some features without any name"
            for i in range(1, featureNum + 1):
                feature_names.append(features_names_dict[i])
            del features_names_dict

        elif line.endswith('0'):  # the cnf
            cnfs.append(list(map(int, line.split(' ')))[:-1])  # delete the 0, store as the lint list

        else:
            assert True, "Unknown line" + line
    assert len(cnfs) == cnfNum, "Unmatched cnfNum."

    return feature_names, featureNum, cnfs, cnfNum


class DimacsModel:

    def __init__(self, fm_name, run_id, script):
        self.name = fm_name
        self.run_id = run_id
        self.script = script
        cwd = os.getcwd()
        os.chdir('../..')
        mpath = os.getcwd()
        self.sf = ScriptFeatures(mpath, self.script, "SWAY")
        os.chdir(cwd)
        self.sf.run_id = self.run_id  ###this have to be called after setting the run_id in the client call
        self.sf.read_features_file()

        '''init variables'''
        _, self.featureNum, self.cnfs, self.cnfNum = load_product_url(fm_name)

        # self.cost = []
        # self.used_before = []
        # self.defects = []
        #
        # filen = os.path.dirname(os.path.abspath(__file__)) + '/../Benchmarks/dimacs/' + fm_name + '.dimacs.augment'
        # lines = open(filen, 'r').read().split('\n')[1:]
        #
        # lines = map(lambda x: x.rstrip(), lines)
        # for l in lines:
        #     if not len(l): continue
        #     _, a, b, c = l.split(" ")
        #     self.cost.append(float(a))
        #     self.used_before.append(bool(int(b)))
        #     self.defects.append(int(c))

        creator.create("FitnessMin", base.Fitness, weights=[-1.0] * 4) #4 objectives
        creator.create("Individual", str, fitness=creator.FitnessMin)

        self.creator = creator
        self.Individual = creator.Individual

        self.toolbox = base.Toolbox()
        self.toolbox.register("evaluate", self.eval_ind)
        self.eval = self.toolbox.evaluate

    def __compute_delta (self,org:float, measured: float) -> float:
        return (measured-org)/org
    def compute_dsr(self, ppm, val):
        device_memory = float(val[2])
        device_storage = float(val[3])
        return ((ppm.memory_us[0] - device_memory) / device_memory + (ppm.code_size[0] - device_storage) / device_storage) / 2

    def eval_ind(self, ind, objectives=4):
        """
        return the fitness, but it might be no needed.
        Args:
            ind:

        Returns:

        """
        '''Convert the individual to a list of booleans'''
        solint = [int(x,2) for x in ind]
        sol = [bool(x) for x in solint]
        # validated_solution = self.sf.js_engine_helper.\
        #     keep_mandatory_features_on_solution(sol)
        ppm = self.sf.js_engine_helper.evaluate_solution_performance_(sol)
        if objectives==4:
            try:
                if ppm.memory_us[0] != float('inf'):
                    median_execution_time = median(ppm.execution_time)
                    '''Compute DSR of each  device'''
                    usr_list = []
                    dsr = []
                    cval_max = -1.0
                    for val in self.sf.bc.devices:
                        device_value = float(val[6])
                        dsr.append((self.compute_dsr(ppm, val), device_value))
                        if device_value > cval_max:
                            cval_max = device_value
                    ''' Compute USR'''
                    for val in dsr:
                        usr_list.append(val[0] * (val[1] / cval_max))
                    '''We normalize the code with the original measurements '''
                    ind.fitness.values = (
                        self.__compute_delta \
                            (self.sf.bc.file_size_org, ppm.code_size[0]),  # this does not vary through executions
                        self.__compute_delta \
                            (self.sf.bc.mem_us_org, ppm.memory_us[0]),  # this does not vary through executions
                        self.__compute_delta \
                            (self.sf.bc.use_time_avg, median_execution_time),
                        mean(usr_list)
                    )
                else:
                    '''we penalized the solution since it broke the execution'''
                    ind.fitness.values = (
                    float('inf'),
                    float('inf'),
                    float('inf'),
                    float('inf')
                    )
                    # solution.objectives[3] = float('inf')
                print(str(ind.fitness.values))
            except TypeError:
                '''we penalized the solution since it broke the execution'''
                ind.fitness.values = (
                    float('inf'),
                    float('inf'),
                    float('inf'),
                    float('inf')
                )
        else:
            try:
                if ppm.memory_us[0] != float('inf'):
                    median_execution_time = median(ppm.execution_time)
                    '''We normalize the code with the original measurements '''
                    ind.fitness.values = (
                        self.__compute_delta \
                            (self.sf.bc.file_size_org, ppm.code_size[0]),  # this does not vary through executions
                        self.__compute_delta \
                            (self.sf.bc.mem_us_org, ppm.memory_us[0]),  # this does not vary through executions
                        self.__compute_delta \
                            (self.sf.bc.use_time_avg, median_execution_time)
                    )
                else:
                    '''we penalized the solution since it broke the execution'''
                    ind.fitness.values = (
                    float('inf'),
                    float('inf'),
                    float('inf')
                    )
                print(str(ind.fitness.values))
            except TypeError:
                '''we penalized the solution since it broke the execution'''
                ind.fitness.values = (
                    float('inf'),
                    float('inf'),
                    float('inf')
                )
            # solution.objectives[3] = float('inf')
        return ind.fitness.values

        #
        # @staticmethod
        # def bit_flip_mutate(individual):
        #     # modification log -- not use the mutateRate parameter. just select one bit and flip that
        #     n = len(individual)
        #     i = random.randint(0, n-1)
        #     T = type(individual)
        #     if individual[i] == '0':
        #         individual = T(individual[:i]+'1'+individual[i+1:])
        #     del individual.fitness.values
        #     return individual,
        #
        # @staticmethod
        # def cxTwoPoint(ind1, ind2):
        #     v1 = list(ind1[:])
        #     v2 = list(ind2[:])
        #     split = random.randint(0, len(v1)-1)
        #     for i in range(split):
        #         v1[i], v2[i] = v2[i], v1[i]
        #     T = type(ind1)
        #     ind1 = T(''.join(v1))
        #     ind2 = T(''.join(v2))
        #     del ind1.fitness.values
        #     del ind2.fitness.values
        #     return ind1, ind2


if __name__ == '__main__':
    p = DimacsModel('webportal')
    # ind = p.Individual('1000111000000000010000000001111111000001100100000')
    # p.eval(ind)
    # pdb.set_trace()
