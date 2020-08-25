from operations.action_upon_detection import action_upon_detection

def detect(token, project_name, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    
    insecureMethods = ['yaml.load', 'yaml.load_all']

    if tokenType == "variable":
        if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
        if token.__contains__("args"): args = token["args"]
        if valueSrc in insecureMethods and len(args) > 0: 
            action_upon_detection(project_name, srcFile, lineno, 'yaml_load_used', 'yaml load used')

    elif tokenType == "function_call":
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
        
        if name in insecureMethods and len(args) > 0: 
            action_upon_detection(project_name, srcFile, lineno, 'yaml_load_used', 'yaml load used')
        
        for arg in args:
            if arg in insecureMethods:
                action_upon_detection(project_name, srcFile, lineno, 'yaml_load_used', 'yaml load used')

    elif tokenType == "function_def":
        if token.__contains__("return"): funcReturn  = token["return"]
        if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
        if funcReturn in insecureMethods and len(returnArgs) > 0: 
            action_upon_detection(project_name, srcFile, lineno, 'yaml_load_used', 'yaml load used')
    
