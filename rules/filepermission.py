from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]

        unwanted_methods = ['os.chmod', 'chmod']
        unwanted_params = ['0x777', '0x757', '0x755','stat.S_IRWXO','stat.S_IROTH','stat.S_IWOTH','stat.S_IXOTH']

        if tokenType == "function_call" and name in unwanted_methods: 
            action_upon_detection(project_name, src_file, lineno, 'bad file permission', 'bad file permission', token)
        
        elif tokenType == 'function_call' and name == 'subprocess.call' and len(args) > 0:
            for arg in args:
                if arg in unwanted_methods: 
                    action_upon_detection(project_name, src_file, lineno, 'bad file permission', 'bad file permission', token)
    
    except Exception as error: save_token_detection_exception('file permission detection  '+str(error)+'  '+ str(token), src_file)