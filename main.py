import ast
import glob
from os import system, name 
from parse import Analyzer
from detection.detection import detection

def runAnalyzer(srcCode, srcFile):
        
    tree = ast.parse(srcCode, type_comments=True)
    # print(ast.dump(tree,include_attributes=True))
    print(ast.dump(tree))

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.checkUserInputsInFunctionArguments()
    analyzer.refineTokens()
    analyzer.printStatements()
    f = open("tokens.txt", "r")
    detection(f.read(), srcFile)



def testFromTestCodeFolder():
    srcFiles =  glob.glob("test-codes/*.py")
    for srcFile in srcFiles:

        print('File number - '+str(fileCounter)+': '+srcFile)    
        fileCounter = fileCounter + 1
        srcFile = open(srcFile, 'r')
        srcCode = srcFile.read()
        runAnalyzer(srcCode, srcFile)


def testFromSrcCodesFolder():
    
    folderNum = 2
    srcFiles =  glob.glob("src-codes/srcs-"+str(folderNum)+"/*.py")
    fileCounter = 0

    for srcFile in srcFiles:
        
        print('File number - '+str(fileCounter)+': '+srcFile)    
        fileCounter = fileCounter + 1
        srcFile = open(srcFile, 'r')
        srcCode = srcFile.read()
        runAnalyzer(srcCode, srcFile)


def testSingleSrcCodeFile():
    fileName = 'src.py'
    srcFile = open('src.py', 'r')
    # srcFile = open('test-codes/function-def.py', 'r')
    # srcFile = open('test-codes/var-assign.py', 'r')
    # srcFile = open('test-codes/marshal.py', 'r')
    # srcFile = open('test-codes/eval.py', 'r')
    # srcFile = open('test-codes/yaml.py', 'r')

    srcCode = srcFile.read()
    runAnalyzer(srcCode,fileName)
    

def main():
    # testFromSrcCodesFolder()
    # testFromTestCodeFolder()
    testSingleSrcCodeFile()
        

if __name__ == "__main__":
    main()
