def clearFileContent(filename):
    
    with open(filename, 'w+') as fp: fp.close()