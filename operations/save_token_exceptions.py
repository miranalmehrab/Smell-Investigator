from operations.write_to_csv_file import write_to_csv_file

def save_token_for_bug_fix(node, params):
    write_to_csv_file('logs/errors/token_bug_fix.csv', [node,params])

def save_token_detection_exception(error,filename):
    name = filename.name
    name = name.split('/')[-1]
    content = [name, error]
    write_to_csv_file('logs/errors/token_detection_exceptions.csv', [name, error])

def save_token_loading_exception(token,filename):
    name = filename.name
    name = name.split('/')[-1]
    content = [name,token]
    write_to_csv_file('logs/errors/token_loading_exceptions.csv',[name, content])

def save_token_parsing_exception(lineno, error):
    write_to_csv_file('logs/errors/token_parsing_exceptions.csv', [lineno,error])