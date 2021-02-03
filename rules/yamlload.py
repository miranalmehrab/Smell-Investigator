from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class YamlOperations:
    '''This is the class for detecting insecure yaml operations in code'''

    def __init__(self):
        self.insecure_methods = [ 'yaml.load', 'yaml.load_all', 'yaml.full_load', 'yaml.dump', 'yaml.dump_all', 'yaml.full_load_all']
        self.detetcion_message = 'use of insecure YAML operations'


    def detect_smell(self, token, project_name, src_file):
        try:
            if token.__contains__("line"): lineno = token["line"]
            if token.__contains__("type"): token_type = token["type"]
            
            if token_type == "variable" and token.__contains__("valueSrc"):
                if token["valueSrc"] in self.insecure_methods: 
                    self.trigger_alarm(project_name, src_file, lineno, token)

            elif token_type == "function_call" and token.__contains__("name"):
                
                if token["name"] in self.insecure_methods:
                    self.trigger_alarm(project_name, src_file, lineno, token)
                
                if token.__contains__("args"):
                    for arg in token["args"]:
                        if arg in self.insecure_methods:
                            self.trigger_alarm(project_name, src_file, lineno, token)

            elif token_type == "function_def" and token.__contains__("return") and token['return'] is not None:
                for func_return in token["return"]:
                    if func_return in self.insecure_methods: 
                        self.trigger_alarm(project_name, src_file, lineno, token)

        except Exception as error: 
            save_token_detection_exception('yaml load detection  '+str(error)+'  '+ str(token), src_file)    


    def trigger_alarm(self, project_name, src_file, lineno, token):
        action_upon_detection(project_name, src_file, lineno, self.detetcion_message, self.detetcion_message, token)

