from operations.savewarnings import saveWarnings

def detect(token):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("firstBlock"): firstBlock = token["firstBlock"]
    
    unwantedArgs = ['continue','pass']
        
    if tokenType == "except_statement" and firstBlock in unwantedArgs:
            
            warning = 'ignore except block'
            saveWarnings(warning,str(lineno))
            print(warning+ ' at line '+ str(lineno))
