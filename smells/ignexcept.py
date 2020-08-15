from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("exceptionHandler"): exceptionHandler = token["exceptionHandler"]
    
    unwantedArgs = ['continue','pass']
    
    if tokenType == "exception_handle" and exceptionHandler in unwantedArgs: 
        print(token)
        actionUponDetection(srcFile, lineno, 'ignore_except_block', 'ignore except block')
            