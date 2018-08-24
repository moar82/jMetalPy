import unittest
from unittest import mock
from script_features import ScriptFeatures
import os

class JSEngineHelperTestCases (unittest.TestCase):
    def setUp(self):
        '''Delete any configuration file'''
        os.system('rm -f config.ini')
        self.sf = ScriptFeatures(os.path.dirname(os.path.abspath(__file__))+"/..") #relative path to unit test
        self.jseh = self.sf.js_engine_helper

    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.jseh)

    def test_repair_solution (self):
        #sf = ScriptFeatures("..")
        self.sf.read_features_file()
        asolution = self.sf.get_random_individual()
        repaired_solution = self.jseh.repair_solution(asolution)
        repaired = True

        if asolution[13] & asolution [10] == False:
            if asolution[10] == True:
                repaired = False
        if asolution[26] & asolution[25] == False:
            if asolution[25] ==True:
                repaired = False

        if asolution[31] & asolution[33] == False:
            if asolution[33] == True:
                repaired = False

        if asolution[71] & asolution[72] == False:
            if asolution[71] != asolution[72]:
                repaired = False

        if asolution[6] & asolution[7]  & asolution[8]&\
                asolution[9]& asolution[10]& asolution[11] == False:
            for f in range (6, 12):
                if asolution[f]==True:
                    repaired = False
                    break

        self.assertTrue(repaired)

    def test_evaluate_solution_performance_create_a_non_null_object(self):
        '''create a minimal solution to test: f1, f5 to true
            DUK_USE_ALLOW_UNDEFINED_BEHAVIOR, DUK_USE_LIGHTFUNC_BUILTINS
             f2 has a numerical value DUK_USE_FATAL_MAXLEN'''
        self.sf.read_features_file()
        asolution = [True,False,False,True,True,False,False,False,False,True,True,False,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,True,True,True,True,False,False,False]
        ppm = self.jseh.evaluate_solution_performance_(asolution)
        self.assertIsNotNone(ppm)



if __name__ == '__main__':
    unittest.main()