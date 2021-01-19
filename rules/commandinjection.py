import re

from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"] 
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
        if token.__contains__("hasInputs"): containsUserInput =  token["hasInputs"]

        shell_methods = ['sys.argv', 'subprocess.Popen', 'os.system', 'os.popen','subprocess.run', 'argparse.ArgumentParser',
                        'getopt.getopt', 'os.execle', 'os.execl', 'popen2.Popen3', 'popen2.Popen4'
                    ]
        
        if tokenType == "variable" and token.__contains__("valueSrc") and token["valueSrc"] is not None and token["valueSrc"] != 'initialization':
            if token["valueSrc"].strip() in shell_methods or is_extended_shell_command_names(token["valueSrc"].strip()):
                action_upon_detection(project_name, src_file, lineno, 'command injection', 'command injection', token)
        
        elif tokenType == "function_call" and name is not None and (name.strip() in shell_methods or is_extended_shell_command_names(name.strip())): 
            action_upon_detection(project_name, src_file, lineno, 'command injection', 'command injection', token)
    
        elif tokenType == "function_def" and token.__contains__('return') and token["return"] is not None: 
            for func_return in token['return']:
                if isinstance(func_return, str) and (func_return in shell_methods or is_extended_shell_command_names(func_return)):
                    action_upon_detection(project_name, src_file, lineno, 'command injection', 'command injection', token)
        
    except Exception as error: 
        print(str(error))
        save_token_detection_exception('command injection detection  '+str(error)+'  '+ str(token), src_file)
    
    
def is_extended_shell_command_names(method_name):
    
    if isinstance(method_name, str) is False: return False
    elif len(method_name) == 0: return False

    shell_methods = ['sys.argv', 'subprocess.Popen', 'os.system', 'os.popen','subprocess.run', 'argparse.ArgumentParser', 'getopt.getopt']
    
    for name in shell_methods:
        if name in method_name: 
            return True

    return False
