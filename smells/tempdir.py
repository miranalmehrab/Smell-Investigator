from operations.action_upon_detection import action_upon_detection

def detect(token, project_name, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("values"): values = token["values"]
    
    unwantedDirNames = ['hardcoded_tmp_directory', 'hardcoded_temp_directory', 'tmp_dir'
                        'hardcoded_directory', 'save_dir', 'temp_dir', 'hardcoded_dir',
                        'temporary_directory', 'temporary_dir', 'temp_directory', 'dir'
                        ]
                        
    unwantedValues = ['/tmp', '/var/tmp', '/dev/shm']
    
    if tokenType == "variable" and  name.lower() in unwantedDirNames and (token['value'] is not None or token['valueSrc'] is not None): 
        action_upon_detection(project_name, srcFile, lineno, 'harcoded_tmp_dir', 'hardcoded temporary directory', token)

    elif (tokenType == "list" or tokenType == "set") and name.lower() in unwantedDirNames and len(values) > 0: 
        action_upon_detection(project_name, srcFile, lineno, 'harcoded_tmp_dir', 'hardcoded temporary directory', token)
    