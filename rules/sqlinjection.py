from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): token_type = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]

        queryMethods = ['execution.query', 'connection.cursor.execute', 'sqlite3.connect.execute',
                        'psycopg2.connect.cursor.execute','mysql.connector.connect.cursor.execute', 
                        'pyodbc.connect.cursor.execute', 'sqlalchemy.sql.text']
        
        if token_type == "variable" and token.__contains__('valueSrc') and token.__contains__('args'):
            
            args = token['args']
            valueSrc = token['valueSrc']
            if(valueSrc in queryMethods or query_methods_has_patterns(valueSrc)) and token['isInput'] is True:
                action_upon_detection(project_name, src_file, lineno, 'constructing sql statement upon user input', 'constructing sql statement upon user input', token)
                    
        elif token_type == "function_call" and (name in queryMethods or  query_methods_has_patterns(name)) and token['hasInputs'] is True:
            action_upon_detection(project_name, src_file, lineno, 'constructing sql statement upon user input', 'constructing sql statement upon user input', token)
        
        elif token_type == "function_def" and token.__contains__('return') and token.__contains__('returnHasInputs'): 
            if (token['return'] in queryMethods or query_methods_has_patterns(token['return'])) and token['returnHasInputs'] is True:
                action_upon_detection(project_name, src_file, lineno, 'constructing sql statement upon user input', 'constructing sql statement upon user input', token)
        

    except Exception as error: save_token_detection_exception('constructing sql statement upon user input detection  '+str(error)+'  '+ str(token), src_file)

def query_methods_has_patterns(name):
    methods = ['objects.extra', 'objects.raw']

    if name is None: return False

    for method in methods:
        if method in name: return True
    
    return False