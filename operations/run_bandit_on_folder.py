import os
import copy
import json
import subprocess

def run_bandit_on_folder():
    projects = []

    for root, dirs, files in os.walk('./../final-unzips/'):
        copied_root = copy.deepcopy(root)
        project_name = copied_root.split('/')[3]

        if project_name not in projects:
            projects.append(project_name)

    
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
            
            input_fp = open(os.path.join('./../../bandits',file_name), 'r')
            contents = input_fp.read()
            if len(contents) == 0: continue
            
            contents = json.loads(contents)
            
            outputs = []
            try:
                for result in contents['results']:
                    outputs.append([result['filename'], result['line_number'], result['issue_text']]) #result['code']
                
                output_fp = open(os.path.join('./../bandits',file_name), 'w+')
                
                for output in outputs:
                    json.dump(output, output_fp)
                    output_fp.write('\n')
                

                output_fp.close()
            except: 
                print('error occurred')
            
            input_fp.close()