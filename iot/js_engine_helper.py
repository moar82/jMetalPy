import sys, csv, os, subprocess, time
from collections import deque


"""
.. module:: miniaturization
   :platform: Unix, Windows
   :synopsis: This class provides facilities to evaluate the performance of a JS engine
   configuration

.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""


class JSEngineHelper ():
    """We use this as a public class for evaluating the performance of a JS engine configuration
		.. note:: Based on JerryScript, and the ID we assign to each of the features used

	"""

    def __init__(self) -> None:
        super().__init__()
        self.feature_list = None

    def repair_solution (self,asolution):
        """	the solution needs to be repaired when it is
            randomly generated, and transformed after
            applying transformation operators"""

        # f7-f10 requires to be disable together (one-index-based)
        if asolution[6]==False or asolution[7]==False or asolution[8]==False \
                or asolution[9]==False or asolution[10]==False or asolution[11]==False:
            asolution[6] = False
            asolution[7] = False
            asolution[8] = False
            asolution[9] = False
            asolution[10] = False
            asolution[11] = False

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
        return asolution
        """ pending to evaluate a bit solution """

    def parse_solution_features(self,asolution):
        '''Find the positions in which asolution differs from default solution'''
        

