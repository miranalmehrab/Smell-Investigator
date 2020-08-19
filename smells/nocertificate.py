from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    
    httpLibs = ['requests.get','requests.Session.get']
    
    if tokenType == "function_call" and name in httpLibs and token.__contains__("keywords"):
        keywords = token["keywords"]

        for keyword in keywords:
            if keyword[0] == 'verify' and keyword[1] is False: 
                actionUponDetection(srcFile, lineno, 'no_certification_validation', 'TLS is not verified')

