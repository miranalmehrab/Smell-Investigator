from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("values"): values = token["values"]
        
        unwantedDirNames = ['hardcoded_tmp_directory', 'hardcoded_temp_directory', 'tmp_dir'
                            'hardcoded_directory', 'save_dir', 'temp_dir', 'hardcoded_dir',
                            'temporary_directory', 'temporary_dir', 'temp_directory', 'dir'
                            ]
                            
        unwantedValues = ['/tmp', '/var/tmp', '/dev/shm']
        
        if tokenType == "variable" and name is not None and name.lower() in unwantedDirNames and (token['value'] is not None or token['valueSrc'] == 'initialized'): 
            action_upon_detection(project_name, srcFile, lineno, 'harcoded_tmp_dir', 'hardcoded temporary directory', token)

        elif (tokenType == "list" or tokenType == "set") and name is not None and name.lower() in unwantedDirNames and len(values) > 0: 
            action_upon_detection(project_name, srcFile, lineno, 'harcoded_tmp_dir', 'hardcoded temporary directory', token)
    
    except Exception as error: save_token_detection_exception('hard-coded tmp directory detection  '+str(error)+'  '+ str(token), srcFile)