import re
from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("value"): value = token["value"]
        if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
        

        commonKeywords = [ 'user_name', 'usr', 'uid', 'userid', 'usrid', 'uname', 'usrname', 'admin_name', 'guest', 'admin', 'root_name', 'root_id', 'owner_name','owner_id','super_user', 'sup_usr',
                            'userpassword', 'usr_pass', 'usr_pwd', 'user_pass', 'password', 'usr_password', 'admin_pwd', 'pwd', 'admin_pass', 'guest_pass', 'default_pwd', 'default_pass',
                            'guest_pwd', 'admin_password', 'guest_password', 'root_password', 'root_pwd', 'root_pass', 'owner_pass', 'owner_pwd', 'owner_password', 'default_password',
                            'user_key', 'usr_key', 'secret_key', 'recaptcha_key', 'site_key', 'ssh_key', 'ssl_key', 'private_key', 'public_key', 'cryptographic_key', 'tls_key', 'tls', 'ssl',
                            'ssh_key', 'ssh_password', 'ssh_pwd', 'ssh_pass', 'site_ssh', 'crypt', 'certificate', 'user_token', 'usr_token', 'u_token', 'utoken' 
        ]
            
        if tokenType == "variable" and name is not None and value is not None and valueSrc == "initialization":
            for key in commonKeywords:
                if re.match(r'[_A-Za-z0-9-\.]*{key}\b'.format(key = key), name.lower().strip()) or re.match(r'\b{key}[_A-Za-z0-9-\.]*'.format(key = key), name.lower().strip()):
                    if is_valid_hardcoded_value(value):
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        break

        if tokenType == "variable" and name is not None and token.__contains__('funcKeywords'):
            for keyword in token['funcKeywords']:
                for key in commonKeywords:
                    if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), keyword[0].lower().strip()) and is_valid_hardcoded_value(keyword[1]):
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        break
            
        elif (tokenType == "list" or tokenType == "set") and name is not None and token.__contains__("values"):
            for key in commonKeywords:
                
                if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), name.lower().strip()):
                    for value in token['values']:

                        if is_valid_hardcoded_value(value): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break
            
        elif tokenType == "dict" and token.__contains__("pairs"): 
            for value_pair in token['pairs']:
                if len(value_pair) == 2 and value_pair[0] is not None and isinstance(value_pair[0], str) and value_pair[1] is not None:
                    for key in commonKeywords:    
                        if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), value_pair[0].lower().strip()) and is_valid_hardcoded_value(value_pair[1]): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break


        
        elif tokenType == "comparison" and token.__contains__("pairs"):
            for pair in token["pairs"]:
                
                if len(pair) == 2 and pair[0] is not None and isinstance(pair[0], str) and pair[0] != 'key' and pair[0] != 'token' and pair[1] is not None:  
                    for key in commonKeywords:

                        if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), pair[0].lower().strip()) and is_valid_hardcoded_value(pair[1]): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break
                     
        
        elif tokenType == "function_call" and token.__contains__('keywords'):
            for keyword in token['keywords']:
                
                if len(keyword) == 3 and isinstance(keyword[0], str) and keyword[0].lower() is not None and keyword[1] is not None and keyword[2] is True:    
                    for key in commonKeywords:

                        if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), keyword[0].lower().strip()) and is_valid_hardcoded_value(keyword[1]): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break
                    

        elif tokenType == "function_def" and token.__contains__("args") and token.__contains__("defaults"):    
            defaults_size = len(token['defaults'])
            args = token['args'][-defaults_size:]

            for pair in zip(args, token['defaults']):    
                for key in commonKeywords:
                    
                    if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), pair[0].lower().strip()) and pair[1][1] is True and is_valid_hardcoded_value(pair[1][0]): 
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        break
                
             
    except Exception as error: save_token_detection_exception('hard-coded secret detection  '+str(error)+'  '+ str(token), src_file)


def contains_suspicious_strings(value):
    prohibitedStrings = ['admin', 'root', 'user', 'username', 'pwd', 'pass', 'guest', 'root_password', 'usr',
                        'userpass', 'usrpwd', 'userpassword', 'usrtoken', 'token','default', 'nopassword',
                        'defaultpass', 'password', 'guest', 'root1', 'user root'
                        ]
    
    for prohibitedString in prohibitedStrings:
        if prohibitedString in value: return True
    return False

def is_valid_hardcoded_value(value):
    new_reg = r'([A-Za-z]*([0-9]+|[!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"-\+\/]+))+([A-Za-z]*([0-9]*|[!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"-\+\/]*))*'

    if isinstance(value, str):
        if len(value) == 0: return False
        elif re.fullmatch(new_reg, value): return True
        elif re.search(r'\\+', value): return False
        elif re.search(r'([!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\'\"-\+\/]+)', value) and len(value) > 1: return True
        # elif re.fullmatch(r'([A-Za-z]*[0-9!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"-\+\/]+)+[A-Za-z]*[0-9!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"\+-\/]*', value): return True
        elif contains_suspicious_strings(value): return True
        else: return False
    
    else: return False
        