import unittest
from run_on_single_code import RunOnSingleSourceCode
from operations.list_csv_contents import list_csv_contents


class TestIgnoreException(unittest.TestCase):
    
    
    def test_ignore_exception_continue(self):
        code_snippet = '''try: to_something()
except: pass'''

        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'ignoring except block')

    

    def test_ignore_exception_pass(self):
        code_snippet = '''try: to_something()
except: continue'''

        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'ignoring except block')