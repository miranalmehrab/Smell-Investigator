import unittest
from run_on_single_code import RunOnSingleSourceCode
from operations.list_csv_contents import list_csv_contents


class TestXss(unittest.TestCase):

    
    def test_yaml_load_call(self):
        code_snippet = '''mark_safe(unsafe_strings)'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'cross site scripting')


    def test_yaml_load_return(self):
        code_snippet = '''def get_ui_contents():
                            return mark_safe(unsafe_strings)
                        '''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'cross site scripting')


    def test_yaml_load_value_assign(self):
        code_snippet = '''ui_contents = mark_safe(unsafe_strings)'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'cross site scripting')
    
    def test_yaml_load_nested_call(self):
        code_snippet = '''print(mark_safe(unsafe_strings))'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'cross site scripting')