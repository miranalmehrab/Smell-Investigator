import re

from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, imports,project_name, srcFile):
    try:
        # print(len(imports))
        
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
            
        libs = ['urllib.request.urlretrieve','urllib.urlretrieve','urllib2.urlopen','requests.get','wget.download']

        if tokenType == "variable" and token.__contains__('valueSrc') and token.__contains__('args'):    
            if token['valueSrc'] in libs and len(token['args']) > 0:
                if valid_download_url(args[0]) and 'hashlib' not in imports:
                    action_upon_detection(project_name, srcFile, lineno, 'no integrity check', 'no integrity check', token)
                

        elif tokenType == "function_call" and name in libs and len(args) > 0:
            if valid_download_url(args[0]) and 'hashlib' not in imports:
                action_upon_detection(project_name, srcFile, lineno, 'no integrity check', 'no integrity check', token)
        

        elif tokenType == "function_def" and token.__contains__('return') and token.__contains__('returnArgs'):
            returnArgs = token['returnArgs']
            
            if len(returnArgs) > 0:
                if token['return'] in libs and valid_download_url(returnArgs[0]) and 'hashlib' not in imports:
                    action_upon_detection(project_name, srcFile, lineno, 'no integrity check', 'no integrity check', token)
        

    except Exception as error: save_token_detection_exception('no integrity detection  '+str(error)+'  '+ str(token), srcFile)


def valid_download_url(string):
    extensions = ['iso', 'tar', 'bzip2', 'zip', 'rar', 'gzip', 'gzip2', 'gz','snap', 'flatpak',
                'deb', 'rpm', 'sh', 'run', 'bin', 'exe', 'rar', '7zip', 'msi', 'bat', 'dmg', 'pacman']

    extension = string.split(".")[-1] if string is not None else None
  
    if extension in extensions: return True
    elif string.find('FILE=') != -1: return True
    elif string.find('file=') != -1: return True
    elif string.find('File=') != -1: return True
    
    return False
