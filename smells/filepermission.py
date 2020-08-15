from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]

    unwantedMethods = ['os.chmod', 'chmod']
    unwantedParams = ['0x777', '0x757', '0x755','stat.S_IRWXO','stat.S_IROTH','stat.S_IWOTH','stat.S_IXOTH']

    if tokenType == "function_call" and name in unwantedMethods:
        for arg in args:
            if arg in unwantedParams: actionUponDetection(srcFile, lineno, 'bad_file_permissions', 'bad file permission')
    
    elif tokenType == 'function_call' and name == 'subprocess.call':
        for arg in args:
            if arg in unwantedMethods: actionUponDetection(srcFile, lineno, 'bad_file_permissions', 'bad file permission')
