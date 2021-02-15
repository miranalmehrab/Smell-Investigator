from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class IgnoreException:
    '''This is the class for detecting ignoring exception blocks in code'''

    def __init__(self):
        self.unwanted_handlers = ['continue','pass']
        self.warning_message = 'ignoring except block'


    def detect_smell(self, token, project_name, src_file):
        try:
            if token.__contains__("line"): lineno = token["line"]
            if token.__contains__("type"): token_type = token["type"] 
            if token.__contains__("exceptionHandler"): exception_handler = token["exceptionHandler"]
            
            if token_type == "exception_handle" and exception_handler in self.unwanted_handlers: 
                self.trigger_alarm(project_name, src_file, lineno, token)
        
        except Exception as error: save_token_detection_exception('ignore except detection  '+str(error)+'  '+ str(token), src_file)
    

    def trigger_alarm(self, project_name, src_file, lineno, token):
        action_upon_detection(project_name, src_file, lineno, self.warning_message, self.warning_message, token)
