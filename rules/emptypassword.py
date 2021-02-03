import re
import time

from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

class EmptyPassword:
    '''This is the class for detecting empty passwords in code'''

    def __init__(self):
        self.insecure_methods = [ 'yaml.load', 'yaml.load_all', 'yaml.full_load', 'yaml.dump', 'yaml.dump_all', 'yaml.full_load_all']
        self.detetcion_message = 'use of insecure YAML operations'

    def detect(token, project_name, src_file):
        try:
            if token.__contains__("line"): lineno = token["line"]
            if token.__contains__("type"): token_type = token["type"]
            if token.__contains__("name"): name = token["name"]
            if token.__contains__("value"): value = token["value"]
            if token.__contains__("valueSrc"): valueSrc = token["valueSrc"]

            common_passwords = ['password','pass','pwd','passwd', 'upass']
            
            if( 
                token_type == "variable" 
                and name is not None
                and isinstance(value, str)  
                and (value is None or len(value) == 0) 
                and token.__contains__('values') is False
                and valueSrc == "initialization"
            ):  
                for pwd in common_passwords:
                    if (re.match(r'[_A-Za-z0-9-\.]*{pwd}\b'.format(pwd = pwd), name.lower().strip()) or re.match(r'\b{pwd}[_A-Za-z0-9-\.]*'.format(pwd = pwd), name.lower().strip())):
                        action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                        break


            elif token_type == "dict" and name is not None and token.__contains__("pairs"):
                
                for pair in token['pairs']:
                    for pwd in common_passwords:
                        if(
                            isinstance(pair[0], str) 
                            and (re.match(r'[_A-Za-z0-9-\.]*{pwd}\b'.format(pwd = pwd), pair[0].lower().strip()) or re.match(r'\b{pwd}[_A-Za-z0-9-\.]*'.format(pwd = pwd), pair[0].lower().strip())) 
                            and (pair[1] is None or len(pair[1]) == 0)
                        ):   
                            action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
            

            elif token_type == "comparison" and token.__contains__("pairs"):
                
                for pair in token["pairs"]:
                    for pwd in common_passwords:
                        if(
                            isinstance(pair[0], str)
                            and (re.match(r'[_A-Za-z0-9-\.]*{pwd}\b'.format(pwd = pwd), pair[0].lower().strip()) or re.match(r'\b{pwd}[_A-Za-z0-9-\.]*'.format(pwd = pwd), pair[0].lower().strip())) 
                            and (pair[1] is None or (isinstance(pair[1], str) and len(pair[1]) == 0))
                        ):    
                            action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                            break

            elif token_type == "function_call" and token.__contains__('keywords'):
                for keyword in token['keywords']:
                    for pwd in common_passwords:
                
                        if (
                            len(keyword) == 3
                            and isinstance(keyword[0], str) 
                            and re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), keyword[0].lower().strip()) 
                            and (keyword[1] is None or len(str(keyword[1])) == 0) and keyword[2] is True
                        ): 
                                action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                                break

            elif token_type == "function_def" and token.__contains__("args") and token.__contains__("defaults"):
                defaults_size = len(token['defaults'])
                args = token['args'][-defaults_size:]

                for pair in zip(args, token['defaults']):
                        for pwd in common_passwords:
                            if re.match(r'[_A-Za-z0-9-]*{pwd}\b'.format(pwd = pwd), pair[0].lower().strip()) and (pair[1][0] == None or len(str(pair[1][0])) == 0) and pair[1][1] is True: 
                                action_upon_detection(project_name, src_file, lineno, 'empty password', 'empty password', token)
                                break

        except Exception as error: save_token_detection_exception('empty password detection  '+str(error)+'  '+ str(token), src_file)