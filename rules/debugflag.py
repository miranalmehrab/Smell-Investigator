from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("value"): value = token["value"]
        
        restrictedNames = ['debug','debug_propagate_exceptions']
        
        if tokenType == "variable" and name is not None and name.lower() in restrictedNames and value is True: 
            action_upon_detection(project_name, srcFile, lineno, 'deployment with debug flag set to true', 'deployment with debug flag set to true', token)


        elif tokenType == "function_call" and token.__contains__("keywords"):
            keywords = token["keywords"]
            
            for keyword in keywords:
                if(keyword[0] in restrictedNames and keyword[1] is True): 
                    action_upon_detection(project_name, srcFile, lineno, 'deployment with debug flag set to true', 'deployment with debug flag set to true', token)


        elif tokenType == "dict" and token.__contains__("keys") and token.__contains__("values"): 
            pairs = [list(item) for item in zip(token["keys"], token["values"])]
            
            for pair in pairs: 
                if pair[0].lower() in restrictedNames and pair[1] is True: 
                    action_upon_detection(project_name, srcFile, lineno, 'deployment with debug flag set to true', 'deployment with debug flag set to true', token)
    
    except Exception as error: save_token_detection_exception('debug detection  '+str(error)+'  '+ str(token), srcFile)
    