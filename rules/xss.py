from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        
        if tokenType == "variable":
            if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
            if token.__contains__("args"): args = token["args"]
            if is_insecure_method(valueSrc) and len(args) > 0: 
                action_upon_detection(project_name, src_file, lineno, 'cross site scripting', 'cross site scripting', token)

        elif tokenType == "function_call":
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("args"): args = token["args"]
            
            if is_insecure_method(name): 
                action_upon_detection(project_name, src_file, lineno, 'cross site scripting', 'cross site scripting', token)
            
            # for arg in args:
            #     if is_insecure_method(arg):
            #         action_upon_detection(project_name, src_file, lineno, 'cross site scripting', 'cross site scripting', token)

        elif tokenType == "function_def" and token.__contains__("return") and token["return"] is not None:
            for func_return in token["return"]:
                if is_insecure_method(func_return): 
                    action_upon_detection(project_name, src_file, lineno, 'cross site scripting', 'cross site scripting', token)
            
    except Exception as error: save_token_detection_exception('xss detection  '+str(error)+'  '+ str(token), src_file)

def is_insecure_method(name):
    if name is None: return False
    elif isinstance(name, str) is False: return False
    
    insecureMethods = ['django.utils.safestring.mark_safe', 'mark_safe']
    for method in insecureMethods:
        if method in name: return True
 
    return False