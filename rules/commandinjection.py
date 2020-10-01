from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:
        if token.__contains__("line"): lineno = token["line"] 
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
        if token.__contains__("hasInputs"): containsUserInput =  token["hasInputs"]

        insecureMethods = ['sys.argv', 'ArgumentParser', 'argparse', 'subprocess.Popen', 'os.system']
        
        if tokenType == "variable" and token.__contains__("valueSrc"):
            if token["valueSrc"] in insecureMethods:
                action_upon_detection(project_name, srcFile, lineno, 'command injection', 'command injection', token)
        
        elif tokenType == "function_call" and name in insecureMethods and len(args) > 0: 
            action_upon_detection(project_name, srcFile, lineno, 'command injection', 'command injection', token)
    
        elif tokenType == "function_def" and token.__contains__('return') and token.__contains__('returnArgs'): 
            if token['return'] in insecureMethods and len(token['returnArgs']) > 0:
                action_upon_detection(project_name, srcFile, lineno, 'command injection', 'command injection', token)
        
    except Exception as error: save_token_detection_exception('command injection detection  '+str(error)+'  '+ str(token), srcFile)
    