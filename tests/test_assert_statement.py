import unittest
from run_on_single_code import RunOnSingleSourceCode
from operations.list_csv_contents import list_csv_contents


class TestAssertStatement(unittest.TestCase):

    def test_object_attribute(self):
        code_snippet = '''assert self.url, "All clients must have a URL attribute"'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of assert statement')


    def test_single_variable(self):
        code_snippet = '''assert x, "x"'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of assert statement')


    def test_constant_value(self):
        code_snippet = '''assert 16, "16"'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of assert statement')


    def test_variable_with_constant_value(self):
        code_snippet = '''assert x == "goodbye", "x should be goodbye"'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of assert statement')


    def test_variable_with_function_return(self):
        code_snippet = '''assert y == getHello(), "value should be x"'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of assert statement')


    def test_function_call(self): 
        code_snippet = '''assert isinstance(x, int), "x should be int"'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of assert statement')
        
    