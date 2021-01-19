import os
import copy
import json
import subprocess

from .write_to_csv_file import write_to_csv_file 
from .list_csv_contents import list_csv_contents

def run_bandit_on_folder():
    projects = []
    
    for root, dirs, files in os.walk('./../final-unzips/'):
        copied_root = copy.deepcopy(root)
        project_name = copied_root.split('/')[3]

        if project_name not in projects and project_name != 'eventbrite-master': projects.append(project_name)
    
    # for project_name in reversed(projects):
    #     result_path = './../../bandits/{project_name}.txt'.format(project_name = project_name)
    #     fp = open(result_path, "w+")
    #     fp.close()
        
    # for project_name in reversed(projects):
    #     project_path = os.path.join('./../final-unzips', project_name)
    #     result_path = './../../bandits/{project_name}.txt'.format(project_name = project_name)

    #     print(project_name)
    #     command = 'bandit -r {project_path} -f json -o {result_path}'.format(project_path = project_path, result_path = result_path)
        
    #     try: os.system(command)
    #     except: print('error while detecting security issues')



def clear_bandit_extracted_result_files():
    for root, dirs, files in os.walk('./../bandits/'):
        for file_name in files:
            
            result_path = os.path.join(root, file_name)
            fp = open(result_path, "w+")
            fp.close() 


def summerize_bandit_output():
    clear_bandit_extracted_result_files()

    total_outputs_of_bandit_tool = []
    for root, dirs, files in os.walk('./../../bandits'):
        for part in root.split('/'):
            if 'test' in part.lower(): continue
            if 'tests' in part.lower(): continue

        for file_name in files:
            
            input_fp = open(os.path.join(root,file_name), 'r')
            contents = input_fp.read()

            if len(contents) == 0: continue
            if file_name.lower().find('test') != -1: continue
            
            contents = json.loads(contents)
            outputs = []
            
            try:
                for result in contents['results']:
                    code = result['code'] #.replace('\n', ' ')
                    smell = None
                    smell_names = [
                        ['use of assert statement', ['B101']],
                        ['cross-site scripting', ['B703']],
                        ['insecure deserialization', ['B301','B302','B403','B405','B406','B407','B408','B409','B410','B411']],
                        ['command injection' , ['B606', 'B609', 'B602', 'B603', 'B604', 'B605', 'B404']],
                        ['constructing sql statement upon user input' , ['B608', 'B610', 'B611']],
                        ['dynamic code execution' , ['B307', 'B102']],
                        ['no certificate validation' , ['B501']],
                        ['use of weak cryptographic algorithm' , ['B306', 'B311', 'B303', 'B304', 'B305', 'B505', 'B324']],
                        ['ignore except block' , ['B110', 'B112']],
                        ['debug set to true in deployment' , ['B201']],
                        ['hard-coded secret' , ['B105','B106','B107']],
                        ['bad file permission' , ['B103']],
                        ['hard-coded ip adrress binding' , ['B104']],
                        ['hard-coded tmp directory' , ['B108']],
                        ['insecure yaml operation' , ['B506']]
                    ]

                    for smell_name in smell_names:
                        if result['test_id'] in smell_name[1]:
                            smell = smell_name[0]
                            break

                    if smell is not None:
                        outputs.append([result['filename'], result['line_number'], result['test_id'], smell, result['code']]) 
                        total_outputs_of_bandit_tool.append([result['filename'], result['line_number'], result['test_id'], smell, result['code']])
                
                output_file = None
                output_file = file_name.replace('.txt', '')
                
                output_file = output_file + '.csv'
                output_path = './../bandits/' + output_file

                output_fp = open(output_path, 'w+')
                
                for output in outputs:
                    write_to_csv_file(output_path, output)
                
                output_fp.close()

            except Exception as error: print(str(error))
                            
            input_fp.close()
    
    ofp = open('./../bandits_results.csv', 'w+')
    ofp.close()

    for output in total_outputs_of_bandit_tool:
        write_to_csv_file('./../bandits_results.csv', output)
    print(len(total_outputs_of_bandit_tool))




def show_specific_smells():
    # specific_smells = ['hardcoded_password_funcarg','hardcoded_password_default','hardcoded_password_string']
    # smell_codes = ['B603','B604','B605','B602','B606','B609']

    counter = 0
    # smell_codes = ['B108']
    # smell_codes = ['B611', 'B610', 'B608']
    # smell_codes = ['B303', 'B304', 'B305', 'B306', 'B311', 'B505', 'B324']
    smell_codes = ['B703']
    smells = list_csv_contents('./../bandits_results.csv')
    
    selected_smells = []

    for smell in smells:
        if smell[2] in smell_codes: 
            counter += 1                
            selected_smells.append(smell)

    print('total number of smells ' + str(counter))            
    
    fp = open('./logs/bandits/result.txt', 'w+')
    fp.close()

    for smell in selected_smells:
        write_to_csv_file('./logs/bandits/result.txt', smell)
    