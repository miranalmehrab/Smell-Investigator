import re
import time

from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("value"): value = token["value"]
        if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]

        commonPasswords = ['password','passwords','pass','pwd','userpassword','userpwd', 'userpass', 'pass_no', 
                            'pass-no','user-pass', 'upass', 'user_pass', 'u_pass', 'user_pwd', 'uid', 'usr_pwd',
                            'usr_pass', 'usr-pass','userpasswords', 'user-passwords', 'user-password', 'user_password', 
                            'use_pass'
                        ]
        
        if tokenType == "variable" and name is not None and name.lower() in commonPasswords and (value is None or len(value) == 0) and valueSrc == "initialization":  
            if token.__contains__('values'): pass
            else: 
                for pwd in commonPasswords:
                    if re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), name.lower().strip()):
                        action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                        break

                
        elif (tokenType == "list" or tokenType == "set") and name is not None and token.__contains__("values"):
            for pwd in commonPasswords:
                if re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), name.lower().strip()) and len(token['values']) == 0:
                    action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                    break

        elif tokenType == "dict" and name is not None and token.__contains__("keys"):
            for pwd in commonPasswords:
                if re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), name.lower().strip()) and len(token['keys']) == 0:
                    action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                    break

            for value_pair in zip(token['keys'], token['values']):
                if len(value_pair) == 2 and value_pair[0] is not None and isinstance(value_pair[0], str) and value_pair[0].lower() in commonPasswords and (value_pair[1] is None or len(value_pair[1]) == 0):
                    action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
        

        elif tokenType == "comparison" and token.__contains__("pairs"):
            for pair in token["pairs"]:
                for pwd in commonPasswords:
                    if re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), pair[0].lower().strip()) and (pair[1] == None or len(pair[1]) == 0):
                        action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                        break

        elif tokenType == "function_call" and token.__contains__('keywords'):
            for keyword in token['keywords']:
                for pwd in commonPasswords:
            
                    if len(keyword) == 2 and re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), keyword[0].lower().strip()) and (keyword[1] is None or len(str(keyword[1])) == 0): 
                        action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                        break

        elif tokenType == "function_def" and token.__contains__("args") and token.__contains__("defaults"):
            if len(token["args"]) == len(token["defaults"]):
                
                for pair in zip(token['args'], token['defaults']):
                        for pwd in commonPasswords:
                            if re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), pair[0].lower().strip()) and (pair[1] == None or len(str(pair[1])) == 0): 
                                action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                                break

    except Exception as error: save_token_detection_exception('empty password detection  '+str(error)+'  '+ str(token), src_file)