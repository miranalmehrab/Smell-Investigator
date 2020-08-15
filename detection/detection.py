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

from operations.saveDetectionExceptions import saveDetectionExceptions
from operations.tokenLoadingExceptions import tokenLoadingExceptions

def getImports(tokens):
    
    imports = []
    tokens = tokens.splitlines()

    for token in tokens:
        try: 
            token = json.loads(token)
            if token['type'] == 'import': imports.append(token['og'])


        except Exception as error:
            print(str(error))
    
    return imports

def detection(tokens, srcFile):
    
    imports = getImports(tokens)
    tokens = tokens.splitlines()
    
    for token in tokens:
        try:
            token = json.loads(token)

            try:
                commandinjectionDetecet(token, srcFile)
                execDetect(token, srcFile)
                debugflagDetect(token, srcFile)
                emptypasswordDetect(token, srcFile)
                hardcodedsecretDetect(token, srcFile)
                filepermissionDetect(token, srcFile)
                ipbindingDetect(token, srcFile)
                httponlyDetect(token, srcFile)
                sqlinjectionDetect(token, srcFile)
                tempdirDetect(token, srcFile)
                ignexceptDetect(token, srcFile)
                assertDetect(token, srcFile)
                pickleDetect(token, srcFile)
                marshalDetect(token, srcFile)
                nocertificateDetect(token, srcFile)
                nointegritycheckDetect(token, imports, srcFile)
                evalDetect(token, srcFile)
                yamlloadDetect(token, srcFile)

            except Exception as error: saveDetectionExceptions(str(error)+' - '+ str(token), srcFile)
            
        except Exception as error: tokenLoadingExceptions(token+' - '+str(error),srcFile)
        
        