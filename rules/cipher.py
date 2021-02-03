from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class Cipher: 
    '''This is the class for detecting weak cryptographic algorithm in code'''

    def __init__(self):
        self.insecure_methods = [ 'yaml.load', 'yaml.load_all', 'yaml.full_load', 'yaml.dump', 'yaml.dump_all', 'yaml.full_load_all']
        self.detetcion_message = 'use of insecure YAML operations'


    def detect(token, project_name, src_file):
        try:

            if token.__contains__("line"): lineno = token["line"]
            if token.__contains__("type"): tokenType = token["type"]
            
            insecure_methods = ['hashlib.md5','cryptography.hazmat.primitives.hashes.MD5','Crypto.Hash.MD2.new','Crypto.Hash.MD4.new','Crypto.Hash.MD5.new',
                            'Crypto.Cipher.ARC2.new','Crypto.Cipher.ARC4.new','Crypto.Cipher.Blowfish.new', 'Crypto.Cipher.DES.new,Crypto.Cipher.XOR.new',
                            'cryptography.hazmat.primitives.ciphers.algorithms.ARC4', 'cryptography.hazmat.primitives.ciphers.algorithms.Blowfish',
                            'cryptography.hazmat.primitives.ciphers.algorithms.IDEA','cryptography.hazmat.primitives.ciphers.modes.ECB','random.random',
                            'random.randrange','random.randint','random.choice','random.uniform','random.triangular', 'Cryptodome.Cipher.ARC2.new',
                            'Cryptodome.Cipher.ARC4.new','Cryptodome.Cipher.Blowfish.new','Cryptodome.Cipher.DES.new','Cryptodome.Cipher.XOR.new',
                            'cryptography.hazmat.primitives.ciphers.algorithms.ARC4','cryptography.hazmat.primitives.ciphers.algorithms.Blowfish',
                            'cryptography.hazmat.primitives.ciphers.algorithms.IDEA', 'cryptography.hazmat.primitives.ciphers.modes.ECB',
                            'Cryptodome.Hash.MD2.new','Cryptodome.Hash.MD4.new','Cryptodome.Hash.MD5.new','Cryptodome.Hash.SHA.new',
                            'cryptography.hazmat.primitives.hashes.SHA1'
                        ]

            if tokenType == "variable" and token.__contains__("valueSrc") and token["valueSrc"] in insecure_methods:
                    action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)

            elif tokenType == "function_call":
                
                if token["name"] is not None and token["name"].lower().strip() in insecure_methods: 
                    action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)
                
                elif token["name"].lower().strip() == 'hashlib.new':
                    black_listed_args = ['md4', 'md5', 'sha', 'sha1']
                    for arg in token["args"]:
                        if arg in black_listed_args:
                            action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)

                # elif token["name"] in ['dsa.generate', 'rsa.generate'] and len(token['args'] > 0):
                    



                if token.__contains__('keywords') and len(token['keywords']) > 0:
                    for keyword in token['keywords']:
                        if keyword[1] is not None and keyword[1] in insecure_methods and keyword[2] is False:
                            action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)

            elif tokenType == "function_def":
                smell_found_in_return_statement = False

                if token.__contains__("return") and token["return"] is not None:
                    for func_return in token["return"]:
                        if func_return in insecure_methods:
                            smell_found_in_return_statement = True
                            if token.__contains__('returnLine'): lineno = token['returnLine']
                            action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)

                if smell_found_in_return_statement is False and token.__contains__("returnArgs"):
                    for arg in token["returnArgs"]:
                        if arg in insecure_methods:
                            action_upon_detection(project_name, src_file, lineno, 'use of weak cryptographic algorithm', 'use of weak cryptographic algorithm', token)


        except Exception as error: save_token_detection_exception('cipher detection  '+str(error)+'  '+ str(token), src_file)
        