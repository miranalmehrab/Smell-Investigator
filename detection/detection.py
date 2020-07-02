import json

from smells.cliargs import detect as cliargsDetect
from smells.exec import detect as execDetect
from smells.debugflag import detect as debugflagDetect
from smells.emptypassword import detect as emptypasswordDetect
from smells.hardcodedsecret import detect as hardcodedsecretDetect
from smells.filepermission import detect as filepermissionDetect
from smells.ipbinding import detect as ipbindingDetect


def detection(tokens):
    tokens = tokens.splitlines()
    
    for token in tokens:
        token = json.loads(token)

        cliargsDetect(token)
        execDetect(token)
        debugflagDetect(token)
        emptypasswordDetect(token)
        hardcodedsecretDetect(token)
        filepermissionDetect(token)
        ipbindingDetect(token)
