from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("value"): value = token["value"]
    if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
    
    commonUserName = ['name','user','username','usrname','usr','role','USER','USERNAME','USR']
    commonPassword = ['password','pass','pwd','userPassword','PASSWORD','PASS','PWD','USERPWD']

    if tokenType == "variable" and valueSrc == "initialized" and (name in commonUserName or name in commonPassword) and value != None and len(value)>0 : 
        actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret')
        
    elif tokenType == "comparison" and token.__contains__("pairs"):

        for pair in token["pairs"]:        
            if pair[0] in commonUserName or pair[0] in commonPassword and len(pair[1]) > 0: actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret')
            elif pair[1] in commonUserName or pair[1] in commonPassword and len(pair[0]) > 0: actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret')
                