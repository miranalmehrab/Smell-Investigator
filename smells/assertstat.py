from operations.actionUponDetection import actionUponDetection
 

def detect(token, srcFile) :

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("left"): left = token["left"]
    if token.__contains__("comparators"): comparators = token["comparators"]

    if (tokenType == "assert" and left!= None and comparators!=None): actionUponDetection(srcFile, lineno, 'assert_used', 'assert statement')