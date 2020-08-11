import ast
import glob
from os import system, name 
from parse import Analyzer
from detection.detection import detection

def runAnalyzer(srcCode):
        
    tree = ast.parse(srcCode, type_comments=True)
    # print(ast.dump(tree,include_attributes=True))
    print(ast.dump(tree))

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.checkUserInputsInFunctionArguments()
    analyzer.refineTokens()
    analyzer.printStatements()
    f = open("tokens.txt", "r")
    detection(f.read())



def testFromTestCodeFolder():
    srcFiles =  glob.glob("test-codes/*.py")
    for srcFile in srcFiles:

        print('File number - '+str(fileCounter)+': '+srcFile.name)    
        fileCounter = fileCounter + 1
        srcFile = open(srcFile, 'r')
        srcCode = srcFile.read()
        runAnalyzer(srcCode)


def testFromSrcCodesFolder():
    
    folderNum = 220
    srcFiles =  glob.glob("src-codes/srcs-"+str(folderNum)+"/*.py")
    fileCounter = 0

    for srcFile in srcFiles:
        
        print('File number - '+str(fileCounter)+': '+srcFile.name)    
        fileCounter = fileCounter + 1
        srcFile = open(srcFile, 'r')
        srcCode = srcFile.read()
        runAnalyzer(srcCode)


def testSingleSrcCodeFile():
    # srcFile = open('src.py', 'r')
    # srcFile = open('test-codes/function-def.py', 'r')
    # srcFile = open('test-codes/var-assign.py', 'r')
    # srcFile = open('test-codes/marshal.py', 'r')
    # srcFile = open('test-codes/eval.py', 'r')
    srcFile = open('test-codes/yaml.py', 'r')


    srcCode = srcFile.read()
    runAnalyzer(srcCode)
    

def main():
    # testFromSrcCodesFolder()
    # testFromTestCodeFolder()
    testSingleSrcCodeFile()
        

if __name__ == "__main__":
    main()
