from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class Assert:
    '''This is the class for detecting assert statement in code'''

    def __init__(self):
        self.insecure_methods = [ 'yaml.load', 'yaml.load_all', 'yaml.full_load', 'yaml.dump', 'yaml.dump_all', 'yaml.full_load_all']
        self.detetcion_message = 'use of insecure YAML operations'

    def detect(token, project_name, src_file) :
        try:
            
            if token['type'] == 'assert': 
                action_upon_detection(project_name, src_file, token['line'], 'use of assert statement', 'assert statement', token) 

            # if tokenType == "assert" and token.__contains__("left"):
            #     if token["left"] is not None:
            #         action_upon_detection(project_name, src_file, lineno, 'assert statement', 'assert statement', token)

            # elif tokenType == "assert" and token.__contains__('func'):
            #     if token['func'] is not None: 
            #         action_upon_detection(project_name, src_file, lineno, 'assert statement', 'assert statement', token)
        
        except Exception as error: save_token_detection_exception('assert detection  '+str(error)+'  '+ str(token), src_file)
    