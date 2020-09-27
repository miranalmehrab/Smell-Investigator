from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        
        httpLibs = ['requests.get','requests.Session.get']
        
        if tokenType == "function_call" and name in httpLibs and token.__contains__("keywords"):
            keywords = token["keywords"]
            
            for keyword in keywords:
                if keyword[0] == 'verify' and keyword[1] is False: 
                    action_upon_detection(project_name, srcFile, lineno, 'no_certification_validation', 'TLS is not verified', token)

        # if tokenType == "function_call" and name in httpLibs:
        #     action_upon_detection(project_name, srcFile, lineno, 'no_certification_validation', 'TLS is not verified', token)
        
        # elif tokenType == "variable" and token['valueSrc'] in httpLibs:
        #     action_upon_detection(project_name, srcFile, lineno, 'no_certification_validation', 'TLS is not verified', token)


    except Exception as error: save_token_detection_exception('no certificate detection  '+str(error)+'  '+ str(token), srcFile)