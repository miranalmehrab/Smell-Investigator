from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]

    httpLibs = ['httplib.urlretrieve', 'urllib', 'requests.get']
    
    if tokenType=="function_call" and name in httpLibs:
        
        if args and args[0].split("://")[0] != "https":
            actionUponDetection(srcFile, lineno, 'use_of_http', 'use of HTTP without TLS')