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

        ##call the function to open the configuration file, and store it in the map
        ##to generate the initial solutions
        self.sf = ScriptFeatures('')
        self.sf.read_features_file()


    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        ''' First repair the solution that could have been corrupted through the
            transformation operators'''
        repaired_solution = self.sf.js_engine_helper.repair_solution(solution.variables[0])
        solution.variables[0] = repaired_solution
        solution_evaluated = False
        ppm = self.sf.js_engine_helper.evaluate_solution_performance_(solution.variables[0])


        if ppm.memory_us[0]<float('inf'):
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
