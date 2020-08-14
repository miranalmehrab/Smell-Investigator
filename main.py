import ast
import glob
from os import system, name 

from parse import Analyzer
from detection.detection import detection

from operations.clearFileContent import clearFileContent
from operations.compareDetectionAccuracy import compareDetectionAccuracy

def analyzeSrcCode(srcCode, srcFile):
    

    tree = ast.parse(srcCode, type_comments=True)
    # print(ast.dump(tree,include_attributes=True))
    # print(ast.dump(tree))

    analyzer = Analyzer()
    analyzer.visit(tree)

    analyzer.checkUserInputsInFunctionArguments()
    analyzer.refineTokens()
    analyzer.writeToFile()
    # analyzer.printStatements('variable', 'list', 'tuple', 'dict')
    # analyzer.printStatements('function_def')
    # analyzer.printStatements('comparison')
    
    f = open("tokens.txt", "r")
    detection(f.read(), srcFile)



def testFromTestCodeFolder():
    srcFiles =  glob.glob("test-codes/*.py")
    for srcFile in srcFiles:

        print('File number - '+str(fileCounter)+': '+srcFile)    
        fileCounter = fileCounter + 1
        srcFile = open(srcFile, 'r')
        srcCode = srcFile.read()
        analyzeSrcCode(srcCode, srcFile)


def testFromSrcCodesFolder():
    
    clearFileContent('detected_smells.csv')

    numberOfParsingError = 0
    for srcCodeFolder in range(0, 588):
        srcFiles = glob.glob("src-codes/srcs-"+str(srcCodeFolder)+"/*.py")
        fileCounter = 1

        for srcFile in srcFiles:
            print('File number -'+str(fileCounter)+': '+srcFile)    
            
            srcFile = open(srcFile, 'r')
            srcCode = srcFile.read()
            
            try:
                analyzeSrcCode(srcCode, srcFile)
            except:
                numberOfParsingError += 1
                print('parsing error count : ' + str(numberOfParsingError))

            fileCounter += 1

    compareDetectionAccuracy()

def testSingleSrcCodeFile():
    fileName = 'test-codes/if-test.py'
    srcFile = open(fileName, 'r')

    # srcFile = open('src.py', 'r')
    # srcFile = open('test-codes/function-def.py', 'r')
    # srcFile = open('test-codes/var-assign.py', 'r')
    # srcFile = open('test-codes/marshal.py', 'r')
    # srcFile = open('test-codes/eval.py', 'r')
    # srcFile = open('test-codes/yaml.py', 'r')

    srcCode = srcFile.read()
    analyzeSrcCode(srcCode,fileName)
    

def main():
    testFromSrcCodesFolder()
    # testFromTestCodeFolder()
    # testSingleSrcCodeFile()
        

if __name__ == "__main__":
    main()
