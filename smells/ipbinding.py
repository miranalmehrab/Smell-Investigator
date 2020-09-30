from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
            
        bindingMethods = ['socket.socket.bind', 'socket.socket.connect']
        
        if tokenType == "variable" and token.__contains__('valueSrc') and token.__contains__('args'):
            args = token['args']
            valueSrc = token['valueSrc']
            
            # if valueSrc in bindingMethods and len(args) > 0:
                # action_upon_detection(project_name, srcFile, lineno, 'hardcoded_ip_binding', 'Harcoded ip address binding used', token) 

            if valueSrc in bindingMethods and len(args) > 0 and args[0] is not None and is_valid_ip(args[0]):
                action_upon_detection(project_name, srcFile, lineno, 'hardcoded_ip_binding', 'Harcoded ip address binding used', token) 

        elif tokenType == "function_call" and name in bindingMethods:
            # action_upon_detection(project_name, srcFile, lineno, 'hardcoded_ip_binding', 'Harcoded ip address binding used', token)

            if len(args) > 1 and (args[0] is not None or args[1] is not None) and (is_valid_ip(args[0]) or is_valid_port(args[1])): 
                action_upon_detection(project_name, srcFile, lineno, 'hardcoded_ip_binding', 'Harcoded ip address binding used', token)
    
    except Exception as error: save_token_detection_exception('ip binding detection  '+str(error)+'  '+ str(token), srcFile)

def is_valid_ip(ip):
    if ip == '': return True
    else:
        parts = ip.split('.')
        if len(parts) != 4: return False
        
        for part in parts:
            if int(part) < 0 or int(part) > 255: return False

    return True 

def is_valid_port(port):
    if int(port) > 0 and int(port) < 65536: return True
    else: return False