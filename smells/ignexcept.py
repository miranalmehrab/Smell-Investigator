from operations.savewarnings import saveWarnings
from operations.saveascsv import saveAsCSV

def detect(token, srcFile):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("firstBlock"): firstBlock = token["firstBlock"]
    
    unwantedArgs = ['continue','pass']
        
    if tokenType == "except_statement" and firstBlock in unwantedArgs:
            warning = 'ignore except block'
            print(warning+ ' at line '+ str(lineno))

            saveAsCSV('ignore_except_block', srcFile)
            saveWarnings(warning,str(lineno))
