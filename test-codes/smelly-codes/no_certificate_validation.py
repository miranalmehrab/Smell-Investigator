# session = requests.Session()
# session.verify = False

# request.get('https://wrong.host.badssl.com/', verify = False)

r = request(url)
r = request(request(url))
r = request(url, verify = False)
r = requests.get(url, verify = False).json()
r = request.get('192.168.1.10', verify = False)

# req = requests.get(req.url if req.url else req.url(), verify=False)