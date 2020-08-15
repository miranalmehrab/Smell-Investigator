from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]
        
    unwantedmethod = ['socket.socket.bind']
        
    if tokenType == "function_call" and name in unwantedmethod :
        if len(args) > 0 and is_valid_ip(args[0]): actionUponDetection(srcFile, lineno, 'hardcoded_ip', 'Harcoded ip address binding used')
                
def is_valid_ip(ip):
    
    parts = ip.split('.')
    if len(parts) != 4: return False
    
    for part in parts:
        if not 0<= int(part) <=255: return False

    return True    