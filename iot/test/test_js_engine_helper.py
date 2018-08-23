import unittest
from unittest import mock
from js_engine_helper import JSEngineHelper
from script_features import ScriptFeatures
import os

class JSEngineHelperTestCases (unittest.TestCase):
    jseh = JSEngineHelper()

    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.jseh)

    def test_repair_solution (self):
        sf = ScriptFeatures("..")
        sf.read_features_file()
        asolution = sf.get_random_individual()
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


if __name__ == '__main__':
    unittest.main()