from operations.actionUponDetection import actionUponDetection

def detect(token, project_name, srcFile) :

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]
    if token.__contains__("hasInputs"): containsUserInput =  token["hasInputs"]

    
    if tokenType == "variable":
        if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
        if token.__contains__("args"): args = token["args"]
        if valueSrc == "exec" and len(args) > 0: actionUponDetection(project_name, srcFile, lineno, 'exec_used', 'exec used')

    elif tokenType == "function_call":
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
        if name == "exec" and len(args) > 0: actionUponDetection(project_name, srcFile, lineno, 'exec_used', 'exec used')
    
    elif tokenType == "function_def":
        if token.__contains__("return"): funcReturn  = token["return"]
        if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
        if funcReturn == "exec" and len(returnArgs) > 0: actionUponDetection(project_name, srcFile, lineno, 'exec_used', 'exec used')