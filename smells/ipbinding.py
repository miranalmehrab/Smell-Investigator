from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]
        
    unwantedmethod = ['socket.socket.bind']
    unwantedparam = ['0.0.0.0','192.168.0.1']
        
    if tokenType == "function_call" and name in unwantedmethod :
        
        for arg in args:
            if arg in unwantedparam: actionUponDetection(srcFile, lineno, 'hardcoded_interface', 'Harcoded ip address binding used')
                
