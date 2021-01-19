import re

from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("values"): values = token["values"]
        
        unwantedDirNames = ['folder', 'directory', 'dir', 'path', 'root', 'tmp', 'temp', 'temporary', 'site', 'log_', 'save', 'upload']                   
        
        if tokenType == "variable" and name is not None and token['value'] is not None:
            for dir_name in unwantedDirNames:
                if(
                    (re.match(r'[_A-Za-z0-9-]*{dir}\b'.format(dir = dir_name), name.lower().strip()) or re.match(r'\b{dir}[_A-Za-z0-9-]*'.format(dir = dir_name), name.lower().strip())) 
                    and is_valid_path(token['value'])
                ): 
                    action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)
                    break

        elif (tokenType == "list" or tokenType == "set") and token['name'] is not None and token.__contains__('values'):
            smell_found = False

            for dir_name in unwantedDirNames:
                if(re.match(r'[_A-Za-z0-9-]*{dir}\b'.format(dir = dir_name), name.lower().strip()) or re.match(r'\b{dir}[_A-Za-z0-9-]*'.format(dir = dir_name), name.lower().strip())): 
                    for value in token['values']: 
                        if is_valid_path(value):
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)
                            smell_found = True
                            break

                if smell_found is True: break


        elif tokenType == "dict" and name is not None and token.__contains__('pairs'):
            smell_found = False

            for pair in token['pairs']:
                for dir_name in unwantedDirNames:
                    if(
                        (re.match(r'[_A-Za-z0-9-]*{dir}\b'.format(dir = dir_name), pair[0].lower().strip()) or re.match(r'\b{dir}[_A-Za-z0-9-]*'.format(dir = dir_name), pair[0].lower().strip()))
                        and is_valid_path(pair[1])
                    ):
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)
                            smell_found = True
                            break
                
                if smell_found is True: break    

        if tokenType == "function_call" and token.__contains__('keywords'):
            for keyword in token['keywords']:
                for dir_name in unwantedDirNames:
                    if (
                        len(keyword) == 2 
                        and (re.match(r'[_A-Za-z0-9-]*{dir}\b'.format(dir = dir_name), keyword[0].lower().strip()) or re.match(r'\b{dir}[_A-Za-z0-9-]*'.format(dir = dir_name), keyword[0].lower().strip())) 
                        and is_valid_path(keyword[1])
                    ): 
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)
                        break

    except Exception as error: save_token_detection_exception('hard-coded tmp directory detection  '+str(error)+'  '+ str(token), src_file)

def is_valid_path(value):

    if value is None: return False
    if isinstance(value, str) is False: return False
    if len(value) == 0: return False
    if value == '/': return False
    if value == '//': return False
    if value == '\\': return False

    unix_path_reg = r'^(~?((\.{1,2}|\/?)*[a-zA-Z0-9]*\/)+)[a-zA-Z0-9]*\/?'
    windows_path_reg = r'^([A-Za-z]?\:?)?\\{1,2}([A-Za-z0-9]*\\)*[A-Za-z0-9]*\\?'

    if re.fullmatch(unix_path_reg, value): return True
    elif re.fullmatch(windows_path_reg, value): return True
    else: return False