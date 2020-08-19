from operations.actionUponDetection import actionUponDetection

def detect(token, project_name, srcFile):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("exceptionHandler"): exceptionHandler = token["exceptionHandler"]
    
    unwantedHandlers = ['continue','pass']
    
    if tokenType == "exception_handle" and exceptionHandler in unwantedHandlers: 
        actionUponDetection(project_name, srcFile, lineno, 'ignore_except_block', 'ignore except block')
            