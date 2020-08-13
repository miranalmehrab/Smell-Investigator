import json

from smells.cliargs import detect as cliargsDetect
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
from smells.eval import detect as evalDetect
from smells.yamlload import detect as yamlloadDetect

from operations.clearFileContent import clearFileContent
from operations.compareDetectionAccuracy import compareDetectionAccuracy

def detection(tokens, srcFile):
    
    clearFileContent('detected_smells.csv')
    tokens = tokens.splitlines()
    
    for token in tokens:
        token = json.loads(token)

        cliargsDetect(token, srcFile)
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
        evalDetect(token, srcFile)
        yamlloadDetect(token, srcFile)
    
    compareDetectionAccuracy()