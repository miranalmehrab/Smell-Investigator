import json

from smells.commandinjection import detect as commandinjectionDetecet
from smells.exec import detect as execDetect
from smells.debugflag import detect as debugflagDetect
from smells.emptypassword import detect as emptypasswordDetect
from smells.hardcodedsecret import detect as hardcodedsecretDetect
from smells.filepermission import detect as filepermissionDetect
from smells.ipbinding import detect as ipbindingDetect
from smells.httponly import detect as httponlyDetect
from smells.sqlinjection import detect as sqlinjectionDetect
from smells.tempdir import detect as tempdirDetect
from smells.ignexcept import detect as ignexceptDetect
from smells.assertstat import detect as assertDetect 
from smells.pickle import detect as pickleDetect
from smells.marshal import detect as marshalDetect
from smells.nointegritycheck import detect as nointegritycheckDetect
from smells.nocertificate import detect as nocertificateDetect
from smells.eval import detect as evalDetect
from smells.yamlload import detect as yamlloadDetect

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

            try:
                commandinjectionDetecet(token, project_name, srcFile)
                execDetect(token, project_name, srcFile)
                debugflagDetect(token, project_name, srcFile)
                emptypasswordDetect(token, project_name, srcFile)
                hardcodedsecretDetect(token, project_name, srcFile)
                filepermissionDetect(token, project_name, srcFile)
                ipbindingDetect(token, project_name, srcFile)
                httponlyDetect(token, project_name, srcFile)
                sqlinjectionDetect(token, project_name, srcFile)
                tempdirDetect(token, project_name, srcFile)
                ignexceptDetect(token, project_name, srcFile)
                assertDetect(token, project_name, srcFile)
                pickleDetect(token, project_name, srcFile)
                marshalDetect(token, project_name, srcFile)
                nocertificateDetect(token, project_name, srcFile)
                nointegritycheckDetect(token, imports, project_name, srcFile)
                evalDetect(token, project_name, srcFile)
                yamlloadDetect(token, project_name, srcFile)

            except Exception as error: save_token_detection_exception(str(error)+'  '+ str(token), srcFile)
            
        except Exception as error: save_token_loading_exception(token+'  '+str(error),srcFile)
        
        