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
        

        commonKeywords = [  '_key','_id','-key', 'cert', '_root','-root','passno','pass-no', 'pass_no', 'auth_token', 'authetication_token','auth-token', 'authentication-token', 
                            'user', 'uname','username', 'user-name','user_name', 'owner-name', 'owner_name', 'owner', 'admin', 'pass', 'pwd', 'password', 
                            'passwd', 'secret', 'uuid','crypt', 'certificate', 'userid','ssh_key', 'md5', 'rsa', 'ssl_content', 'ca_content',
                            'ssl-content', 'ca-content', 'ssh_key_content','ssh-key-content', 'ssh_key_public', 'ssh-key-public', 'ssh_key_private','ssh-key-private',
                            'ssh_key_public_content', 'ssh_key_private_content','ssh-key-public-content', 'ssh-key-private-content','admin', 'username',
                            'guest', 'root_password', 'usr', 'userpass', 'usrpwd', 'userpassword', 'usrtoken', 'nopassword'
                        ]

        if tokenType == "variable" and name is not None and value is not None and valueSrc == "initialization":
            for key in commonKeywords:
                if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), name.lower().strip()) or re.match(r'\b{key}[_A-Za-z0-9-]*'.format(key = key), name.lower().strip()):
                    if  is_value_valid(value):
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        break

        if tokenType == "variable" and name is not None and value is None and token.__contains__('funcKeywords'):
            found_something = False
            for keyword in token['funcKeywords']:
                for key in commonKeywords:
                    if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), keyword[0].lower().strip()) and is_value_valid(keyword[1]):
                        print(keyword)
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        found_something = True
                        break

                if found_something: break
        
            
        elif (tokenType == "list" or tokenType == "set") and name is not None and token.__contains__("values"):
            for key in commonKeywords:
                
                if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), name.lower().strip()):
                    for value in token['values']:

                        if is_value_valid(value): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break
            
        elif tokenType == "dict" and name is not None and token.__contains__("keys") and token.__contains__('values'): 
            for key in commonKeywords:
                if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), name.lower().strip()): 
                    
                    value_pairs = zip(token['keys'], token['values'])
                    for value_pair in value_pairs:        
                
                        if len(value_pair) == 2 and value_pair[0] is not None and isinstance(value_pair[0], str) and value_pair[1] is not None:
                            for key in commonKeywords:

                                if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), value_pair[0].lower().strip()) and is_value_valid(value_pair[1]): 
                                    action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                                    break


        
        elif tokenType == "comparison" and token.__contains__("pairs"):
            for pair in token["pairs"]:
                
                if len(pair) == 2 and pair[0] is not None and isinstance(pair[0], str) and pair[0] != 'key' and pair[0] != 'token' and pair[1] is not None:  
                    for key in commonKeywords:

                        if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), pair[0].lower().strip()) and is_value_valid(pair[1]): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break
                     
        
        elif tokenType == "function_call" and token.__contains__('keywords'):
            for keyword in token['keywords']:
                
                if len(keyword) == 2 and isinstance(keyword[0], str) and keyword[0].lower() is not None and keyword[1] is not None:    
                    for key in commonKeywords:

                        if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), keyword[0].lower().strip()) and is_value_valid(keyword[1]): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break
                    

        elif tokenType == "function_def" and token.__contains__("args") and token.__contains__("defaults"):
            if len(token["args"]) == len(token["defaults"]):
                
                pairs = zip(token['args'], token['defaults'])
                for pair in pairs:    
                    
                    for key in commonKeywords:
                        if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), pair[0].lower().strip()) and is_value_valid(pair[1]): 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                            break
                    
             
    except Exception as error: save_token_detection_exception('hard-coded secret detection  '+str(error)+'  '+ str(token), src_file)


def contains_suspicious_strings(value):
    prohibitedStrings = ['admin', 'root', 'user', 'username', 'pwd', 'pass', 'guest', 'root_password', 'usr', 'userpass', 'usrpwd', 'userpassword', 'usrtoken', 'token',
                        'default', 'nopassword', 'defaultpass', 'password', 'guest', 'root1'
                        ]
    
    if value in prohibitedStrings: return True
    return False

def is_value_valid(value):
    new_reg = r'([A-Za-z]*([0-9]+|[!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"-\+\/]+))+([A-Za-z]*([0-9]*|[!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"-\+\/]*))*'

    if value is None: return False
    elif isinstance(value, bool): return False
    elif isinstance(value, str):
        if len(value) == 0: return False
        elif re.search(r'([!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\'\"-\+\/]+)', value) and len(value) > 1: return True
        elif re.search(r'\.+', value): return False
        elif re.search(r'\\+', value): return False
        elif re.search(r'/+', value): return False
        elif re.search(r'\[+', value): return False
        elif re.search(r'\]+', value): return False
        elif re.search(r'[0-9]+', value): return True
        elif re.fullmatch(new_reg, value): return True
        # elif re.fullmatch(r'([A-Za-z]*[0-9!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"-\+\/]+)+[A-Za-z]*[0-9!\?@#\$%\^&\*\(\)\{\}\[\]_=?<>:\.\'\"\+-\/]*', value): return True
        elif contains_suspicious_strings(value): return True
    
    elif isinstance(value, int):
        if len(str(value)) > 1: return True

    else: return False
        