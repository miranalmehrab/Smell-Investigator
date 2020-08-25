import os
import ast
import copy 
import glob

from parse import Analyzer
from detection.detection import detection

from operations.showResult import show_results
from operations.projectSmell import save_project_smells
from operations.showProjectSmell import save_individual_projects_smells

TOTAL_SRC_FILE_COUNT = 0

def print_total_file_count():
    print('')
    print('----------------- Result -----------------')
    print('total file counted : '+str(TOTAL_SRC_FILE_COUNT))
    

def analyze_single_code():
    file_name = './test-codes/'+'src.py'
    analyze_code('', '', file_name)
    show_results()


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
        analyzer.checkUserInputsInFunctionArguments()
        analyzer.refineTokens()
        # analyzer.delete_incomplete_tokens()
        # analyzer.makeTokensByteFree()
        # analyzer.printStatements()
        analyzer.writeToFile()

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

    print_total_file_count()
    show_results()
    save_project_smells()
    save_individual_projects_smells()



if __name__ == "__main__":
    main()
