from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception
 
def detect(token, project_name, src_file) :
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        
        if tokenType == "assert" and token.__contains__("left"):
            if token["left"] is not None:
                action_upon_detection(project_name, src_file, lineno, 'assert statement', 'assert statement', token)

        elif tokenType == "assert" and token.__contains__('func'):
            if token['func'] is not None: 
                action_upon_detection(project_name, src_file, lineno, 'assert statement', 'assert statement', token)
    
    except Exception as error: save_token_detection_exception('assert detection  '+str(error)+'  '+ str(token), src_file)
    