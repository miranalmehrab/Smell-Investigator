from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:

        bindingMethods = ['socket.socket.bind', 'socket.socket.connect']
        binding_methods_relaxed = ['.bind', '.connect']
        
        if token["type"] == "variable" and token.__contains__('valueSrc') and token.__contains__('args'):
            if is_valid_ip(token['value']):
                action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token)
            
            
            args = token['args']
            valueSrc = token['valueSrc']
            
            if valueSrc in bindingMethods and len(args) > 0 and is_valid_ip(args[0]):
                action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token) 

        elif token["type"] == "function_call" and token['name'] in bindingMethods:
            args = token['args']

            if len(args) > 0 and is_valid_ip(args[0]):
                action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token)
        
        elif token['type'] == 'function_def' and token.__contains__('return') and token['return'] is not None and isinstance(token['return'], list) and len(token['return']) > 1:
            for method in binding_methods_relaxed:
                if isinstance(token['return'][0], str) and method in token['return'][0] and is_valid_ip(token['return'][1]):
                     action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token)
    
    except Exception as error: save_token_detection_exception('ip binding detection  '+str(error)+'  '+ str(token), src_file)

def is_valid_ip(ip):
    if isinstance(ip,str) is False: return False
    elif ip is None: return False
    elif ip == '0.0.0.0': return True
    elif ip == '8.8.8.8': return True
    elif ip == '': return True
    else:
        parts = ip.split('.')
        if len(parts) != 4: return False
        
        for part in parts:
            if int(part) < 0 or int(part) > 255: return False

    return True 

def is_valid_port(port):
    if isinstance(port, str) and port.isdigit() is False: return False
    elif int(port) > 0 and int(port) < 65536: return True
    else: return False