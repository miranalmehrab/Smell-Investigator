from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("value"): value = token["value"]
    
    restrictedNames = ['debug', 'DEBUG', 'DEBUG_PROPAGATE_EXCEPTIONS']
    
    if tokenType == "variable" and name in restrictedNames and value == True: actionUponDetection(srcFile, lineno, 'debug_true', 'debug set true')

    elif tokenType == "function_call" and token.__contains__("keywords"):
        for keyword in token["keywords"]:
            if(keyword[0] in restrictedNames and keyword[1] == True): actionUponDetection(srcFile, lineno, 'debug_true', 'debug set true')

    elif tokenType == "dict" and token.__contains__("keys") and token.__contains__("values"): 
        pairs = [list(a) for a in zip(token["keys"], token["values"])]
        
        for pair in pairs: 
            if pair[0] in restrictedNames and pair[1] == True: actionUponDetection(srcFile, lineno, 'debug_true', 'debug set true')
