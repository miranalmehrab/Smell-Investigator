from __future__ import unicode_literals
from csvkit import CSVKitWriter
from calaccess_raw import models
from django.db import connection
from calaccess_raw.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    help = 'Dump all of the unique campaign contributor names'

    def handle(self, *args, **options):
        self.cursor = connection.cursor()
        sql = """
        SELECT
            title,
            first_name,
            last_name,
            suffix,
            occupation,
            employer,
            address1,
            address2,
            city,
            state,
            zipcode,
            committee_id,
            COUNT(*)
        FROM (
            SELECT
                ctrib_namt as title,
                ctrib_namf as first_name,
                ctrib_naml as last_name,
                ctrib_nams as suffix,
                ctrib_occ as occupation,
                ctrib_emp as employer,
                ctrib_adr1 as address1,
                ctrib_adr2 as address2,
                ctrib_city as city,
                ctrib_st as state,
                ctrib_zip4 as zipcode,
                cmte_id as committee_id
            FROM %(rcpt)s

            UNION ALL

            SELECT
                lndr_namt as title,
                lndr_namf as first_name,
                lndr_naml as last_name,
                lndr_nams as suffix,
                loan_occ as occupation,
                loan_emp as employer,
                loan_adr1 as address1,
                loan_adr2 as address2,
                loan_city as city,
                loan_st as state,
                loan_zip4 as zipcode,
                cmte_id as committee_id
            FROM %(loan)s

            UNION ALL

            SELECT
                enty_namt as title,
                enty_namf as first_name,
                enty_naml as last_name,
                enty_nams as suffix,
                ctrib_occ as occupation,
                ctrib_emp as employer,
                '' as address1,
                '' as address2,
                enty_city as city,
                enty_st as state,
                enty_zip4 as zipcode,
                cmte_id as committee_id
            FROM %(s497)s
        ) as t
        GROUP BY
            title,
            first_name,
            last_name,
            suffix,
            occupation,
            employer,
            address1,
            address2,
            city,
            state,
            zipcode,
            committee_id
        ORDER BY
            last_name,
            first_name,
            suffix,
            title,
            city,
            state,
            occupation,
            employer
        """ % dict(
            rcpt=models.RcptCd._meta.db_table,
            loan=models.LoanCd._meta.db_table,
            s497=models.S497Cd._meta.db_table,
        )
        self.cursor.execute(sql)
        writer = CSVKitWriter(open("./contributors.csv", 'wb'))
        writer.writerow([
            'title',
            'first_name',
            'last_name',
            'suffix',
            'occupation',
            'employer',
            'address1',
            'address2',
            'city',
            'state',
            'zipcode',
            'committee_id',
            'count'
        ])
        writer.writerows(self.cursor.fetchall())




# grant_access(get_name( get_pwd(pwd = 'ij123xyz')))
# self.do_something(requests.get('http://www.malicious.com/files?file=virus.exe'))

# SECRET_KEY = 'e^h9#%6uqkyy8ef8&6mzc@&v9n!25(h#%d59ossolktzt_om4@'
# self.user = User.objects.create_user('foo', password = 'pass')
# self.admin = 'admin'
# twitter_social_app = SocialApp.objects.create( provider='twitter', name='Twitter', client_id='11223344', secret='55667788')


# username = 'admin'
# EMAIL_HOST_USER = "18500611672@sinacn"
# EMAIL_HOST_PASSWORD = "zz1123581321"
# SECRET_KEY = 'qzk7a803m2d6_ngccq$jh&8#90m!19qfr^s39#ay6#_*ri5ap+'
# MAIL_PASSWORD = 'password'
# admin = 'admin'
# pylint_token = "R0902"
# password='pbkdf2_sha256$36000$HizLkJV9vzk4$++1pBxJlH/uqIn5Qx0jugTH1b3U5SyZTaqnm+kSk7pQ='


# from sqlalchemy import text

# t = text("SELECT * FROM users")
# result = connection.execute(t)

# db = records.Database('postgres://...')
# rows = db.query('select * from active_users')


# admin = 'root'
# username = 'root'
# pwd = forms.root

# net.latents_var = T.TensorType('float32', [False] * len(net.example_latents.shape))('latents_var')

