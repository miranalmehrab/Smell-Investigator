from operations.action_upon_detection import action_upon_detection

def detect(token, project_name, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    
    httpLibs = ['requests.get','requests.Session.get']
    
    if tokenType == "function_call" and name in httpLibs and token.__contains__("keywords"):
        keywords = token["keywords"]

        for keyword in keywords:
            if keyword[0] == 'verify' and keyword[1] is False: 
                action_upon_detection(project_name, srcFile, lineno, 'no_certification_validation', 'TLS is not verified', token)

