import json

from rules.cipher import detect as cipherDetection
from rules.commandinjection import detect as commandinjectionDetecet
from rules.dynamicode import detect as dynamicodeDetect
from rules.debugflag import detect as debugflagDetect
from rules.emptypassword import detect as emptypasswordDetect
from rules.hardcodedsecret import detect as hardcodedsecretDetect
from rules.filepermission import detect as filepermissionDetect
from rules.ipbinding import detect as ipbindingDetect
from rules.httponly import detect as httponlyDetect
from rules.sqlinjection import detect as sqlinjectionDetect
from rules.tempdir import detect as tempdirDetect
from rules.ignexcept import detect as ignexceptDetect
from rules.assertstat import detect as assertDetect 
from rules.deserialization import detect as deserializationDetect
from rules.nointegritycheck import detect as nointegritycheckDetect
from rules.nocertificate import detect as nocertificateDetect
from rules.xss import detect as xssDetect
from rules.yamlload import detect as yamlloadDetect

from operations.save_token_exceptions import save_token_detection_exception
from operations.save_token_exceptions import save_token_loading_exception

def getImports(tokens):
    
    imports = []
    tokens = tokens.splitlines()

    for token in tokens:
        try: 
            token = json.loads(token)
            if token['type'] == 'import':
                imports.append(token['og'])

        except Exception as error:
            print(str(error))
    
    return imports


def detection(tokens, project_name, srcFile):
    imports = getImports(tokens)
    tokens = tokens.splitlines()
    
    for token in tokens:
        try:
            token = json.loads(token)

            cipherDetection(token, project_name, srcFile)
            commandinjectionDetecet(token, project_name, srcFile)
            debugflagDetect(token, project_name, srcFile)
            dynamicodeDetect(token, project_name, srcFile)
            emptypasswordDetect(token, project_name, srcFile)
            hardcodedsecretDetect(token, project_name, srcFile)
            filepermissionDetect(token, project_name, srcFile)
            ipbindingDetect(token, project_name, srcFile)
            httponlyDetect(token, project_name, srcFile)
            sqlinjectionDetect(token, project_name, srcFile)
            tempdirDetect(token, project_name, srcFile)
            ignexceptDetect(token, project_name, srcFile)
            assertDetect(token, project_name, srcFile)
            deserializationDetect(token, project_name, srcFile)
            nocertificateDetect(token, project_name, srcFile)
            nointegritycheckDetect(token, imports, project_name, srcFile)
            xssDetect(token, project_name, srcFile)
            yamlloadDetect(token, project_name, srcFile)

        except Exception as error: 
            save_token_loading_exception(str(token)+'  '+str(error),srcFile)
        
        