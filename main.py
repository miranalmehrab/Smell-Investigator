import os
import ast
import copy 
import glob

from parse import Analyzer
from detection.detection import detection

from operations.clearFileContent import clearFileContent
from operations.showResult import show_results
from operations.projectSmell import save_project_smells

def detect_smells_in_tokens(project_name,src_file):
    f = open("tokens.txt", "r")
    detection(f.read(), project_name, src_file)


def parse_code(code, src_file):
    try:
        tree = ast.parse(code, type_comments=True)
        # print(ast.dump(tree, include_attributes = True))
        # print(ast.dump(tree))

        analyzer = Analyzer()
        analyzer.visit(tree)

        analyzer.checkUserInputsInFunctionArguments()
        analyzer.refineTokens()
        analyzer.delete_incomplete_tokens()
        # analyzer.makeTokensByteFree()
        analyzer.writeToFile()
        
        # analyzer.printStatements()
        # analyzer.printStatements('comparison')
        
    except Exception as error:
        print(str(error)) 


def analyze_code(root, project_name, src_file):
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
    
    file_counter = 0
    project_counter = 0
    project_name = None

    for root, dirs, files in os.walk('./../unzips/'):
        project_name = copy.deepcopy(root)
        project_name = project_name.split('/')[3]
        
        for src_file in files:
            if os.path.splitext(src_file)[-1] == '.py':   
                analyze_code(root, project_name, src_file)
                file_counter += 1
    
    print('')
    print('------------------------------ Result ------------------------------ ')
    print('total file counted : '+str(file_counter))
    
    show_results()
    # save_project_smells()


def analyze_single_code():

    file_name = './src.py'
    analyze_code('', file_name)
    show_results()


# each project -> smells -> count -> problems

def main():
    clearFileContent('logs/bugFix.csv')
    clearFileContent('detected_smells.csv')
    clearFileContent('logs/projectSmells.csv')
    clearFileContent('logs/parsingExceptions.csv')
    clearFileContent('logs/detectionExceptions.csv')
    clearFileContent('logs/tokenLoadingExceptions.csv')

    # analyze_single_code()
    analyze_code_folder()
        

if __name__ == "__main__":
    main()
