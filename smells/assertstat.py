from operations.savewarnings import saveWarnings

def detect(token) :

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("left"): left = token["left"]
    if token.__contains__("comparators"): comparators = token["comparators"]

    if (tokenType == "assert" and left!= None and comparators!=None):
        warning = 'assert statement'
        saveWarnings(warning,str(lineno))
        print(warning+ ' at line '+ str(lineno))
