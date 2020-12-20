from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("value"): value = token["value"]
        
        restricted_names = ['debug','debug_propagate_exceptions','propagate_exceptions','PROPAGATE_EXCEPTIONS']
        
        if tokenType == "variable" and name is not None and (name.lower() in restricted_names or has_debug_in_name(name.lower())) and value is True: 
            action_upon_detection(project_name, src_file, lineno, 'deployment with debug flag set to true', 'deployment with debug flag set to true', token)


        elif tokenType == "function_call" and token.__contains__("keywords"):
            
            for keyword in token["keywords"]:
                if(keyword[0] is not None and isinstance(keyword[0], str) and keyword[0].lower() in restricted_names and keyword[1] is True): 
                    action_upon_detection(project_name, src_file, lineno, 'deployment with debug flag set to true', 'deployment with debug flag set to true', token)


        elif tokenType == "dict" and token.__contains__("pairs"): 
            
            for pair in token['pairs']:
                if pair[0] in restricted_names and pair[1] is True: 
                    action_upon_detection(project_name, src_file, lineno, 'deployment with debug flag set to true', 'deployment with debug flag set to true', token)
    
    except Exception as error: save_token_detection_exception('debug detection  '+str(error)+'  '+ str(token), src_file)


def has_debug_in_name(var_name):
    restricted_names = ['debug','debug_propagate_exceptions','propagate_exceptions']
    
    for name in restricted_names:
        if name in var_name.lower().strip(): 
            return True
    
    return False