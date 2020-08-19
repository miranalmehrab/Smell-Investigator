from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):

    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("values"): values = token["values"]
    
    unwantedDirNames = ['hardcoded_tmp_directory', 'hardcoded_temp_directory', 'tmp_dir'
                        'hardcoded_directory', 'save_dir', 'temp_dir', 'hardcoded_dir',
                        'temporary_directory', 'temporary_dir', 'temp_directory', 'dir'
                        ]
                        
    unwantedValues = ['/tmp', '/var/tmp', '/dev/shm']
    
    if tokenType == "variable" and name.lower() in unwantedDirNames and token['value'] is not None: 
        actionUponDetection(srcFile, lineno, 'harcoded_tmp_dir', 'hardcoded temporary directory')

    elif tokenType == "list" and name.lower() in unwantedDirNames and len(values) > 0: 
        actionUponDetection(srcFile, lineno, 'harcoded_tmp_dir', 'hardcoded temporary directory')
    