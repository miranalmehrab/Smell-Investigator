from operations.saveDetectedSmells import saveDetectedSmells

def actionUponDetection(srcFile, lineno, smell, msg):
    saveDetectedSmells(smell, srcFile)
    print(msg +' at line '+ str(lineno))
