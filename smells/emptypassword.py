from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("value"): value = token["value"]
    
    commonPasswords = ['password','passwords','pass','pwd','userpassword','userpwd', 'userpass', 'pass_no', 'pass-no', 'user-pass', 'upass']
    
    if tokenType == "variable" and name in commonPasswords and value is not None: 
        actionUponDetection(srcFile, lineno, 'empty_password', 'empty password')


    elif tokenType == "variable" and name in commonPasswords and len(value) == 0: 
        actionUponDetection(srcFile, lineno, 'empty_password', 'empty password')


    elif tokenType == "comparison" and token.__contains__("pairs"):
        pairs = token["pairs"]

        for pair in pairs:
            if len(pair) == 2 and pair[0] in commonPasswords and len(pair[1]) == 0: 
                actionUponDetection(srcFile, lineno, 'empty_password', 'empty password')
            
            elif len(pair) == 2 and pair[1] in commonPasswords and len(pair[0]) == 0: 
                actionUponDetection(srcFile, lineno, 'empty_password', 'empty password')
    

    elif tokenType == "function_call" and token.__contains__('keywords'):
        for keyword in token['keywords']:
            if len(keyword) == 2 and keyword[0].lower() in commonPasswords and len(keyword[1]) == 0: 
                actionUponDetection(srcFile, lineno, 'empty_password', 'empty password')
