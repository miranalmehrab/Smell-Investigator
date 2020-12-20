from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        
        insecure_methods = ['yaml.load', 'yaml.load_all', 'yaml.full_load', 'yaml.dump', 'yaml.dump_all', 'yaml.full_load_all']

        if tokenType == "variable" and token.__contains__("valueSrc"):
            if token["valueSrc"] in insecure_methods: 
                action_upon_detection(project_name, src_file, lineno, 'use of YAML load', 'use of YAML load', token)

        elif tokenType == "function_call" and token.__contains__("name"):
            
            if token["name"] in insecure_methods:
                action_upon_detection(project_name, src_file, lineno, 'use of YAML load', 'use of YAML load', token)
            
            if token.__contains__("args"):
                for arg in token["args"]:
                    if arg in insecure_methods:
                        action_upon_detection(project_name, src_file, lineno, 'use of YAML load', 'use of YAML load', token)


        elif tokenType == "function_def" and token.__contains__("return") and token['return'] is not None:
            for func_return in token["return"]:
                if func_return in insecure_methods: 
                    action_upon_detection(project_name, src_file, lineno, 'use of YAML load', 'use of YAML load', token)

    except Exception as error: save_token_detection_exception('yaml load detection  '+str(error)+'  '+ str(token), src_file)    
