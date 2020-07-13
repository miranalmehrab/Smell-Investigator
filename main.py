import ast
from parse import Analyzer
from detection.detection import detection

def main():
    srcFile = open('src.py', 'r')
    srcCode = srcFile.read()
    
    tree = ast.parse(srcCode, type_comments=True)
    # print(ast.dump(tree,include_attributes=True))
    # print(ast.dump(tree))

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.findUserInputInFunction()
    analyzer.printStatements()

    f = open("tokens.txt", "r")
    detection(f.read())


if __name__ == "__main__":
    main()
