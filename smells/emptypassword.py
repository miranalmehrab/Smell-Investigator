from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("value"): value = token["value"]
    
    commonPasswords = ['password','pass','pwd','userPassword','PASSWORD','PASS','PWD','USERPWD']
    
    print(token)

    if tokenType == "variable" and name in commonPasswords and value == None: actionUponDetection(srcFile, lineno, 'empty_password', 'empty password')
    
    elif tokenType == "variable" and name in commonPasswords and len(value) == 0: actionUponDetection(srcFile, lineno, 'empty_password', 'empty password')

    elif tokenType == "comparison" and token.__contains__("pairs"):

        for pair in token["pairs"]:
            if pair[0] in commonPasswords and len(pair[1]) == 0: actionUponDetection(srcFile, lineno, 'empty_password', 'empty password')
            elif pair[1] in commonPasswords and len(pair[0]) == 0: actionUponDetection(srcFile, lineno, 'empty_password', 'empty password')
                
