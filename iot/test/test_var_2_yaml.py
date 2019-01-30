import unittest
from unittest import mock

from var_2_yaml import Convert_VAR_2_YAML


class Convert_VAR_2_YAMLTestCases (unittest.TestCase):
    #VAR_file = 'VAR.NSGAII.3d-morph.js.1.Miniaturization_test'
    #VAR_file = 'VAR.NSGAII._1.Miniaturization'
    #VAR_file = 'VAR.NSGAII.string-base64.js.4.Miniaturization'
    #VAR_file = 'VAR.NSGAII.access-fannkuch.js_run.Miniaturization'
    VAR_file = 'VAR.SWAY.access-fannkuch_1.txt'

    def test_read_features_file(self):
        convert = Convert_VAR_2_YAML('','confOpt.csv', self.VAR_file)
        self.assertTrue(convert.read_features_file())
    def test_read_solution_file(self):
        convert = Convert_VAR_2_YAML('', 'confOpt.csv',
                                     self.VAR_file)
        self.assertTrue(convert.read_solution_file())
    def test_parse_solutions_file_to_yaml_files (self):
        convert = Convert_VAR_2_YAML('', 'confOpt.csv',
                                     self.VAR_file)
        convert.read_features_file()
        convert.read_solution_file()
        self.assertTrue(convert.parse_solutions_file_to_yaml_files())



if __name__ == '__main__':
    unittest.main()