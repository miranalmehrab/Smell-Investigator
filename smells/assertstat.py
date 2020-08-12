from operations.savewarnings import saveWarnings
from operations.saveascsv import saveAsCSV 

def detect(token, srcFile) :

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("left"): left = token["left"]
    if token.__contains__("comparators"): comparators = token["comparators"]

    if (tokenType == "assert" and left!= None and comparators!=None):
        warning = 'assert statement'
        print(warning+ ' at line '+ str(lineno))
        
        saveAsCSV('assert_used', srcFile)
        saveWarnings(warning,str(lineno))
