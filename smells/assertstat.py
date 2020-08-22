from operations.actionUponDetection import actionUponDetection
 
def detect(token, project_name, srcFile) :

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    
    if tokenType == "assert" and token.__contains__("left") and token.__contains__("comparators"):
        left = token["left"]
        comparators = token["comparators"]
        
        if left is not None and len(comparators) > 0:
            actionUponDetection(project_name, srcFile, lineno, 'assert_used', 'assert statement')

    elif tokenType == "assert" and token.__contains__('func'):
        func = token['func']
        args = token['args']
        
        if func is not None:
            actionUponDetection(project_name, srcFile, lineno, 'assert_used', 'assert statement')