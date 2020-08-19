import os
import ast
import glob

from parse import Analyzer
from detection.detection import detection

from operations.clearFileContent import clearFileContent
from operations.showResult import show_results


def detect_smells_in_tokens(src_file):
    f = open("tokens.txt", "r")
    detection(f.read(), src_file)


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


def analyze_code(root, src_file):
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
                detect_smells_in_tokens(src_file)
    
    except Exception as error: 
        print(str(error))
        

def analyze_code_folder():
    
    file_counter = 0
    for root, dirs, files in os.walk('./../unzips/'):
        for src_file in files:
            if os.path.splitext(src_file)[-1] == '.py':   
                analyze_code(root, src_file)
                file_counter += 1
    
    print('')
    print('------------------------------ Result ------------------------------ ')
    print('total file counted : '+str(file_counter))
    
    show_results()


def analyze_single_code():

    file_name = './src.py'
    analyze_code('', file_name)
    show_results()


def main():
    clearFileContent('logs/bugFix.csv')
    clearFileContent('detected_smells.csv')
    clearFileContent('logs/parsingExceptions.csv')
    clearFileContent('logs/detectionExceptions.csv')
    clearFileContent('logs/tokenLoadingExceptions.csv')

    # analyze_single_code()
    analyze_code_folder()
        

if __name__ == "__main__":
    main()
