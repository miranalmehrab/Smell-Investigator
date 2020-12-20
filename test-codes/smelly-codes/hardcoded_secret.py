def grant_access(username = 'guest', password = 'guest'):
   pass

cert = get_cert(username = 'root')

if username == 'admin' and password == 'admin':
    grant_access(username = 'root', password = 'root')

username = 'admin'
password = 'admin'

pwds = ['admin', 'root']

tokens = {'user': 'root', 'pwd': '1h23ighwdvssedw23'}