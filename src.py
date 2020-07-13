# x = 1
# query = 2
# ask = y = query + x
# ask = 'a' + 'b' + 'c' + 'd' + 'e' + x + x + x 
# m = s = socket.socket(ip,port)

# import os
# import socket 
# from math import pi,sqrt,fabs
# from os import *
# file_name = input()
# exec('sudo mkdir {file_name}')

# os.chmod('/etc/hosts',0x777)
# os.chmod('/etc/hosts',stat.S_IRWXO)
# os.chmod('/etc/hosts',stat.S_IROTH)
# os.chmod('/etc/hosts',stat.S_IWOTH)
# os.chmod('/etc/hosts',stat.S_IXOTH)

# DEBUG_PROPAGATE_EXCEPTIONS = True
# app.run(debug = True,start = True)
# password = "pass"
# password = ''
# pwd = ''
# password = None
# name = "root"
# pwd = "root123"
# query = "delete from foo where id = " + user_input + user_input
# x = "abc"
# urllib.urlretrieve("192.168.10.1/example.iso")

# user_input = input()
# execution.query(user_input)
# subprocess.Popen(user_input)
# result = connection.execute(user_input)
# sys.argv('sudo mkdir {user_input}')

# def getPort(ip,port,socket = ['socket','port']):
#     return 3000+32

# def getIp(ip = 3000, port = getPort()):
#     return getPort(ip,port,'12'+'00',12+23,socket(12),sock.socket(12))


# socket.socket(socket.AF_INET, socket.SOCK_STREAM).bind(getIp(),getPort(),'123'+'4')


# if username == "root" and password == "":
#     logIn()

# if 1 == username:
#     print('1 is equal to 1')
# if username == 1:
#     print('1 is equal to 1')

# hardcoded_tmp_directory = ['/tmp','/var/tmp','/var/usr/tmp', 12+12]
# requests.get("http://abc.com")

# connection.execute("hello")
# connection.execute(user_input)

# port = '3000'
# ip = '0.0.0.0'


# s = socket(ip,port)
# s = socket(2000, 1223)
# m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind('0.0.0.0','3000')
# m.bind(ip,port)

# try: x = 2
# except:
#     doSomething() 
#     pass

# """ This is a convenient way to monkeypatch a method or attribute of a Python
#     object. This is great for situations where you want to modify a global
#     object within a limited scope, i.e., your typical class or module when
#     testing. This was tested and works with Python 2.7 and 3.4. """

# import contextlib

# @contextlib.contextmanager
# def monkeypatched(object, name, patch):
#     """ Temporarily monkeypatches an object. """

#     pre_patched_value = getattr(object, name)
#     setattr(object, name, patch)
#     yield object
#     setattr(object, name, pre_patched_value)

# if __name__ == '__main__':

#     class Foo:
#         bar = False

#     with monkeypatched(Foo, 'bar', True):
#         assert Foo.bar

#     assert not Foo.bar
    
# plot weight of oit

# import matplotlib.pyplot as plt
# import numpy as np

# N = 1000
# z = np.linspace(1, 500, N)


# def clamp(a, amin, amax):
#     return np.max([amin, np.min([a, amax])])


# def equation7(z):
#     zabs = np.abs(z)
#     val = 10. / (1e-5 + np.power(zabs/5.0, 2.0) + np.power(zabs/200.0, 6.0))
#     return clamp(val, 1e-2, 3e3)


# def equation8(z):
#     zabs = np.abs(z)
#     val = 10. / (1e-5 + np.power(zabs/5.0, 3.0) + np.power(zabs/200.0, 6.0))
#     return clamp(val, 1e-2, 3e3)


# def equation9(z):
#     val = 0.001/(1e-5 + np.power(np.abs(z)/200.0, 4.0))
#     return clamp(val, 1e-2, 3e3)


# zw = np.array([[equation7(zi), equation8(zi), equation9(zi)] for zi in z])

# plt.loglog(zw)
# plt.xlim([1, 1000])

