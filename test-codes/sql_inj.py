query = input('')
query = 'select * from table = '+query

sqlite3.connect.execute(query)

r = psycopg2.connect.cursor.execute(query)

def func():
    return mysql.connector.connect.cursor.execute(query)

r = pyodbc.connect.cursor.execute(query)