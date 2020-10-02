from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        
        insecureMethods = ['yaml.load', 'yaml.load_all']

        if tokenType == "variable":
            if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
            if token.__contains__("args"): args = token["args"]
            if valueSrc in insecureMethods and len(args) > 0: 
                action_upon_detection(project_name, src_file, lineno, 'use of YAML load', 'use of YAML load', token)

        elif tokenType == "function_call":
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("args"): args = token["args"]
            
            if name in insecureMethods and len(args) > 0: 
                action_upon_detection(project_name, src_file, lineno, 'use of YAML load', 'use of YAML load', token)
            
            for arg in args:
                if arg in insecureMethods:
                    action_upon_detection(project_name, src_file, lineno, 'use of YAML load', 'use of YAML load', token)

        elif tokenType == "function_def":
            if token.__contains__("return"): funcReturn  = token["return"]
            if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
            if funcReturn in insecureMethods and len(returnArgs) > 0: 
                action_upon_detection(project_name, src_file, lineno, 'use of YAML load', 'use of YAML load', token)

    except Exception as error: save_token_detection_exception('yaml load detection  '+str(error)+'  '+ str(token), src_file)    
