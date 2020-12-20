from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        
        contextVars = ['requests.Session.verify']
        httpLibs = ['requests.get','requests.Session.get', 'requests.post', 'requests.Session.get']
        
        if tokenType == "variable" and name in contextVars and token['value'] is False: 
                action_upon_detection(project_name, src_file, lineno, 'no certificate validation', 'no certificate validation', token)

        elif tokenType == "variable" and token.__contains__("valueSrc") and token.__contains__("funcKeywords"):
            
            keywords = token['funcKeywords']
            valueSrc = token['valueSrc']

            if valueSrc in httpLibs and len(keywords) > 0:
                
                for keyword in keywords:
                    if keyword[0] == 'verify' and (keyword[1] is False or keyword[1] == 'False'): 
                        action_upon_detection(project_name, src_file, lineno, 'no certificate validation', 'no certificate validation', token)

        elif tokenType == "function_call" and name in httpLibs and token.__contains__("keywords"):
            keywords = token["keywords"]
            
            for keyword in keywords:
                if keyword[0] == 'verify' and (keyword[1] is False or keyword[1] == 'False'): 
                    action_upon_detection(project_name, src_file, lineno, 'no certificate validation', 'no certificate validation', token)
        
        
        elif tokenType == "function_def" and token.__contains__("return") and token.__contains__("returnKeywords") and token["return"] is not None:
            
            keywords = token['returnKeywords']
            
            for func_return in token['return']:
                if func_return in httpLibs:
                    for keyword in keywords:
                        if keyword[0] == 'verify' and (keyword[1] is False or keyword[1] == 'False'): 
                            action_upon_detection(project_name, src_file, lineno, 'no certificate validation', 'no certificate validation', token)
            
        
    except Exception as error: save_token_detection_exception('no certificate detection  '+str(error)+'  '+ str(token), src_file)