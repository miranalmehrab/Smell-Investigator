import unittest
from run_on_single_code import RunOnSingleSourceCode
from operations.list_csv_contents import list_csv_contents


class TestBadFilePermission(unittest.TestCase):

    def test_octal_permission(self):
        code_snippet = '''os.chmod('/etc/hosts', 0x777)'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'bad file permission')


    def test_parameter_permission(self):
        code_snippet = '''os.chmod('/etc/hosts',stat.S_IRWXO)'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'bad file permission')


    def test_subprocess_call(self):
        code_snippet = '''subprocess.call(['chmod', 0x777, 'path'])'''
        code_analyze = RunOnSingleSourceCode(None, False, False, code_snippet)
        code_analyze.analyze_single_code()

        detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
        self.assertEqual(detected_smells[0][2], 'bad file permission')