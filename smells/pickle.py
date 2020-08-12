from operations.savewarnings import saveWarnings
from operations.saveascsv import saveAsCSV

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    
    if tokenType == "variable":
        if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
        if token.__contains__("args"): args = token["args"]
        if valueSrc == "pickle.load" and args != None: printWarning(lineno)

    elif tokenType == "function_call":
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
        if name == "pickle.load" and args != None: printWarning(lineno)
    
    elif tokenType == "function_def":
        if token.__contains__("return"): funcReturn  = token["return"]
        if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
        if funcReturn == "pickle.load" and returnArgs!= None: printWarning(lineno)
    

def printWarning(lineno):
    warning = 'Pickle used'
    print(warning+ ' at line '+ str(lineno))

    saveAsCSV('pickle_used', srcFile)
    saveWarnings(warning,str(lineno))
