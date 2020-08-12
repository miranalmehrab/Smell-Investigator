from operations.savewarnings import saveWarnings
from operations.saveascsv import saveAsCSV

def detect(token, srcFile):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("value"): value = token["value"]
    
    commonPasswords = ['password','pass','pwd','userPassword','PASSWORD','PASS','PWD','USERPWD']
    
    if tokenType == "variable" and name in commonPasswords and value == None:
        warning = 'empty password'
        print(warning+ ' at line '+ str(lineno))
        
        saveAsCSV('empty_password', srcFile)
        saveWarnings(warning,str(lineno))

    elif tokenType == "variable" and name in commonPasswords and len(value) == 0: 
        warning = 'empty password'
        print(warning+ ' at line '+ str(lineno))
        
        saveAsCSV('empty_password', srcFile)
        saveWarnings(warning,str(lineno))
    
    elif tokenType == "comparison":

        if token.__contains__("pairs"):
            for pair in token["pairs"]:
                
                if pair[0] in commonPasswords and len(pair[1]) == 0:
                    warning = 'emplty password'
                    print(warning+ ' at line '+ str(lineno))
                    
                    saveAsCSV('empty_password', srcFile)
                    saveWarnings(warning,str(lineno))
                    

                elif pair[1] in commonPasswords and len(pair[0]) == 0:
                    warning = 'emplty password'
                    print(warning+ ' at line '+ str(lineno))

                    saveAsCSV('empty_password', srcFile)
                    saveWarnings(warning,str(lineno))
                    
