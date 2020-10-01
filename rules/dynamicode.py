from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        
        insecureMethods = ['exec', 'eval']

        if tokenType == "variable":
            if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
            if token.__contains__("args"): args = token["args"]
            if valueSrc in insecureMethods and token['isInput'] == True: 
                action_upon_detection(project_name, srcFile, lineno, 'dynamic code execution', 'dynamic code execution', token)

        elif tokenType == "function_call":
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("args"): args = token["args"]
            if name in insecureMethods and token['hasInputs'] == True:
                action_upon_detection(project_name, srcFile, lineno, 'dynamic code execution', 'dynamic code execution', token)
        
        elif tokenType == "function_def":
            if token.__contains__("return"): funcReturn  = token["return"]
            if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
            if funcReturn in insecureMethods and token['returnHasInputs'] == True:
                action_upon_detection(project_name, srcFile, lineno, 'dynamic code execution', 'dynamic code execution', token)

    except Exception as error: save_token_detection_exception('code detection  '+str(error)+'  '+ str(token), srcFile)