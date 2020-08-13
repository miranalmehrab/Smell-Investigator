from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]
    if token.__contains__("hasInputs"): hasInputs = token["hasInputs"]

    unwantedMethods = ['execution.query']
    
    if tokenType == "function_call" and name in unwantedMethods and args and hasInputs:
        actionUponDetection(srcFile, lineno, 'sql_injection', 'sql injection')
        
