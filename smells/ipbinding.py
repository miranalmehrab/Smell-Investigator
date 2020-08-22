from operations.actionUponDetection import actionUponDetection

def detect(token, project_name, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]
        
    bindingMethods = ['socket.socket.bind']
    
    if tokenType == "variable" and token.__contains__('valueSrc') and token.__contains__('args'):
        args = token['args']
        valueSrc = token['valueSrc']
        
        if valueSrc in bindingMethods and len(args) > 0 and is_valid_ip(args[0]):
            actionUponDetection(project_name, srcFile, lineno, 'hardcoded_ip_binding', 'Harcoded ip address binding used') 

    elif tokenType == "function_call" and name in bindingMethods:
        
        if len(args) > 0 and is_valid_ip(args[0]): 
            actionUponDetection(project_name, srcFile, lineno, 'hardcoded_ip_binding', 'Harcoded ip address binding used')
                
def is_valid_ip(ip):
    parts = ip.split('.')
    
    if len(parts) != 4: return False
    for part in parts:
        if int(part) < 0 or int(part) > 255: return False

    return True    