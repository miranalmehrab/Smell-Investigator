from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        
        insecureMethods = ['exec', 'eval', 'compile']

        if tokenType == "variable" and token.__contains__('valueSrc'):
            
            if token["valueSrc"] in insecureMethods: 
                action_upon_detection(project_name, src_file, lineno, 'dynamic code execution', 'dynamic code execution', token)

        elif tokenType == "function_call":
            
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("args"): args = token["args"]
            
            if name in insecureMethods and len(args) > 0:
                action_upon_detection(project_name, src_file, lineno, 'dynamic code execution', 'dynamic code execution', token)
        
        elif tokenType == "function_def":
            returnHasInputs = False

            if token.__contains__("return"): funcReturn  = token["return"]
            if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
            
            if funcReturn in insecureMethods and len(returnArgs) > 0:
                action_upon_detection(project_name, src_file, lineno, 'dynamic code execution', 'dynamic code execution', token)

    except Exception as error: save_token_detection_exception('code detection  '+str(error)+'  '+ str(token), src_file)