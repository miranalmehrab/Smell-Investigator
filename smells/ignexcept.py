from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"] 
    if token.__contains__("firstBlock"): firstBlock = token["firstBlock"]
    
    unwantedArgs = ['continue','pass']
        
    if tokenType == "except_statement" and firstBlock in unwantedArgs:
            actionUponDetection(srcFile, lineno, 'ignore_except_block', 'ignore except block')
            