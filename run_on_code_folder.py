import os
import ast
import copy 

from analyzer import Analyzer
from detection.detection import detection
from operations.save_project_smells import save_detected_different_smells_frequency_in_projects
from operations.save_project_smells import save_smells_categorized_according_to_project_type

from operations.list_csv_contents import list_csv_contents

from operations.save_smell_frequency import save_smell_frequency
from operations.show_detection_result import show_detection_result
from operations.individual_smell_introduction import individual_smell_introduction_in_total_number_of_projects

from operations.save_project_smells import save_total_smell_counts_in_projects
from operations.save_project_smells import save_unique_smell_counts_in_projects
from operations.open_smell_loc_in_code import open_smell_location 


class RunDetectionOnSourceCodeFolder():

    def __init__(self, folder_name, print_ast_tree = False, print_tokens = False):
        
        self.total_src_file_count = 0
        self.code_folder_name = folder_name
        self.should_print_tokens = print_tokens
        self.should_print_ast_tree = print_ast_tree


    def show_total_src_file_count(self):
        print('')
        print('----------------- Result -----------------')
        print('total file counted : '+str(self.total_src_file_count))
        

    def show_categories_in_project_descriptions(self):
        unique_names = []
        projects = list_csv_contents('./project-descriptions.csv')
        projects.pop(0)

        for project in projects:
            if project[2] not in unique_names:
                unique_names.append(project[2])

        for name in unique_names:
            print(name)


    def clear_log_files(self):
        for root, dirs, log_files in os.walk('./logs/'):    
            for log_file in log_files:
                with open(os.path.join(root, log_file), 'w') as fp: 
                    fp.close()


    def detect_smells_in_tokens(self, project_name,src_file):
        try:
            fp = open("logs/tokens.txt", "r")
            tokens = fp.read()
            
            fp.close()
            detection(tokens, project_name, src_file)
        
        except Exception as error:
            print(str(error))


    def analyze_ast_tree(self, code, src_file):
        try:
            tree = ast.parse(code, type_comments = True)
            
            analyzer = Analyzer()
            analyzer.visit(tree)
            analyzer.refine_tokens()
            analyzer.write_tokens_to_file()
            
            if self.should_print_ast_tree is True:
                for node in tree.body:
                    print(ast.dump(node))

            if self.should_print_tokens is True: 
                analyzer.print_statements()

            self.total_src_file_count += 1
            
        except Exception as error:
            print(str(error)) 


    def read_src_code(self, root, project_name, src_file):
        try: 
            with open(os.path.join(root, src_file), "r") as src_file:     
                code = None
                
                try: 
                    src_file = open(src_file.name, 'r')
                    code = src_file.read()
                    
                except Exception as error:  
                    print(str(error))
                    
                if code is not None: 
                    self.analyze_ast_tree(code, src_file)
                    self.detect_smells_in_tokens(project_name, src_file)
        
        except Exception as error: 
            print(str(error))


    def analyze_code_folder(self):
        project_name = None

        for root, dirs, files in os.walk(self.code_folder_name):
            copied_root = copy.deepcopy(root)
            project_name = copied_root.split('/')[3]
            should_skip = False

            for part in copied_root.split('/'):
                if part.find('test') != -1:
                    should_skip = True

            if should_skip is False:
                for src_file in files:

                    if src_file.lower().find('test') == -1:
                        if os.path.splitext(src_file)[-1] == '.py':  
                            self.read_src_code(root, project_name, src_file)
    

    def run_analyze_code_folder(self):
        self.clear_log_files()    

        self.analyze_code_folder()
        self.show_total_src_file_count()
        
        show_detection_result() #must thaka lagbe #clear
        save_smell_frequency() #must thaka lagbe #clear
        save_detected_different_smells_frequency_in_projects() #must thaka lagbe #clear
        individual_smell_introduction_in_total_number_of_projects() #must thaka lagbe 
        
        save_total_smell_counts_in_projects()
        save_unique_smell_counts_in_projects()
        save_smells_categorized_according_to_project_type()
