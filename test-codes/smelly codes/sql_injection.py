from sqlalchemy import text

t = text("SELECT * FROM users")
result = connection.execute(t)

db = records.Database('postgres://...')
rows = db.query('select * from active_users')

sqlite3.connect.execute(query)

r = psycopg2.connect.cursor.execute(query)

def func():
    return mysql.connector.connect.cursor.execute(query)

r = pyodbc.connect.cursor.execute(query)