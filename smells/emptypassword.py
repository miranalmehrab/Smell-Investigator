from operations.savewarnings import saveWarnings

def detect(token):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("value"): value = token["value"]
    
    commonPasswords = ['password','pass','pwd','userPassword','PASSWORD','PASS','PWD','USERPWD']
    
    if tokenType == "variable" and name in commonPasswords and value == None:
        warning = 'empty password'
        saveWarnings(warning,str(lineno))
        print(warning+ ' at line '+ str(lineno))

    elif tokenType == "variable" and name in commonPasswords and len(value) == 0: 
        warning = 'empty password'
        saveWarnings(warning,str(lineno))
        print(warning+ ' at line '+ str(lineno))
    
    elif tokenType == "comparison":

        if token.__contains__("pairs"):
            for pair in token["pairs"]:
                
                if pair[0] in commonPasswords and len(pair[1]) == 0:

                    warning = 'emplty password'
                    saveWarnings(warning,str(lineno))
                    
                    print(warning+ ' at line '+ str(lineno))

                elif pair[1] in commonPasswords and len(pair[0]) == 0:

                    warning = 'emplty password'
                    saveWarnings(warning,str(lineno))
                    
                    print(warning+ ' at line '+ str(lineno))
