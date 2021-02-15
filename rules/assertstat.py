from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class AssertStatement:
    '''This is the class for detecting assert statement in code'''

    def __init__(self):
        self.insecure_token_types = ['assert']
        self.warning_message = 'use of assert statement'


    def detect_smell(self, token, project_name, src_file) :
        lineno = token['line']

        try:
            if token['type'] in self.insecure_token_types: 
                self.trigger_alarm(project_name, src_file, lineno, token) 
        
        except Exception as error: save_token_detection_exception('assert detection  '+str(error)+'  '+ str(token), src_file)


    def trigger_alarm(self, project_name, src_file, lineno, token):
        action_upon_detection(project_name, src_file, lineno, self.warning_message, self.warning_message, token)
