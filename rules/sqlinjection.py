from operations.action_upon_detection import action_upon_detection
from operations.save_token_exceptions import save_token_detection_exception

def detect(token, project_name, srcFile):
    try:
        if token.__contains__("line"): lineno = token["line"]
        if token.__contains__("type"): tokenType = token["type"]
        if token.__contains__("name"): name = token["name"]
        if token.__contains__("args"): args = token["args"]
        if token.__contains__("hasInputs"): hasInputs = token["hasInputs"]

        queryMethods = ['execution.query', 'connection.cursor.execute', 'sqlite3.connect.execute',
                        'psycopg2.connect.cursor.execute','mysql.connector.connect.cursor.execute', 
                        'pyodbc.connect.cursor.execute']
        
        if tokenType == "variable" and token.__contains__('valueSrc') and token.__contains__('args'):
            
            args = token['args']
            valueSrc = token['valueSrc']
            if valueSrc in queryMethods and token['isInput'] == True:
                action_upon_detection(project_name, srcFile, lineno, 'constructing sql statement upon user input', 'constructing sql statement upon user input', token)
                    
        elif tokenType == "function_call" and name in queryMethods and token['hasInputs'] == True:
            action_upon_detection(project_name, srcFile, lineno, 'constructing sql statement upon user input', 'constructing sql statement upon user input', token)
        
        elif tokenType == "function_def" and token.__contains__('return') and token.__contains__('returnHasInputs'): 
            if token['return'] in queryMethods and token['returnHasInputs'] == True:
                action_upon_detection(project_name, srcFile, lineno, 'constructing sql statement upon user input', 'constructing sql statement upon user input', token)
        

    except Exception as error: save_token_detection_exception('constructing sql statement upon user input detection  '+str(error)+'  '+ str(token), srcFile)