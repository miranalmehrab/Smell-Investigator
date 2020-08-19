from operations.saveDetectedSmells import saveDetectedSmells

def actionUponDetection(project_name, srcFile, lineno, smell, msg):
    saveDetectedSmells(smell, project_name, srcFile, lineno)
    print(msg +' at line '+ str(lineno))
