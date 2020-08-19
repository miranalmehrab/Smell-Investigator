from operations.actionUponDetection import actionUponDetection
 
def detect(token, project_name, srcFile) :

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("left"): left = token["left"]
    if token.__contains__("comparators"): comparators = token["comparators"]

    if tokenType == "assert" and left is not None and len(comparators) > 0: 
        actionUponDetection(project_name, srcFile, lineno, 'assert_used', 'assert statement')