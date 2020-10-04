import os
import ast
import copy 
import glob

from analyzer import Analyzer
from detection.detection import detection
from operations.save_project_smells import save_detected_different_smells_frequency_in_projects
from operations.save_project_smells import save_smells_categorized_according_to_project_type
# from operations.find_correlation import find_correlation

from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file

from operations.save_smell_frequency import save_smell_frequency
from operations.show_detection_result import show_detection_result
from operations.individual_smell_introduction import individual_smell_introduction_in_total_number_of_projects

from operations.save_project_smells import save_total_smell_counts_in_projects
from operations.save_project_smells import save_unique_smell_counts_in_projects

TOTAL_SRC_FILE_COUNT = 0

def show_total_src_file_count():
    print('')
    print('----------------- Result -----------------')
    print('total file counted : '+str(TOTAL_SRC_FILE_COUNT))
    

def analyze_single_code():
    # file_name = './test-codes/'+'temp_dir.py'
    file_name = './test-codes/'+'src.py'
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
        tree = ast.parse(code, type_comments = True)
        # print(ast.dump(tree, include_attributes = True))
        # print(ast.dump(tree))
        
        global TOTAL_SRC_FILE_COUNT
        TOTAL_SRC_FILE_COUNT += 1

        analyzer = Analyzer()
        analyzer.visit(tree)
        analyzer.refine_tokens()
        analyzer.search_input_in_function_call_and_returned_function_args()
        
        # analyzer.delete_incomplete_tokens()
        # analyzer.make_tokens_byte_free()
        
        analyzer.print_statements()
        analyzer.write_tokens_to_file()
        analyzer.write_user_inputs()
        

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
    
    folder_name = './../final-unzips/'
    # folder_name = './gist-src/'
    project_name = None

    for root, dirs, files in os.walk(folder_name):
        copied_root = copy.deepcopy(root)
        project_name = copied_root.split('/')[3]
        
        should_skip = False

        for part in copied_root.split('/'):
            if part.find('test') != -1:
                should_skip = True
                break

        if should_skip is False:
            for src_file in files:
                if (src_file.lower()).find('test') == -1:
                    if os.path.splitext(src_file)[-1] == '.py':  
                        read_src_code(root, project_name, src_file)
        

def main():

    clear_log_files()    

    # analyze_code_folder()
    analyze_single_code()

    show_total_src_file_count()
    
    show_detection_result() #must thaka lagbe #clear
    # save_smell_frequency() #must thaka lagbe #clear
    # save_detected_different_smells_frequency_in_projects() #must thaka lagbe #clear
    # individual_smell_introduction_in_total_number_of_projects() #must thaka lagbe 
    
    # save_total_smell_counts_in_projects()
    # save_unique_smell_counts_in_projects()
    # save_smells_categorized_according_to_project_type()

    # find_correlation()

if __name__ == "__main__":
    main()
