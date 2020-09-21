import os
import ast
import copy 
import glob

from analyzer import Analyzer
from detection.detection import detection
from operations.save_project_smells import save_smells_categorized_according_to_project_type
from operations.save_project_smells import save_unique_smell_count_in_project
# from operations.find_correlation import find_correlation

from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file
from operations.show_detection_result import show_detection_result
from operations.individual_smell_in_projects import individual_smell_in_projects
from operations.save_project_smells import save_total_count_of_detected_smells_in_projects as toatl_smells_in_project
from operations.save_project_smells import save_detected_different_smells_frequency_in_projects as different_smells_in_project

TOTAL_SRC_FILE_COUNT = 0

def show_total_file_count():
    print('')
    print('----------------- Result -----------------')
    print('total file counted : '+str(TOTAL_SRC_FILE_COUNT))
    

def analyze_single_code():
    file_name = './test-codes/'+'src.py'
    file_name = './test-codes/'+'if-test.py'
    read_src_code('', '', file_name)
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


def analyze_ast_tree(code, src_file):
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
        # analyzer.print_statements('comparison')
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
                analyze_ast_tree(code, src_file)
                detect_smells_in_tokens(project_name, src_file)
    
    except Exception as error: 
        print(str(error))
        


def analyze_code_folder():
    project_name = None
    names = []

    for root, dirs, files in os.walk('./../dataset unzip/'):
        root_copy = copy.deepcopy(root)
        project_name = root_copy.split('/')[3]
        should_skip = False

        # if project_name not in names and project_name != "":
        #     names.append(project_name)
        
        for part in root_copy.split('/'):
            if part.find('test') != -1:
                should_skip = True
                break

        if should_skip is False:
            for src_file in files:
                if (src_file.lower()).find('test') == -1:
                    if os.path.splitext(src_file)[-1] == '.py':  
                        read_src_code(root, project_name, src_file)
                
        #     for name in names:
        # write_to_csv_file('logs/project_names.csv', [name.replace('-master', '')])


def main():
    # clear_log_files()    
    # analyze_code_folder()
    
    # analyze_single_code()
    # save_unique_smell_count_in_project()

    # show_total_file_count()
    # show_detection_result()
    
    # different_smells_in_project()
    # toatl_smells_in_project()
    # individual_smell_in_projects()
    save_smells_categorized_according_to_project_type()
    # find_correlation()



if __name__ == "__main__":
    main()