# parser = argparse.ArgumentParser(prog='myprogram')
# parser.add_argument('--foo', help='foo of the %(prog)s program')
# parser.print_help()

# app = Flask(__name__)

# DEBUG = True
# app.debug = True
# app.run(debug = True)

# app.config['PROPAGATE_EXCEPTIONS'] = True

# debug = True

# name_ver = 'name_ver'
# info_dir = '%s.dist-info' % name_ver

# url = 'https://www.malicious.com/virus.exe'
# requests.get(url)

# url = 'https://www.malicious.com/files?file=virus.exe'
# requests.get(url)

# url = 'https://www.malicious.com/files?virus.exe'
# requests.get(url)


# url = 'http://localhost:8000'
# requests.get(url)

# import hashlib

# try: result = 'abcedf'
# except: pass

# username = 'admin'
# password = 'admin'
# pass1 = ahc.gsdf.sjagdshj()
# pass1 = password

# name = str(input('wassup man? got a name?_'))

# tokens = {'user': 'root', 'pwd': '1h23ighwdvssedw23'}
# def grant_access(username = 'guest', password = 'guest'):
#    pass

# if username == 'admin' and password == 'admin':
#     grant_access(username, password)


# ip = '0.0.0.0'
# port = '3030'

# s = socket.socket(AF.NET,IO.SOCKET)
# s.bind('0.0.0.0','3030')

# s.bind(ip,port)


# passwords = ['abc123', 'xyz321']
# myDict = {'password' : '12234', 'token' : '12i1gjhwbejsqdguayg2367t276', 'debug': True}
# username = {"apple", "banana", "cherry"}

# import os
# import socket 
# from math import pi,sqrt,fabs
# from os import *
# import hashlib

# file_name = input()
# exec(file_name)
# import marshal
# marshal_dump = marshal.dump

# os.chmod('/etc/hosts',0x777)
# os.chmod('/etc/hosts',stat.S_IRWXO)
# os.chmod('/etc/hosts',stat.S_IROTH)
# os.chmod('/etc/hosts',stat.S_IWOTH)
# os.chmod('/etc/hosts',stat.S_IXOTH)

# DEBUG_PROPAGATE_EXCEPTIONS = True
# app.run(debug = True, start = True)

# session = requests.Session()
# session.verify = False
# session.get('https://wrong.host.badssl.com/', verify = False)

# m = urllib.urlretrieve("192.168.10.1/example.iso")

# user_input = 'abcdef'
# user_input = input()
# query = "delete from foo where id = " + user_input + user_input
# x = "abc"

# process = input()
# pre = 'kil - {}'.format(process)

# process = 'abcdef'

# subprocess.Popen('kil - {}'.format(process))
# subprocess.Popen("A list: %s, %s" % process % pre)
# subprocess.Popen('In the basket are %s and %s' % (comm,pre))


# execution.query(user_input)
# result = connection.execute(user_input)
# sys.argv(f'sudo mkdir {user_input}')



# x = 1
# query = 2
# ask = y = query + x
# ask = 'a' + 'b' + 'c' + 'd' + 'e' + x + x + x 
# s = socket.socket(AF.NET,IO.SOCKET)
# s.bind('0.0.0.0',3000)
# token = "abcdea"
# header[authorization] = "bearer:"+token
# header[0] = token

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
# r = sys.argv(f'sudo mkdir {user_input}')

# ip = '192.168.0.10'
# port = 2000

# def getPort(ip,port,socket = ['socket','port']):
#     return ip+port

# getPort(ip, '12213kjhg')

# def getIp(ip = 3000, port = getPort()):
#     return getPort(ip,port,'12'+'00',12+23,socket(12),sock.socket(12))

# r = requests.get("http://abc.com")
# requests.get("http://abc.com")
# requests.get("www.abc.com")

# socket.socket(socket.AF_INET, socket.SOCK_STREAM).bind(getIp(),getPort(),'123'+'4')


# if username == "root" and password == "":
#     logIn()

# if 1 == username:
#     print('1 is equal to 1')
# if username == 1:
#     print('1 is equal to 1')

# hardcoded_tmp_directory = ['/tmp','/var/tmp','/var/usr/tmp', 12+12]

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
# except: pass

# doSomething() 
