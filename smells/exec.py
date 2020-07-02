def detect(token) :

    if token.__contains__("line"): lineno = token["line"] 
    if token.__contains__("name"): methodname = token["name"]
    if token.__contains__("args"): args = token["args"]
    if token.__contains__("hasInputs"): containsUserInput =  token["hasInputs"]

    if (methodname == "exec" and args and containsUserInput):
        warning = 'possible exec statement at line ' + str(lineno)
        print(warning)
