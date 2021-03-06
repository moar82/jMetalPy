from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution
from script_features import ScriptFeatures
from statistics import median, mean
"""
.. module:: miniaturization
   :platform: Unix, Windows
   :synopsis: Miniaturization of programs for IoT a multi-objective problem.
   this is a problem class

.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""


class Miniaturization(BinaryProblem):
    """ Problem Miniaturization

    .. note:: Unconstrained problem. The default number of variables and objectives are
      and 3 objectives (code size, memory and size).
    """

    def __init__(self, number_of_variables: int = 1, number_of_objectives=4):
        """ :param number_of_variables: number of decision variables of the problem.
        """
        super(Miniaturization, self).__init__()
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE] * number_of_objectives

        self.lower_bound = self.number_of_variables * [0.0]
        self.upper_bound = self.number_of_variables * [1.0]

        BinarySolution.lower_bound = self.lower_bound
        BinarySolution.upper_bound = self.upper_bound


        self.__run_id = None
        self.repair_solution = True

        '''to naming the different executions with an id'''
    @property
    def run_id(self) -> str:
        return self.__run_id
    @run_id.setter
    def run_id(self,run_id) -> None:
        self.__run_id = run_id
    '''to parametrize the name of the script to analyse to perform batch mode using bash script'''
    @property
    def script(self) -> str:
        return self.__script
    @property
    def algo_name(self) -> str:
        return self.__algo_name
    @algo_name.setter
    def algo_name (self, algo_name) -> None:
        self.__algo_name = algo_name
    @script.setter
    def script (self,script) -> None:
        self.__script= script
        ##call the function to open the configuration file, and store it in the map
        ##to generate the initial solutions
        self.sf = ScriptFeatures('', script, self.algo_name )
        self.sf.run_id =  self.__run_id ###this have to be called after setting the run_id in the client call
        self.sf.read_features_file()


    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        ''' First apply the mandatory features '''
        ''' Note that in python the class is pass as reference so the value is modified automatically.  We use tmp variables for readability though.'''
        validated_solution = self.sf.js_engine_helper.keep_mandatory_features_on_solution(solution.variables[0])
        ''' Then repair the solution that could have been corrupted through the
            transformation operators'''
        if self.repair_solution==True:
            repaired_solution = self.sf.js_engine_helper.repair_solution(validated_solution)
            solution.variables[0] = repaired_solution
        else:
            solution.variables[0] = validated_solution
        ppm = self.sf.js_engine_helper.evaluate_solution_performance_(solution.variables[0])
        try:
            if ppm.memory_us[0]!=float('inf'):
                '''We normalize the code with the original measurements '''
                solution.objectives[0] = self.__compute_delta\
                    (self.sf.bc.file_size_org,ppm.code_size[0])#this does not vary through executions
                solution.objectives[1] = self.__compute_delta\
                    (self.sf.bc.mem_us_org,ppm.memory_us[0])  #this does not vary through executions
                median_execution_time = median(ppm.execution_time)
                solution.objectives[2] = self.__compute_delta\
                    (self.sf.bc.use_time_avg,median_execution_time)
                '''Compute DSR of each  device'''
                usr_list = []
                dsr = []
                cval_max = -1.0
                for val in self.sf.bc.devices:
                   device_value = float(val[6])
                   dsr.append ( (self.compute_dsr(ppm, val), device_value))
                   if device_value > cval_max:
                        cval_max = device_value
                ''' Compute USR'''
                for val in dsr:
                    usr_list.append( val[0] * ( val[1] /cval_max )  )
                solution.objectives[3] = mean ( usr_list )
            else:
                '''we penalized the solution since it broke the execution'''
                solution.objectives[0] = float('inf')
                solution.objectives[1] = float('inf')
                solution.objectives[2] = float('inf')
                solution.objectives[3] = float('inf')
            print (solution.objectives)
        except TypeError:
            '''we penalized the solution since it broke the execution'''
            solution.objectives[0] = float('inf')
            solution.objectives[1] = float('inf')
            solution.objectives[2] = float('inf')
            solution.objectives[3] = float('inf')
        return solution

    def compute_dsr(self, ppm, val):
        device_memory = float(val[2])
        device_storage = float(val[3])
        return ((ppm.memory_us[0] - device_memory) / device_memory + (ppm.code_size[0] - device_storage) / device_storage) / 2

    def get_name(self):
        return 'Miniaturization'

    def __compute_delta (self,org:float, measured: float) -> float:
        return (measured-org)/org

    def create_solution(self) -> BinarySolution:

        new_solution = BinarySolution(self.number_of_variables, self.number_of_objectives, self.number_of_constraints)
        new_solution.variables = \
            [self.sf.get_random_individual() for i in range(self.number_of_variables)]
        return new_solution

    def save_values_achieved(self,solution_list: list, file_name):
        '''to compare the results in disk space, memory usage and execution time'''
        with open(file_name, 'w') as of:
            for solution in solution_list:
                file_size = (solution.objectives[0]*self.sf.bc.file_size_org) +self.sf.bc.file_size_org
                usr_mem = (solution.objectives[1]*self.sf.bc.mem_us_org) +self.sf.bc.mem_us_org
                time_usr =(solution.objectives[2]*self.sf.bc.use_time_avg) +self.sf.bc.use_time_avg
                dsr = solution.objectives[3]
                of.write(str(file_size) + ",")
                of.write(str(usr_mem) + ",")
                of.write(str(time_usr) + ",")
                of.write(str(dsr))
                of.write("\n")