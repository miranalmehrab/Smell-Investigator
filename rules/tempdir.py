from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("values"): values = token["values"]
        
        unwantedDirNames = ['hardcoded_tmp_directory', 'hardcoded_temp_directory', 'tmp_dir'
                            'hardcoded_directory', 'save_dir', 'temp_dir', 'hardcoded_dir',
                            'temporary_directory', 'temporary_dir', 'temp_directory', 'dir',
                            'directory', 'tmp_directory', 'tmp_path', 'dir_path', 'path_dir',
                            'path_directory', 'directory_path', 'temp_path', 'temporary_path',
                            'file_path', 'file_dir', 'folder_path', 'folder_dir', 'file_ditectory',
                            'folder_directory'
                        ]
                            
        unwantedValues = ['/tmp', '/var/tmp', '/dev/shm']
        
        if tokenType == "function_call" and token.__contains__('keywords'):
            for keyword in token['keywords']:
                if len(keyword) == 2 and isinstance(keyword[0], str) and keyword[0].lower() in unwantedDirNames and keyword[1] is not None and len(keyword[1]) > 0 and is_valid_path(keyword[1]): 
                    action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)
    
        elif tokenType == "variable" and name is not None and name.lower() in unwantedDirNames and token['value'] is not None and is_valid_path(token['value']): 
            action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)

        elif (tokenType == "list" or tokenType == "set") and name is not None and name.lower() in unwantedDirNames and len(values) > 0: 
            action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)

        elif tokenType == "dict" and name is not None and name.lower() in unwantedDirNames and token.__contains__('keys'):
            for key in token['keys']:
                if key is not None and isinstance(key, str) and key.lower() in unwantedDirNames:
                    action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)

            

    except Exception as error: save_token_detection_exception('hard-coded tmp directory detection  '+str(error)+'  '+ str(token), src_file)

def is_valid_path(value):
    if value is None: return False
    if './' in value: return True
    elif '/' in value: return True
    elif '\\' in value: return True
    elif '%' in value: return True
    else: return False