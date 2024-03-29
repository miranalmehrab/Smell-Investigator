from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class FilePermission:
    '''This is the class for detecting bad file permissions in code'''

    def __init__(self):
        self.insecure_methods = ['os.chmod', 'chmod'] 
        self.warning_message = 'bad file permission'
        self.unwanted_params = ['stat.S_IRWXG','stat.S_IRGRP', 'stat.S_IWGRP','stat.S_IXGRP','stat.S_IRWXO','stat.S_IROTH','stat.S_IWOTH','stat.S_IXOTH']


    def detect_smell(self, token, project_name, src_file):
        try:
            if token.__contains__("line"): lineno = token["line"]
            if token.__contains__("type"): tokenType = token["type"]
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("args"): args = token["args"]

            if tokenType == "function_call" and name in self.insecure_methods:
                if self.has_dangerous_parameters_in_function_call(token['args']):
                    self.trigger_alarm(project_name, src_file, lineno, token)
                
            elif tokenType == 'function_call' and name == 'subprocess.call' and len(args) > 0:
                
                if isinstance(token['args'][0], list):
                    for arg in token['args'][0]:
                        if arg in self.insecure_methods:
                            if self.has_dangerous_parameters_in_function_call(token['args'][0]):
                                self.trigger_alarm(project_name, src_file, lineno, token)
                else:
                    for arg in token['args']:
                        if arg in self.insecure_methods:
                            if self.has_dangerous_parameters_in_function_call(token['args']):
                                self.trigger_alarm(project_name, src_file, lineno, token)
                
        except Exception as error: save_token_detection_exception('file permission detection  '+str(error)+'  '+ str(token), src_file)


    def has_dangerous_parameters_in_function_call(self, args):
        for arg in args:
            if isinstance(arg, int):

                octal_value_of_arg = oct(arg)
                group_permission_value = octal_value_of_arg[-2]
                other_permission_value = octal_value_of_arg[-1]

                if int(group_permission_value) > 4 or int(other_permission_value) > 4: return True
                    
            elif isinstance(arg, str):
                if arg in self.unwanted_params: 
                    return True

        return False
    

    def trigger_alarm(self, project_name, src_file, lineno, token):
        action_upon_detection(project_name, src_file, lineno, self.warning_message, self.warning_message, token)
