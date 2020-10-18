from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        
        insecureMethods = ['hashlib.md5','cryptography.hazmat.primitives.hashes.MD5','Crypto.Hash.MD2.new','Crypto.Hash.MD4.new','Crypto.Hash.MD5.new',
                        'Crypto.Cipher.ARC2.new','Crypto.Cipher.ARC4.new','Crypto.Cipher.Blowfish.new', 'Crypto.Cipher.DES.new,Crypto.Cipher.XOR.new',
                        'cryptography.hazmat.primitives.ciphers.algorithms.ARC4', 'cryptography.hazmat.primitives.ciphers.algorithms.Blowfish',
                        'cryptography.hazmat.primitives.ciphers.algorithms.IDEA','cryptography.hazmat.primitives.ciphers.modes.ECB','random.random',
                        'random.randrange','random.randint','random.choice','random.uniform','random.triangular'
                    ]

        if tokenType == "variable":
            if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
            if token.__contains__("args"): args = token["args"]
            if valueSrc in insecureMethods:
                action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)

        if tokenType == "dict" and token.__contains__('keys') and token.__contains__('values'):
            for value_pair in zip(token['keys'], token['values']):  
                if len(value_pair) == 2 and ((value_pair[0] is not None and value_pair[0]in insecureMethods) or (value_pair[1] is not None and value_pair[1] in insecureMethods)):
                    action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)
            

        elif tokenType == "function_call":
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("args"): args = token["args"]
            
            if name in insecureMethods: 
                action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)
            
            for arg in args:
                if arg in insecureMethods:
                    action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)

            if name in insecureMethods and token.__contains__('keywords') and len(token['keywords']) > 0:
                action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)
            
            if token.__contains__('keywords') and len(token['keywords']) > 0:
                for keyword in token['keywords']:
                    if keyword[1] is not None and keyword[1] in insecureMethods:
                        action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)

        elif tokenType == "function_def":
            returnArgs = []
            if token.__contains__("return"): funcReturn  = token["return"]
            if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
            
            if funcReturn in insecureMethods: 
                action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)

            for arg in returnArgs:
                if arg in insecureMethods:
                    action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)


    except Exception as error: save_token_detection_exception('cipher detection  '+str(error)+'  '+ str(token), src_file)
    