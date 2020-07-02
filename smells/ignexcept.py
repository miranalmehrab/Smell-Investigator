def detect(token):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("arg"): arg = token["arg"]
    
    unwantedArgs = ['continue','pass']
        
    if tokenType == "except_statement" and arg in unwantedArgs:
            warning = 'possible ignore except block at line '+ str(lineno)
            print(warning)
            