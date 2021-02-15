from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class DynamicCode:
    '''This is the class for detecting insecure dynamic code executions in code'''

    def __init__(self):
        self.insecure_methods = ['exec', 'eval', 'compile']
        self.warning_message = 'dynamic code execution'


    def detect_smell(self, token, project_name, src_file):
        try:
            if token.__contains__("line"): lineno = token["line"]
            if token.__contains__("type"): token_type = token["type"]
            
            if token_type == "variable" and token.__contains__('valueSrc'):
                if token["valueSrc"] in self.insecure_methods: 
                    self.trigger_alarm(project_name, src_file, lineno, token)

            elif token_type == "function_call" and token.__contains__("name") and token["name"] in self.insecure_methods:
                    self.trigger_alarm(project_name, src_file, lineno, token)
            
            elif token_type == "function_def" and token.__contains__("return") and token["return"] is not None:
                for func_return in token["return"]:
                    if func_return in self.insecure_methods:
                        self.trigger_alarm(project_name, src_file, lineno, token)
                        
        except Exception as error: save_token_detection_exception('code detection  '+str(error)+'  '+ str(token), src_file)


    def trigger_alarm(self, project_name, src_file, lineno, token):
        action_upon_detection(project_name, src_file, lineno, self.warning_message, self.warning_message, token)
