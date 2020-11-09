import re

from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("values"): values = token["values"]
        
        unwantedDirNames = ['folder', 'directory', 'dir', 'path', 'root', 'tmp', 'temp', 'temporary', 'site', 'log', 'save']                   
        
        if tokenType == "function_call" and name is not None and token.__contains__('keywords'):
            for keyword in token['keywords']:
                for dir_name in unwantedDirNames:
                    if len(keyword) == 2 and isinstance(keyword[0], str) and re.match(r'[_A-Za-z0-9-]*{dir}\b'.format(dir = keyword[0]), name.lower().strip()) and keyword[1] is not None and isinstance(keyword[1], str) and len(keyword[1]) > 0 and is_valid_path(keyword[1]): 
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)
                        break

        elif tokenType == "variable" and name is not None:
            for dir_name in unwantedDirNames:
                if re.match(r'[_A-Za-z0-9-]*{dir}\b'.format(dir = dir_name), name.lower().strip()) and token['value'] is not None and is_valid_path(token['value']): 
                    action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)
                    break

        elif (tokenType == "list" or tokenType == "set"):
            for dir_name in unwantedDirNames:
                if re.match(r'[_A-Za-z0-9-]*{dir}\b'.format(dir = dir_name), name.lower().strip()): 
                    for value in values: 
                        if is_valid_path(value):
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)

        elif tokenType == "dict" and name is not None and token.__contains__('pairs'):
            for pair in token['pairs']:
                for dir_name in unwantedDirNames:
                    if re.match(r'[_A-Za-z0-9-]*{dir}\b'.format(dir = dir_name), pair[0].lower().strip()):
                        if is_valid_path(pair[1]):
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded tmp directories', 'hard-coded tmp directories', token)
                

    except Exception as error: save_token_detection_exception('hard-coded tmp directory detection  '+str(error)+'  '+ str(token), src_file)

def is_valid_path(value):

    if value is None: return False
    if isinstance(value, str) is False: return False
    
    unix_path_reg = r'^(~?((\.{1,2}|\/?)*[a-zA-Z0-9]*\/)+)[a-zA-Z0-9]*\/?'
    windows_path_reg = r'^([A-Za-z]?\:?)?\\{1,2}([A-Za-z0-9]*\\)*[A-Za-z0-9]*\\?'

    if re.fullmatch(unix_path_reg, value): return True
    elif re.fullmatch(windows_path_reg, value): return True
    else: return False