from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    
    if tokenType == "variable":
        if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
        if token.__contains__("args"): args = token["args"]
        if valueSrc == "eval" and args != None: actionUponDetection(srcFile, lineno, 'shell_injection', 'eval used')

    elif tokenType == "function_call":
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
        if name == "eval" and args != None: actionUponDetection(srcFile, lineno, 'shell_injection', 'eval used')
    
    elif tokenType == "function_def":
        if token.__contains__("return"): funcReturn  = token["return"]
        if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
        if funcReturn == "eval" and returnArgs!= None: actionUponDetection(srcFile, lineno, 'shell_injection', 'eval used')