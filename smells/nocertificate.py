from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("keywords"): keywords = token["keywords"]

    httpLibs = ['requests.get','requests.Session.get']
    
    if tokenType == "function_call" and name in httpLibs and len(keywords)>0:
        for keyword in keywords:
            if keyword[0] == 'verify' and keyword[1] == False: actionUponDetection(srcFile, lineno, 'no_certification_validation', 'Omission of TLS verification')

