from operations.action_upon_detection import action_upon_detection

def detect(token, project_name, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]

    httpLibs = ['httplib.urlretrieve', 'urllib.urlopen', 'requests.get']
    
    if tokenType == "variable" and token.__contains__("valueSrc") and token.__contains__("args"):
        args = token['args']
        valueSrc = token['valueSrc']

        if valueSrc in httpLibs and len(args) > 0:
            if args[0].split("://")[0] != "https": 
                action_upon_detection(project_name, srcFile, lineno, 'http_without_tls', 'use of HTTP without TLS')

    if tokenType == "function_call" and name in httpLibs:
        if len(args) > 0 and args[0].split("://")[0] != "https": 
            action_upon_detection(project_name, srcFile, lineno, 'http_without_tls', 'use of HTTP without TLS')

