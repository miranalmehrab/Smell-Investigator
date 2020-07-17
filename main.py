import ast
import glob
from parse import Analyzer
from detection.detection import detection

def runAnalyzer(srcCode):
        
    tree = ast.parse(srcCode, type_comments=True)
    # print(ast.dump(tree,include_attributes=True))
    # print(ast.dump(tree))

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.findUserInputInFunction()
    # analyzer.printStatements()
    analyzer.printFilteredStatement("function_call")
    # f = open("tokens.txt", "r")
    # detection(f.read())



def main():
    srcFile = open('test-codes/expression.py', 'r')
    # srcFile = open('test-codes/var-assign.py', 'r')
    
    srcCode = srcFile.read()
    runAnalyzer(srcCode)

    # folderNumber = 0
    # srcFiles =  glob.glob("src-codes/srcs-"+str(folderNumber)+"/*.py")
    # srcFiles =  glob.glob("test-codes/*.py")

    # fileCounter = 0
    # for srcFile in srcFiles:
    #     fileCounter = fileCounter + 1
    #     srcFile = open(srcFile, 'r')
    #     srcCode = srcFile.read()

    #     while True:

    #         print('File number - '+str(fileCounter)+': '+srcFile.name)    
    #         runAnalyzer(srcCode)
    
    #         # print('Loop?')
    #         # loop = input('Y/N:')
    #         # if loop == 'N' or loop == 'n': break
    #         break
    #     # print('Analyze Next File?')
    #     # next = input('Y/N: ')
    #     # if next == 'N' or next == 'n': break
        

if __name__ == "__main__":
    main()
