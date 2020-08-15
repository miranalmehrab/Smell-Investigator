from operations.actionUponDetection import actionUponDetection

def detect(token, srcFile):
    
    if token.__contains__("line"): lineno = token["line"]
    if token.__contains__("type"): tokenType = token["type"]
    if token.__contains__("name"): name = token["name"]
    if token.__contains__("value"): value = token["value"]
    if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
    
    commonKeywords = ['key','id', 'cert', 'root','passno','pass-no', 'pass_no', 'auth_token', 'authetication_token','auth-token', 'authentication-token', 'user', 'uname', 'username', 'user-name', 'user_name', 'owner-name', 'owner_name', 'owner', 'admin', 'login', 'pass', 'pwd', 'password', 'passwd', 'secret', 'uuid', 'crypt', 'certificate', 'userid', 'loginid', 'token', 'ssh_key', 'md5', 'rsa', 'ssl_content', 'ca_content', 'ssl-content', 'ca-content', 'ssh_key_content', 'ssh-key-content', 'ssh_key_public', 'ssh-key-public', 'ssh_key_private', 'ssh-key-private', 'ssh_key_public_content', 'ssh_key_private_content', 'ssh-key-public-content', 'ssh-key-private-content']
    commonPassword = ['password','passwords','pass','pwd','userpassword','userpwd', 'userpass', 'pass_no', 'pass-no', 'user-pass', 'upass']

    if tokenType == "variable" and valueSrc == "initialized" and (name.lower() in commonKeywords or name.lower() in commonPassword) and value != None and len(value)>0 : 
        actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret')
        
    elif tokenType == "comparison" and token.__contains__("pairs"):
        for pair in token["pairs"]:        
            if len(pair) == 2 and (pair[0].lower() in commonKeywords or pair[0].lower() in commonPassword) and len(pair[1]) > 0: actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret')
            elif len(pair) == 2 and (pair[1].lower() in commonKeywords or pair[1].lower() in commonPassword) and len(pair[0]) > 0: actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret')
    
    elif (tokenType == "list" or tokenType=="set") and token.__contains__("values"):
        if (name.lower() in commonKeywords or name.lower() in commonPassword) and len(token['values'])>0: actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret')
    
    elif tokenType == "dict" and token.__contains__("keys"):
        if (name.lower() in commonKeywords or name.lower() in commonPassword) and len(token['keys'])>0: actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret') 
        for key in token["keys"]: 
            if key.lower() in commonKeywords or key.lower() in commonPassword: actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret')

    elif tokenType == "function_call" and token.__contains__('keywords'):
        for keyword in token['keywords']:
            if len(keyword) == 2 and (keyword[0].lower() in commonKeywords or keyword[0].lower() in commonPassword) and len(keyword[1])>0: actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret')

    elif tokenType == "function_def" and token.__contains__("args") and token.__contains__("defaults"):
        for arg in token["args"]:
            if (arg.lower() in commonKeywords or arg.lower() in commonPassword) and len(token["args"]) == len(token["args"]): actionUponDetection(srcFile, lineno, 'hardcoded_secret', 'hardcoded secret') 
