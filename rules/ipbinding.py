import re
from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:

        ip_related_names = ['ip', 'host', 'db', 'database', 'server']
        ip_binding_methods = ['socket.socket.bind', 'socket.socket.connect']
        ip_binding_methods_relaxed = ['.bind', '.connect']

        
        if token['type'] == 'variable' and token['value'] is not None and token['valueSrc'] == 'initialization':
            if is_valid_ip(token['value']):
                action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token)

            if token.__contains__('args'):
                args = token['args']

                for arg in args:
                    if is_valid_ip(arg):
                        action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token)
        
        
        if token["type"] == "function_call":
            if token.__contains__('keywords') and len(token['keywords']) > 0:
                for keyword in token['keywords']:        
                    if len(keyword) == 3 and isinstance(keyword[0], str) and keyword[0].lower() is not None and keyword[1] is not None and keyword[2] is True:    
                        if is_valid_ip(keyword[1]):
                            action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token)
            
        
            if token.__contains__('args'):
                for arg in token['args']:
                    if is_valid_ip(arg):
                        action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token)
                        break

        if token['type'] == 'function_def' and token.__contains__('return') and token['return'] is not None and isinstance(token['return'], list) and len(token['return']) > 1:
            for method in ip_binding_methods_relaxed:
                if isinstance(token['return'][0], str) and method in token['return'][0] and is_valid_ip(token['return'][1]):
                    action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token)
    

        if token['type'] == 'comparison' and token.__contains__('pairs'):
            for pair in token['pairs']:
                if len(pair) == 2 and pair[0] is not None and pair[1] is not None:
                    if is_valid_ip(pair[1]):
                        action_upon_detection(project_name, src_file, token['line'], 'hard-coded IP address bindings', 'hard-coded IP address bindings', token)
                        break       
                

    except Exception as error: save_token_detection_exception('ip binding detection  '+str(error)+'  '+ str(token), src_file)

def is_valid_ip(ip):
    if isinstance(ip,str) is False: return False
    elif ip is None: return False
    elif ip == '0.0.0.0': return True
    elif ip == '8.8.8.8': return True
    elif ':' in ip: ip = ip.split(':')[0]
    
    elif re.match(r'[_A-Za-z-]+', ip): return False
    elif re.match(r'[!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"-\+\/]+', ip): return False
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