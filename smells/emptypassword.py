def detect(token):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("value"): value = token["value"]
    
    commonPasswords = ['password','pass','pwd','userPassword','PASSWORD','PASS','PWD','USERPWD']
    
    if tokenType == "variable" and name in commonPasswords and value == None:
        warning = 'possible empty password at line '+str(lineno)
        print(warning)

    elif tokenType == "variable" and name in commonPasswords and len(value) == 0: 
        warning = 'possible empty password at line '+str(lineno)
        print(warning)
