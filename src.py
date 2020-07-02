import os,stat
# file_name = input()
# exec('sudo mkdir {file_name}')

os.chmod('/etc/hosts',0x777)
os.chmod('/etc/hosts',stat.S_IRWXO)
os.chmod('/etc/hosts',stat.S_IROTH)
os.chmod('/etc/hosts',stat.S_IWOTH)
os.chmod('/etc/hosts',stat.S_IXOTH)

# DEBUG_PROPAGATE_EXCEPTIONS = True
# app.run(debug = True,start = True)
password = "pass"
password = ''
password = None
name = "root"
pwd = "root123"
# query = "delete from foo where id = " + user_input + user_input
# x = "abc"
# user_input = input()
# result = connection.execute(user_input)
# sys.argv('sudo mkdir {user_input}')

# if username == "root" and password == "123":
#     logIn()
