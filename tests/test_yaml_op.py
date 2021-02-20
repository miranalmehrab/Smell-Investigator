import unittest
from run_on_single_code import RunOnSingleSourceCode
from operations.list_csv_contents import list_csv_contents


class TestBadYamlOps(unittest.TestCase):

    unwated_ops = ['yaml.load', 'yaml.load_all', 'yaml.full_load', 'yaml.dump', 'yaml.dump_all', 'yaml.full_load_all']

    def test_yaml_load_call(self):
        code_snippet = '''yaml.load(stream)'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of insecure YAML operations')


    def test_yaml_load_return(self):
        code_snippet = '''def get_contents():
                            return yaml.load(stream)
                        '''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of insecure YAML operations')


    def test_yaml_load_value_assign(self):
        code_snippet = '''contents = yaml.load(stream)'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of insecure YAML operations')
    
    def test_yaml_load_nested_call(self):
        code_snippet = '''print(yaml.load(stream))'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'use of insecure YAML operations')