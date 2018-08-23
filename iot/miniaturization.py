from math import pi, cos

from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution
from script_features import ScriptFeatures
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

    def __init__(self, number_of_variables: int = 1, number_of_objectives=3):
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
        self.sf = ScriptFeatures()
        self.sf.read_features_file()


    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        k = self.number_of_variables - self.number_of_objectives + 1

        g = sum([(x - 0.5) * (x - 0.5) - cos(20.0 * pi * (x - 0.5))
                 for x in solution.variables[self.number_of_variables - k:]])

        g = 100 * (k + g)

        solution.objectives = [(1.0 + g) * 0.5] * self.number_of_objectives

        for i in range(self.number_of_objectives):
            for j in range(self.number_of_objectives - (i + 1)):
                solution.objectives[i] *= solution.variables[j]

            if i != 0:
                solution.objectives[i] *= 1 - solution.variables[self.number_of_objectives - (i + 1)]

        return solution

    def get_name(self):
        return 'Miniaturization'

    def create_solution(self) -> BinarySolution:

        new_solution = BinarySolution(self.number_of_variables, self.number_of_objectives, self.number_of_constraints,
                                     self.lower_bound, self.upper_bound)
        new_solution.variables = \
            [self.sf.get_random_individual() for i in range(self.number_of_variables)]

        return new_solution
