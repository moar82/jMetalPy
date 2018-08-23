import unittest
from unittest import mock
from script_features import ScriptFeatures
import os

class ScriptFeaturesTestCases (unittest.TestCase):
    sf = ScriptFeatures("..")
    def test_should_constructor_create_a_non_null_object(self):
        self.assertIsNotNone(self.sf)

    def test_read_features_file_succeded (self):
        self.sf.read_features_file ()
        self.assertIsNotNone( self.sf.d)

    def test_get_random_individual_create_a_non_null_object (self):
        self.sf.read_features_file()
        individual = self.sf.get_random_individual()
        self.assertIsNotNone(individual)

    def test_get_random_individual_create_two_different__objects (self):
        self.sf.read_features_file()
        individual_A = self.sf.get_random_individual()
        individual_B = self.sf.get_random_individual()
        self.assertNotEqual(individual_A,individual_B)

    def test_return_base_individual(self):
        self.sf.read_features_file()
        bi = self.sf.get_base_individual()
        ''' This base individual was generated from confOpt.csv'''
        bioracle = [False,True,False,True,False,False,False,False,False,True,True,False,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,True,True,True,True,False,False,False]
        self.assertEqual(bi,bioracle)

if __name__ == '__main__':
    unittest.main()