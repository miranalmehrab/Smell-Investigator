from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:

        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        
        insecureMethods = ['hashlib.md5','cryptography.hazmat.primitives.hashes.MD5',
                        'Crypto.Hash.MD2.new','Crypto.Hash.MD4.new','Crypto.Hash.MD5.new',
                        'Crypto.Cipher.ARC2.new','Crypto.Cipher.ARC4.new','Crypto.Cipher.Blowfish.new',
                        'Crypto.Cipher.DES.new,Crypto.Cipher.XOR.new','cryptography.hazmat.primitives.ciphers.algorithms.ARC4',
                        'cryptography.hazmat.primitives.ciphers.algorithms.Blowfish','cryptography.hazmat.primitives.ciphers.algorithms.IDEA',
                        'cryptography.hazmat.primitives.ciphers.modes.ECB','random.random','random.randrange','random.randint','random.choice','random.uniform','random.triangular'
                    ]

        if tokenType == "variable":
            if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]
            if token.__contains__("args"): args = token["args"]
            if valueSrc in insecureMethods and len(args) > 0: 
                action_upon_detection(project_name, srcFile, lineno, 'insecure_cipher_used', 'insecure cipher used', token)

        elif tokenType == "function_call":
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("args"): args = token["args"]
            
            if name in insecureMethods and len(args) > 0: 
                action_upon_detection(project_name, srcFile, lineno, 'insecure_cipher_used', 'insecure cipher used', token)
            
            for arg in args:
                if arg in insecureMethods:
                    action_upon_detection(project_name, srcFile, lineno, 'insecure_cipher_used', 'insecure cipher used', token)

        elif tokenType == "function_def":
            if token.__contains__("return"): funcReturn  = token["return"]
            if token.__contains__("returnArgs"): returnArgs = token["returnArgs"]
            if funcReturn in insecureMethods and len(returnArgs) > 0: 
                action_upon_detection(project_name, srcFile, lineno, 'insecure_cipher_used', 'insecure cipher used', token)
        
    except Exception as error: save_token_detection_exception('cipher detection  '+str(error)+'  '+ str(token), srcFile)
    