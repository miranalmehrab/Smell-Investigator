from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class NoCertificate:
    '''This is the class for detecting no certificate validations in code'''

    def __init__(self):
        self.insecure_methods = [ 'yaml.load', 'yaml.load_all', 'yaml.full_load', 'yaml.dump', 'yaml.dump_all', 'yaml.full_load_all']
        self.detetcion_message = 'use of insecure YAML operations'
    
    def detect(token, project_name, src_file):
        try:

            if token.__contains__("line"): lineno = token["line"]
            if token.__contains__("type"): tokenType = token["type"]
            if token.__contains__("name"): name = token["name"]
            
            contextVars = ['requests.Session.verify']
            httpLibs = ['requests.get','requests.Session.get', 'requests.post', 'requests.Session.get', 'requests.head']
            
            if tokenType == "variable" and name in contextVars and token['value'] is False: 
                    action_upon_detection(project_name, src_file, lineno, 'no certificate validation', 'no certificate validation', token)

            elif tokenType == "variable" and token.__contains__("valueSrc") and token.__contains__("funcKeywords"):
                
                keywords = token['funcKeywords']
                valueSrc = token['valueSrc']

                if (valueSrc in httpLibs or is_http_call_relaxed(valueSrc)) and len(keywords) > 0:
                    
                    for keyword in keywords:
                        if keyword[0] == 'verify' and (keyword[1] is False or keyword[1] == 'False'): 
                            action_upon_detection(project_name, src_file, lineno, 'no certificate validation', 'no certificate validation', token)

            elif tokenType == "function_call" and (name in httpLibs or is_http_call_relaxed(name)) and token.__contains__("keywords"):
                keywords = token["keywords"]
                
                for keyword in keywords:
                    if keyword[0] == 'verify' and (keyword[1] is False or keyword[1] == 'False'): 
                        action_upon_detection(project_name, src_file, lineno, 'no certificate validation', 'no certificate validation', token)
            
            
            elif tokenType == "function_def" and token.__contains__("return") and token.__contains__("returnKeywords") and token["return"] is not None:
                
                keywords = token['returnKeywords']
                
                for func_return in token['return']:
                    if func_return in httpLibs or is_http_call_relaxed(func_return):
                        for keyword in keywords:
                            if keyword[0] == 'verify' and (keyword[1] is False or keyword[1] == 'False'): 
                                action_upon_detection(project_name, src_file, lineno, 'no certificate validation', 'no certificate validation', token)
                
            
        except Exception as error: save_token_detection_exception('no certificate detection  '+str(error)+'  '+ str(token), src_file)


    def is_http_call_relaxed(method_name):
        http_libs = ['requests.get','requests.Session.get', 'requests.post', 'requests.Session.get']
        http_libs_verb = ['.get', '.post']

        if isinstance(method_name, str) is False: return False

        for lib in http_libs:
            if lib in method_name: 
                return True
        
        for lib_verb in http_libs_verb:
            if lib_verb in method_name and 'request' in method_name:
                return True
        
        return False