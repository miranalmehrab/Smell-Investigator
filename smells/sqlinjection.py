from operations.actionUponDetection import actionUponDetection

def detect(token, project_name, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]
    if token.__contains__("hasInputs"): hasInputs = token["hasInputs"]

    unwantedMethods = ['execution.query', 'connection.cursor.execute']
    
    if tokenType == "variable" and token.__contains__('valueSrc') and token.__contains__('args'):
        args = token['args']
        valueSrc = token['valueSrc']
        if valueSrc in unwantedMethods and len(args) > 0:
            actionUponDetection(project_name, srcFile, lineno, 'sql_injection', 'sql injection')
                
    elif tokenType == "function_call" and name in unwantedMethods and (len(args) > 0 or hasInputs):
        actionUponDetection(project_name, srcFile, lineno, 'sql_injection', 'sql injection')
        
