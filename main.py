import ast
import glob
from os import system, name 

from parse import Analyzer
from detection.detection import detection

from operations.clearFileContent import clearFileContent
from operations.saveParsingExceptions import saveParsingExceptions
from operations.compareDetectionAccuracy import compareDetectionAccuracy

def detectSmellsFromTokens(srcFile):
    f = open("tokens.txt", "r")
    detection(f.read(), srcFile)


def analyzeSrcCode(srcCode, srcFile):
    
    tree = ast.parse(srcCode, type_comments=True)
    # print(ast.dump(tree,include_attributes=True))
    # print(ast.dump(tree))

    analyzer = Analyzer()
    analyzer.visit(tree)

    analyzer.checkUserInputsInFunctionArguments()
    analyzer.refineTokens()
    analyzer.writeToFile()
    
    # analyzer.printStatements()
    # analyzer.printStatements('comparison')
    # analyzer.printStatements('list', 'dict', 'set')
    # analyzer.printStatements('variable', 'list', 'tuple', 'dict')



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
    clearFileContent('logs/parsingExceptions.csv')
    clearFileContent('logs/detectionExceptions.csv')

    numberOfParsingError = 0
    
    for srcCodeFolder in range(0, 588):
        
        srcFiles = glob.glob("src-codes/srcs-"+str(srcCodeFolder)+"/*.py")
        
        for srcFile in srcFiles:    
            
            srcFile = open(srcFile, 'r')
            srcCode = srcFile.read()
            
            try:
                analyzeSrcCode(srcCode, srcFile)
            except Exception as error:
                numberOfParsingError += 1
                saveParsingExceptions(str(error) +str(numberOfParsingError), srcFile)

            detectSmellsFromTokens(srcFile)

    compareDetectionAccuracy()




def testSingleSrcCodeFile():

    clearFileContent('detected_smells.csv')
    clearFileContent('logs/parsingExceptions.csv')
    clearFileContent('logs/detectionExceptions.csv')

    fileName = 'src.py'
    # fileName = 'test-codes/function-def.py'
    # fileName = 'test-codes/var-assign.py'
    # fileName = 'test-codes/marshal.py'
    # fileName = 'test-codes/eval.py'
    # fileName = 'test-codes/yaml.py'

    srcFile = open(fileName,'r')
    srcCode = srcFile.read()
    
    analyzeSrcCode(srcCode,fileName)
    detectSmellsFromTokens(srcFile)
    compareDetectionAccuracy()
    

def main():
    testFromSrcCodesFolder()
    # testFromTestCodeFolder()
    # testSingleSrcCodeFile()
        

if __name__ == "__main__":
    main()
