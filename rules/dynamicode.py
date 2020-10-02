from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        
        insecureMethods = ['exec', 'eval', 'compile']

        if tokenType == "variable":
            if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
            if token.__contains__("args"): args = token["args"]
            if valueSrc in insecureMethods and token['isInput'] is True: 
                action_upon_detection(project_name, src_file, lineno, 'dynamic code execution', 'dynamic code execution', token)

        elif tokenType == "function_call":
            isInput = False
            hasInputs = False

            if token.__contains__("name"): name = token["name"]
            if token.__contains__("args"): args = token["args"]
            if token.__contains__("hasInputs"): hasInputs = token["hasInputs"]
            if token.__contains__("isInput"): isInput = token['isInput']
            
            if name in insecureMethods and (hasInputs is True or isInput is True):
                action_upon_detection(project_name, src_file, lineno, 'dynamic code execution', 'dynamic code execution', token)
        
        elif tokenType == "function_def":
            returnHasInputs = False

            if token.__contains__("return"): funcReturn  = token["return"]
            if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
            if token.__contains__("returnHasInputs"): returnHasInputs = token['returnHasInputs']
            if funcReturn in insecureMethods and returnHasInputs is True:
                action_upon_detection(project_name, src_file, lineno, 'dynamic code execution', 'dynamic code execution', token)

    except Exception as error: save_token_detection_exception('code detection  '+str(error)+'  '+ str(token), src_file)