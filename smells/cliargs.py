def detect(token):

    if token.__contains__("line"): lineno = token["line"] 
    if token.__contains__("name"): methodname = token["name"]
    if token.__contains__("args"): args = token["args"]
    if token.__contains__("hasInputs"): containsUserInput =  token["hasInputs"]

    cliArgsFuncNames = ['sys.argv', 'ArgumentParser', 'argparse', 'subprocess.Popen']
    
    if methodname in cliArgsFuncNames and containsUserInput:
        warning = 'possible use of command line args at line ' +  str(lineno)
        print(warning)
