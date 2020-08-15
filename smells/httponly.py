from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]

    httpLibs = ['httplib.urlretrieve', 'urllib.urlopen', 'requests.get']
    
    if tokenType == "variable" and token.__contains__("valueSrc") and token.__contains__("args"):
        
        args = token['args']
        valueSrc = token['valueSrc']

        if valueSrc in httpLibs:
            if len(args)>0 and args[0].split("://")[0] != "https" : actionUponDetection(srcFile, lineno, 'use_of_http', 'use of HTTP without TLS')

    if tokenType == "function_call" and name in httpLibs:
        if len(args) > 0 and args[0].split("://")[0] != "https" : actionUponDetection(srcFile, lineno, 'use_of_http', 'use of HTTP without TLS')

