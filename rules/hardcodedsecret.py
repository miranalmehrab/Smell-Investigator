import re
from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): token_type = token["type"]
        if token.__contains__("value"): value = token["value"]
        if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
        
        if token.__contains__("name"): 
            name = token["name"]
            name = name.lower().strip()

        common_keywords = [ 'user', 'usr', 'guest', 'admin', 'root', 'owner', 'uid', 'uname', 'password','pwd',
                            '_key', 'tls','ssl','ssh', 'crypt', 'certificate', 'token', 'id', 'default', 'u_pass',
                            'userpass', 'pass_no'
                        ]
        
        # 'secret_key', 'recaptcha_key', 'site_key', 'ssh_key', 'ssl_key', 
            
        if token_type == "variable" and name is not None and value is not None and valueSrc == "initialization":
            for key in common_keywords:
                if(
                    (re.match(r'[_A-Za-z0-9-\.]*{key}\b'.format(key = key), name) or re.match(r'\b{key}[_A-Za-z0-9-\.]*'.format(key = key), name))
                    and is_valid_hardcoded_value(value)
                ):
                    action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                    break

        if token_type == "variable" and name is not None and token.__contains__('funcKeywords'):
            for keyword in token['funcKeywords']:
                for key in common_keywords:

                    if(
                        (re.match(r'[_A-Za-z0-9-\.]*{key}\b'.format(key = key), keyword[0].lower().strip()) or re.match(r'\b{key}[_A-Za-z0-9-\.]*'.format(key = key), keyword[0].lower().strip())) 
                        and is_valid_hardcoded_value(keyword[1])
                    ):
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        break
            

        elif (token_type == "list" or token_type == "set") and name is not None and token.__contains__("values"):

            for key in common_keywords:
                if (re.match(r'[_A-Za-z0-9-\.]*{key}\b'.format(key = key), name) or re.match(r'\b{key}[_A-Za-z0-9-\.]*'.format(key = key), name)):
                    
                    for value in token['values']:
                        if is_valid_hardcoded_value(value): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            
            
        elif token_type == "dict" and token.__contains__("pairs"): 
            for pair in token['pairs']:
                if len(pair) == 2 and isinstance(pair[0], str) and pair[1] is not None:
                    
                    for key in common_keywords:  
                        if re.match(r'[_A-Za-z0-9-\.]*{key}\b'.format(key = key), pair[0].lower().strip()) and is_valid_hardcoded_value(pair[1]): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break


        
        elif token_type == "comparison" and token.__contains__("pairs"):
            for pair in token["pairs"]:
                if len(pair) == 2 and isinstance(pair[0], str) and pair[0] != 'key' and pair[0] != 'token' and pair[1] is not None:  
                    
                    for key in common_keywords:
                        if re.match(r'[_A-Za-z0-9-\.]*{key}\b'.format(key = key), pair[0].lower().strip()) and is_valid_hardcoded_value(pair[1]): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break
                     
        
        elif token_type == "function_call" and token.__contains__('keywords'):
            for keyword in token['keywords']:
                if len(keyword) == 3 and isinstance(keyword[0], str) and isinstance(keyword[1], str) and keyword[2] is True:    
                    
                    for key in common_keywords:
                        if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), keyword[0].lower().strip()) and is_valid_hardcoded_value(keyword[1]): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break
                    

        elif token_type == "function_def" and token.__contains__("args") and token.__contains__("defaults"):    
            defaults_size = len(token['defaults'])
            args = token['args'][-defaults_size:]

            for pair in zip(args, token['defaults']):    
                for key in common_keywords:
                    
                    if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), pair[0].lower().strip()) and pair[1][1] is True and is_valid_hardcoded_value(pair[1][0]): 
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        break
                
             
    except Exception as error: save_token_detection_exception('hard-coded secret detection  '+str(error)+'  '+ str(token), src_file)


def contains_suspicious_strings(value):
    prohibited_values = ['admin', 'root', 'user', 'username', 'pwd', 'pass', 'guest', 'root_password', 'usr',
                        'userpass', 'usrpwd', 'userpassword', 'usrtoken', 'token','default', 'nopassword',
                        'defaultpass', 'password', 'guest', 'root1', 'user root'
                        ]
    
    for prohibited_value in prohibited_values:
        if prohibited_value in value: return True
    return False

def is_valid_hardcoded_value(value):
    new_reg = r'([A-Za-z]*([0-9]+|[!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\'\"-\+\/]+))+([A-Za-z]*([0-9]*|[!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\'\"-\+\/]*))*'

    if isinstance(value, str):
        if len(value) == 0: return False
        elif re.fullmatch(new_reg, value): return True
        elif re.search(r'\\+', value): return False
        elif re.search(r'([!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\'\"-\+\/]+)', value) and len(value) > 1: return True
        # elif re.fullmatch(r'([A-Za-z]*[0-9!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"-\+\/]+)+[A-Za-z]*[0-9!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"\+-\/]*', value): return True
        elif contains_suspicious_strings(value): return True
        else: return False
    
    else: return False
        