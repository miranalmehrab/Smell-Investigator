from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("value"): value = token["value"]
    
    restrictedNames = ['debug', 'DEBUG', 'DEBUG_PROPAGATE_EXCEPTIONS']
    
    if tokenType == "variable" and name in restrictedNames and value: actionUponDetection(srcFile, lineno, 'debug_true', 'debug set true')

    elif tokenType == "function_call":
        if token.__contains__("keywords"): keywords = token["keywords"]
        
        for keyword in keywords:
            if(keyword[0] in restrictedNames and keyword[1]): actionUponDetection(srcFile, lineno, 'debug_true', 'debug set true')
                