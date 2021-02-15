import os
import ast

from analyzer import Analyzer
from detection.detection import detection

class RunOnSingleSourceCode():

    def __init__(self, file_name = None, print_ast_tree = False, print_tokens = False, code_snippet = None):
        self.src_file_name = file_name
        self.code_snippet = code_snippet
        self.should_print_tokens = print_tokens
        self.should_print_ast_tree = print_ast_tree
        

    def clear_log_files(self):
        for root, dirs, log_files in os.walk('./logs/'):    
            for log_file in log_files:
                with open(os.path.join(root, log_file), 'w') as fp: 
                    fp.close()


    def detect_smells_in_tokens(self, project_name,src_file):
        try:
            file_pointer = open("logs/tokens.txt", "r")
            tokens = file_pointer.read()
            
            file_pointer.close()
            detection(tokens, project_name, src_file)
        except Exception as error:
            print(str(error))


    def analyze_ast_tree(self, code):
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
            
        except Exception as error:
            print(str(error)) 


    def read_src_code(self, root, project_name, src_file):
        try: 
            with open(os.path.join(root, src_file), "r") as src_file:     
                code = None
                
                try: 
                    src_file = open(src_file.name, 'r')
                    code = src_file.read()
                    src_file.close()

                except Exception as error: 
                    print(str(error))
                    
                if code is not None: 
                    self.analyze_ast_tree(code)
                    self.detect_smells_in_tokens(project_name, src_file)
        
        except Exception as error:
            print(str(error))
            

    def run_analyzer_on_code_snippet(self):
        try:
            self.analyze_ast_tree(self.code_snippet)
            self.detect_smells_in_tokens('', '')
        
        except Exception as error: 
            print(str(error))
        

    def analyze_single_code(self):
        self.clear_log_files()

        if self.src_file_name is not None: 
            self.read_src_code('', '', self.src_file_name)
        
        else: self.run_analyzer_on_code_snippet()