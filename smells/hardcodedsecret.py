from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("value"): value = token["value"]
        if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
        
        commonKeywords = ['key','id', 'cert', 'root','passno','pass-no', 'pass_no', 'auth_token', 'authetication_token','auth-token', 'authentication-token', 
                        'user', 'uname', 'username', 'user-name', 'user_name', 'owner-name', 'owner_name', 'owner', 'admin', 'login', 'pass', 'pwd', 'password',
                        'passwd', 'secret', 'uuid', 'crypt', 'certificate', 'userid', 'loginid', 'token', 'ssh_key', 'md5', 'rsa', 'ssl_content', 'ca_content',
                        'ssl-content', 'ca-content', 'ssh_key_content', 'ssh-key-content', 'ssh_key_public', 'ssh-key-public', 'ssh_key_private', 'ssh-key-private',
                        'ssh_key_public_content', 'ssh_key_private_content', 'ssh-key-public-content', 'ssh-key-private-content']
        
        commonPasswords = ['password','passwords','pass','pwd','userpassword','userpwd', 'userpass', 'pass_no', 'pass-no', 'user-pass', 'upass']

        if tokenType == "variable" and name is not None and value is not None and valueSrc == "initialized":
            if (name.lower() in commonKeywords or name.lower() in commonPasswords) and len(value) > 0:
                action_upon_detection(project_name, src_file, lineno, 'hardcoded_secret', 'hardcoded secret', token)
            

        elif (tokenType == "list" or tokenType == "set") and name is not None and token.__contains__("values"):
            if (name.lower() in commonKeywords or name.lower() in commonPasswords) and len(token['values']) > 0: 
                action_upon_detection(project_name, src_file, lineno, 'hardcoded_secret', 'hardcoded secret', token)
            
        elif tokenType == "dict" and name is not None and token.__contains__("keys"):
            if(name.lower() in commonKeywords or name.lower() in commonPasswords) and len(token['keys']) > 0: 
                action_upon_detection(project_name, src_file, lineno, 'hardcoded_secret', 'hardcoded secret', token) 
            
            for key in token["keys"]:
                if key in commonKeywords or key in commonPasswords: 
                    action_upon_detection(project_name, src_file, lineno, 'hardcoded_secret', 'hardcoded secret', token)
                
        
        elif tokenType == "comparison" and token.__contains__("pairs"):
            for pair in token["pairs"]:
                if len(pair) == 2 and pair[0] is not None and pair[1] is not None:
                    if pair[0] in commonKeywords or pair[0] in commonPasswords: action_upon_detection(project_name, src_file, lineno, 'hardcoded_secret', 'hardcoded secret', token)
                    elif pair[1] in commonKeywords or pair[1] in commonPasswords: action_upon_detection(project_name, src_file, lineno, 'hardcoded_secret', 'hardcoded secret', token)
                    
        
        elif tokenType == "function_call" and token.__contains__('keywords'):
            for keyword in token['keywords']:

                if len(keyword) == 2 and keyword[0] is not None and keyword[1] is not None:
                    if keyword[0] in commonKeywords or keyword[0] in commonPasswords: 
                        action_upon_detection(project_name, src_file, lineno, 'hardcoded_secret', 'hardcoded secret', token)
                    
        elif tokenType == "function_def" and token.__contains__("args") and token.__contains__("defaults"):
            if len(token["args"]) == len(token["defaults"]):
                
                for pair in zip(token['args'], token['defaults']):    
                    if pair[0] is not None and pair[1] is not None:
                        if pair[0] in commonKeywords or pair[0] in commonPasswords: action_upon_detection(project_name, src_file, lineno, 'hardcoded_secret', 'hardcoded secret', token) 
    
    except Exception as error: save_token_detection_exception('hard-coded secret detection  '+str(error)+'  '+ str(token), srcFile)