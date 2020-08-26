import os
import ast
import copy 
import glob

from parse import Analyzer
from detection.detection import detection

from operations.show_detection_result import show_detection_result
from operations.save_project_smells import save_total_count_of_detected_smells_in_projects as toatl_smells_in_project
from operations.save_project_smells import save_detected_different_smells_frequency_in_projects as different_smells_in_project


TOTAL_SRC_FILE_COUNT = 0

def show_total_file_count():
    print('')
    print('----------------- Result -----------------')
    print('total file counted : '+str(TOTAL_SRC_FILE_COUNT))
    

def analyze_single_code():
    file_name = './test-codes/'+'src.py'
    analyze_code('', '', file_name)
    show_detection_result()


def clear_log_files():
    for root, dirs, log_files in os.walk('./logs/'):    
        for log_file in log_files:
            with open(os.path.join(root, log_file), 'w') as fp: 
                fp.close()


def detect_smells_in_tokens(project_name,src_file):
    try:
        fp = open("logs/tokens.txt", "r")
        tokens = fp.read()
        
        fp.close()
        detection(tokens, project_name, src_file)
    
    except Exception as error:
        print(str(error))


def parse_code(code, src_file):
    try:
        tree = ast.parse(code, type_comments=True)
        # print(ast.dump(tree, include_attributes = True))
        # print(ast.dump(tree))
        
        global TOTAL_SRC_FILE_COUNT
        TOTAL_SRC_FILE_COUNT += 1

        analyzer = Analyzer()
        analyzer.visit(tree)
        analyzer.refine_tokens()
        # analyzer.delete_incomplete_tokens()
        # analyzer.make_tokens_byte_free()
        # analyzer.print_statements()
        analyzer.write_tokens_to_file()

    except Exception as error:
        print(str(error)) 


def read_src_code(root, project_name, src_file):
    try: 
        with open(os.path.join(root, src_file), "r") as src_file:     
            code = None
            
            try: 
                src_file = open(src_file.name, 'r')
                code = src_file.read()
                
            except Exception as error:  
                print(str(error))
                
            if code is not None: 
                parse_code(code, src_file)
                detect_smells_in_tokens(project_name, src_file)
    
    except Exception as error: 
        print(str(error))
        


def analyze_code_folder():
    project_name = None
    
    for root, dirs, files in os.walk('./../unzips/'):
        root_copy = copy.deepcopy(root)
        project_name = root_copy.split('/')[3]
        should_skip = False 

        for part in root_copy.split('/'):
            if part.find('test') != -1 or part.find('tests') != -1:
                should_skip = True

        if should_skip is False:
            for src_file in files:
                if src_file.find('test') == -1 or src_file.find('tests') == -1: 
                    
                    if os.path.splitext(src_file)[-1] == '.py':   
                        read_src_code(root, project_name, src_file)
    
    

def main():
    clear_log_files()    
    analyze_code_folder()
    # analyze_single_code()

    show_total_file_count()
    show_detection_result()
    
    different_smells_in_project()
    toatl_smells_in_project()



if __name__ == "__main__":
    main()
