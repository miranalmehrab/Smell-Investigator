def detect(token):
    
    if token.__contains__("line"): lineno = token["line"] 
    if token.__contains__("name"): methodname = token["name"]
    if token.__contains__("args"): args = token["args"]
    if token.__contains__("hasInputs"): containsUserInput =  token["hasInputs"]

    unwanted = ['subprocess.Popen']
    
    if methodname in unwanted and (args or containsUserInput):
        warning = 'possible cmd injection at line ' + str(lineno)
        print(warning)