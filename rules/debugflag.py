from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class DebugFlag:
    '''This is the class for detecting debug flag set to true in code'''

    def __init__(self):
        self.restricted_names = ['debug','debug_propagate_exceptions','propagate_exceptions']
        self.warning_message = 'deployment with debug flag set to true'

    def detect_smell(self, token, project_name, src_file):
        try:
            if token.__contains__("line"): lineno = token["line"]
            if token.__contains__("type"): tokenType = token["type"]
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("value"): value = token["value"]
            
            
            if tokenType == "variable" and name is not None and (name.lower() in self.restricted_names or self.has_debug_in_name(name.lower())) and value is True: 
                self.trigger_alarm(project_name, src_file, lineno, token)


            elif tokenType == "function_call" and token.__contains__("keywords"):
                
                for keyword in token["keywords"]:
                    if(keyword[0] is not None and isinstance(keyword[0], str) and keyword[0].lower() in self.restricted_names and keyword[1] is True): 
                        self.trigger_alarm(project_name, src_file, lineno, token)


            elif tokenType == "dict" and token.__contains__("pairs"): 
                
                for pair in token['pairs']:
                    if pair[0] in self.restricted_names and pair[1] is True: 
                        self.trigger_alarm(project_name, src_file, lineno, token)
        
        except Exception as error: save_token_detection_exception('debug detection  '+str(error)+'  '+ str(token), src_file)


    def has_debug_in_name(self, var_name):
        for name in self.restricted_names:
            if name in var_name.lower().strip(): 
                return True
        
        return False


    def trigger_alarm(self, project_name, src_file, lineno, token):
        action_upon_detection(project_name, src_file, lineno, self.warning_message, self.warning_message, token)
