import json

# from rules.commandinjection import detect as commandinjectionDetecet
# from rules.dynamicode import detect as dynamicodeDetect
# from rules.emptypassword import detect as emptypasswordDetect
# from rules.hardcodedsecret import detect as hardcoded_secret_detect
# from rules.ipbinding import detect as ipbindingDetect
# from rules.httponly import detect as httponlyDetect
# from rules.ignexcept import detect as ignexceptDetect
# from rules.assertstat import detect as assertDetect 
# from rules.deserialization import detect as deserializationDetect
# from rules.yamlload import detect as yamlloadDetect

from rules.xss import Xss
from rules.cipher import Cipher
from rules.debugflag import DebugFlag
from rules.tempdir import TmpDirectory
from rules.yamlload import YamlOperations 
from rules.sqlinjection import SqlInjection
from rules.nocertificate import NoCertificate
from rules.nointegritycheck import NoIntegrity
from rules.filepermission import FilePermission

from operations.save_token_exceptions import save_token_detection_exception
from operations.save_token_exceptions import save_token_loading_exception

def get_imports_in_code(tokens):
    
    imports = []
    for token in tokens:
        try: 
            token = json.loads(token)
            if token['type'] == 'import':
                imports.append(token['og'])

        except Exception as error: print(str(error))
    
    return imports


def detection(tokens, project_name, srcFile):
    tokens = tokens.splitlines()
    imports = get_imports_in_code(tokens)
    
    xss = Xss()
    cipher = Cipher()
    yaml = YamlOperations()
    debug_flag = DebugFlag()
    tmp_dir = TmpDirectory()
    no_integrity = NoIntegrity()
    sql_injection = SqlInjection()
    no_certificate = NoCertificate()
    file_permission = FilePermission()


    for token in tokens:
        try:
            token = json.loads(token)
            
            # xss.detect_smell(token, project_name, srcFile)
            # yaml.detect_smell(token, project_name, srcFile)
            # tmp_dir.detect_smell(token, project_name, srcFile)
            # no_integrity.detect_smell(token, imports, project_name, srcFile)
            # sql_injection.detect_smell(token, project_name, srcFile)
            # cipher.detect_smell(token, project_name, srcFile)
            # debug_flag.detect_smell(token, project_name, srcFile)
            # no_certificate.detect_smell(token, project_name, srcFile)
            
            file_permission.detect_smell(token, project_name, srcFile)

            # yamlloadDetect(token, project_name, srcFile)
            # xssDetect(token, project_name, srcFile)
            # tempdirDetect(token, project_name, srcFile)
            # ipbindingDetect(token, project_name, srcFile)
            
            # deserializationDetect(token, project_name, srcFile)
            
            # emptypasswordDetect(token, project_name, srcFile)
            # httponlyDetect(token, project_name, srcFile)
            # dynamicodeDetect(token, project_name, srcFile)
            # sqlinjectionDetect(token, project_name, srcFile)
            # commandinjectionDetecet(token, project_name, srcFile)
            # hardcoded_secret_detect(token, project_name, srcFile)
            
            # ignexceptDetect(token, project_name, srcFile)
            # assertDetect(token, project_name, srcFile)

        except Exception as error: 
            save_token_loading_exception(str(token)+'  '+str(error),srcFile)
        
        