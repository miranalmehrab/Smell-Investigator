from operations.action_upon_detection import action_upon_detection

def detect(token, project_name, srcFile):
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]

    insecureMethods = ['marshal.load', 'marshal.loads','pickle.load', 'pickle.loads', 'cPickle.load']

    if tokenType == "variable":
        if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
        if token.__contains__("args"): args = token["args"]
        if valueSrc in insecureMethods and args is not None and len(args) > 0:
            action_upon_detection(project_name, srcFile, lineno, 'insecure_data_diserialization', 'insecure data diserialized', token)

    elif tokenType == "function_call":
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
        if name in insecureMethods and args is not None and len(args) > 0: 
            action_upon_detection(project_name, srcFile, lineno, 'insecure_data_diserialization', 'insecure data diserialized', token)
    
    elif tokenType == "function_def":
        if token.__contains__("return"): funcReturn  = token["return"]
        if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
        if funcReturn in insecureMethods and returnArgs is not None and len(returnArgs) > 0: 
            action_upon_detection(project_name, srcFile, lineno, 'insecure_data_diserialization', 'insecure data diserialized', token)