from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"] 
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("args"): args = token["args"]
    if token.__contains__("hasInputs"): containsUserInput =  token["hasInputs"]

    cmdFuncs = ['sys.argv', 'ArgumentParser', 'argparse', 'subprocess.Popen', 'os.system']
    
    if tokenType == "variable" and token.__contains__("valueSrc"):
        if token["valueSrc"] in cmdFuncs: actionUponDetection(srcFile, lineno, 'shell_injection', 'command injection')
    
    elif tokenType == "function_call" and name in cmdFuncs and containsUserInput: actionUponDetection(srcFile, lineno, 'shell_injection', 'command injection')
       