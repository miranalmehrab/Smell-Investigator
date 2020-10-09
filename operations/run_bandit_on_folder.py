import os
import copy
import json
import subprocess

from .write_to_csv_file import write_to_csv_file 

def run_bandit_on_folder():
    projects = ['cassiopeia-master']

    # for root, dirs, files in os.walk('./../final-unzips/'):
    #     copied_root = copy.deepcopy(root)
    #     project_name = copied_root.split('/')[3]

    #     if project_name not in projects:
    #         projects.append(project_name)

    
    for project_name in projects:
        result_path = './../../bandits/{project_name}.txt'.format(project_name = project_name)
        fp = open(result_path, "w+")
        fp.close() 
        
    for project_name in reversed(projects):
        project_path = os.path.join('./../final-unzips', project_name)
        result_path = './../../bandits/{project_name}.txt'.format(project_name = project_name)

        # command = 'ls -l {project_name}'.format(project_name = project_name)
        command = 'bandit -r {project_path} -f json -o {result_path}'.format(project_path = project_path, result_path = result_path)
        # command = 'bandit -r {project_name}'.format(project_name = project_path)
        
        try: 
            print(project_name)
            os.system(command)
            # result = subprocess.run([command], capture_output = True, text = True)
            # print(result.stdout)

        except: 
            print('error while detecting security issues')


def summerize_bandit_output():

    for root, dirs, files in os.walk('./../../bandits'):
        for file_name in files:
            
            input_fp = open(os.path.join(root,file_name), 'r')
            contents = input_fp.read()
            if len(contents) == 0: continue
            
            contents = json.loads(contents)
            outputs = []
            
            try:
                for result in contents['results']:
                    outputs.append([result['filename'], result['line_number'], result['test_id'], result['test_name']]) #result['code']
                
                output_file = None
                name_parts = file_name.split('.')[0: -1]
                
                for part in name_parts:
                    output_file = output_file + part if output_file is not None else part
                    
                output_file = output_file + '.csv'
                output_path = './../bandits/' + output_file

                output_fp = open(output_path, 'w+')
                
                for output in outputs:
                    write_to_csv_file(output_path, output)
                
                output_fp.close()

            except Exception as error: print(str(error))
                            
            input_fp.close()