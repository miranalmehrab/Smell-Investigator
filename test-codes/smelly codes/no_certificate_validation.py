session = requests.Session()
session.verify = False

request.get('192.168.1.10', verify = False)
request.get('https://wrong.host.badssl.com/', verify = False)
