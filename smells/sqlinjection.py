from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]
    if token.__contains__("hasInputs"): hasInputs = token["hasInputs"]

    unwantedMethods = ['execution.query', 'connection.cursor.execute']
    
    if tokenType == "function_call" and name in unwantedMethods and len(args) > 0 and hasInputs:
        actionUponDetection(srcFile, lineno, 'sql_injection', 'sql injection')
        
