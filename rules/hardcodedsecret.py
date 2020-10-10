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
        
        commonKeywords = ['auth_key','user-id', 'cert','passno','pass-no', 'pass_no', 'auth_token', 'authetication_token','auth-token', 'authentication-token', 
                        'user', 'uname', 'username', 'user-name', 'user_name', 'owner-name', 'owner_name', 'owner', 'admin', 'login', 'pass', 'pwd', 'password',
                        'passwd', 'secret', 'uuid', 'uid', 'user_id', 'u_id', 'upwd', 'user_pwd', 'crypt', 'certificate', 'userid', 'loginid', 'log_in', 'login_id', 
                        'ssh_key','user_logid', 'ulogin', 'name_id', 'user_token', 'utoken', 'user-token', 'uauth', 'u_auth', 'user_auth', 'user-auth', 'user-key' 
                        'md5', 'rsa', 'ssl_content', 'ca_content','ssl-content', 'ca-content', 'ssh_key_content', 'ssh-key-content', 'ssh_key_public', 'ssh-key-public', 
                        'ssh_key_private', 'ssh-key-private','ssh_key_public_content', 'ssh_key_private_content', 'ssh-key-public-content', 'ssh-key-private-content',
                        'user_key', 'ukey', 'private_key', 'public_key', 'key_private', 'key_public', 'tls-key', 'tls_key', 'ssl-key', 'ssl-private-key', 'tls-private-key',
                        'ssl-public-key', 'tls-public-key', 'ssl_private_key',  'tls_private_key', 'ssl', 'tls', 'public-key', 'private-key', '_key', '-key', '_passwd',
                        '-passwd', '-token', '_token'
                    ]
        
        commonPasswords = [ 'password','passwords','pass','pwd','userpassword','userpwd', 'userpass', 'pass_no', 'pass-no', 'user-pass', 'upass', 'user_pass', 
                            'u_pass', 'user_pwd', 'uid', 'usr_pwd', 'usr_pass', 'usr-pass', 'userpasswords', 'user-passwords', 'user-password', 'user_password', 
                            'use_pass', 'admin_id', 'guest_id', 'admin_pass', 'guest_pass'
                        ]

        if tokenType == "variable" and name is not None and value is not None and valueSrc == "initialization":
            for key in commonKeywords:
                if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), name.lower().strip()):
                    if isinstance(value, str) and len(value) > 0 and is_valid(value):
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        break
                    
            for pwd in commonPasswords:
                if re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), name.lower().strip()):
                    if isinstance(value, str) and len(value) > 0 and is_valid(value):
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        break

        elif (tokenType == "list" or tokenType == "set") and name is not None and token.__contains__("values"):
            for key in commonKeywords:
                if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), name.lower().strip()) and len(token['values']) > 0: 
                    action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                    break
            
            for pwd in commonPasswords:
                if re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), name.lower().strip()) and len(token['values']) > 0: 
                    action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                    break
            

        elif tokenType == "dict" and name is not None and token.__contains__("keys"):
            for key in commonKeywords:
                if re.match(r'[_A-Za-z0-9-]*{key}\b'.format(key = key), name.lower().strip()) and len(token['keys']) > 0:
                    action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token) 
                    break

            for pwd in commonKeywords:
                if re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), name.lower().strip()) and len(token['keys']) > 0:
                    action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token) 
                    break
            

            if token.__contains__('values'): 
                for value_pair in zip(token['keys'], token['values']):        
                    if len(value_pair) == 2 and value_pair[0] is not None and isinstance(value_pair[0], str) and (value_pair[0].lower() in commonPasswords or value_pair[0].lower() in commonKeywords) and (value_pair[1] is not None and len(str(value_pair[1])) > 0 and is_valid(value_pair[1])):
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                        
        
        elif tokenType == "comparison" and token.__contains__("pairs"):
            for pair in token["pairs"]:
                if len(pair) == 2 and pair[0] is not None and pair[1] is not None:
                    if isinstance(pair[0], str) and (pair[0].lower() in commonKeywords or pair[0].lower() in commonPasswords) and pair[1] is not None and len(str(pair[1])) > 0 and is_valid(pair[1]): 
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                    
        
        elif tokenType == "function_call" and token.__contains__('keywords'):
            for keyword in token['keywords']:

                if len(keyword) == 2 and isinstance(keyword[0], str) and keyword[0].lower() is not None and keyword[1] is not None and len(str(keyword[1])) > 0:
                    if keyword[0] in commonKeywords or keyword[0] in commonPasswords:
                        action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)
                    
        elif tokenType == "function_def" and token.__contains__("args") and token.__contains__("defaults"):
            if len(token["args"]) == len(token["defaults"]):
                
                for pair in zip(token['args'], token['defaults']):    
                    if isinstance(pair[0], str) and pair[0] is not None and pair[1] is not None and len(str(pair[1])) > 0:
                        if pair[0].lower() in commonKeywords or pair[0].lower() in commonPasswords: 
                            action_upon_detection(project_name, src_file, lineno, 'hard-coded secrets', 'hard-coded secrets', token)

    except Exception as error: save_token_detection_exception('hard-coded secret detection  '+str(error)+'  '+ str(token), src_file)

def is_valid(value):
    if isinstance(value, str):
        if value.find('self.') != -1: return False
        elif value.find('request.') != -1: return False 
        elif value.find('post.') != -1: return False
        elif value.find('tokens.') != -1: return False
        elif value.find('forms.') != -1: return False
        elif value.find('os.environ') != -1: return False

        return True
        
    else: return True