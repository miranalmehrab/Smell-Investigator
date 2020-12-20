from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, src_file):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): token_type = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]

        insecure_methods = ['execution.query', 'connection.cursor.execute', 'sqlite3.connect.execute',
                        'psycopg2.connect.cursor.execute','mysql.connector.connect.cursor.execute', 
                        'pyodbc.connect.cursor.execute', 'sqlalchemy.sql.text', 'sqlalchemy.text',
                        'text', 'records.Database.query'
                    ]
        
        if token_type == "variable" and token.__contains__('valueSrc') and token.__contains__('args'):
            
            valueSrc = token['valueSrc']
            if(valueSrc in insecure_methods or query_methods_has_patterns(valueSrc)): # and token['isInput'] is True:
                action_upon_detection(project_name, src_file, lineno, 'constructing sql statement upon user input', 'constructing sql statement upon user input', token)
                    
        elif token_type == "function_call" and token.__contains__('name') and token.__contains__('args'):#token['hasInputs'] is True:
            if (name in insecure_methods or query_methods_has_patterns(name)) and len(token['args']) > 0:  
                action_upon_detection(project_name, src_file, lineno, 'constructing sql statement upon user input', 'constructing sql statement upon user input', token)
        
        elif token_type == "function_def" and token.__contains__('return') and token["return"] is not None:
            for func_return in token['return']:
                if (func_return in insecure_methods or query_methods_has_patterns(func_return)):
                    action_upon_detection(project_name, src_file, lineno, 'constructing sql statement upon user input', 'constructing sql statement upon user input', token)

    except Exception as error: save_token_detection_exception('constructing sql statement upon user input detection  '+str(error)+'  '+ str(token), src_file)

def query_methods_has_patterns(name):
    methods = ['execution.query', 'connection.cursor.execute', 'sqlite3.connect.execute','psycopg2.connect.cursor.execute', 'objects.raw',
                'mysql.connector.connect.cursor.execute', 'pyodbc.connect.cursor.execute', 'sqlalchemy.sql.text', 'objects.extra'
            ]

    if isinstance(name, str) is False: return False
    elif len(name) == 0: return False

    for method in methods:
        if method in name: return True
    
    return False