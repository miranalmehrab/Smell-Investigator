# import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('0.0.0.0', 31137))
# s.bind(('192.168.0.1', 8080))

# r = s.bind(('192.168.0.1', 8080))


def getSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s.bind(('0.0.0.0', 31137))
     

# get_db(s.bind(('192.168.0.1', 8080)))

# def getX():
#     x = 20
#     return x

# def getNothing():
#     return {'name': 'admin', 'password': 'pass'}
#     return ['admin', 'kagdfv', 'asdggadf']

# def getFullName(firstName, lastName):
#     return firstName+lastName

# def getUserName(id, name = "user",pwd = "xyz123"):
#     return name+id

# def my_function(*kids):
#     pass

# def my_function(**kid):
#     pass

# getX()
# getNothing()
# getFullName('Miran', 'Al Mehrab')
# getUserName(pwd = '', name = 'user root', id =  '1x2y4s5t')

# socket.socket(AF.NET, IO.STREAM)

# my_function(['apple','mango'])