from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"] 
        if token.__contains__("exceptionHandler"): exceptionHandler = token["exceptionHandler"]
        
        unwantedHandlers = ['continue','pass']
        
        if tokenType == "exception_handle" and exceptionHandler in unwantedHandlers: 
            action_upon_detection(project_name, src_file, lineno, 'ignoring except block', 'ignoring except block', token)
    
    except Exception as error: save_token_detection_exception('ignore except detection  '+str(error)+'  '+ str(token), src_file)