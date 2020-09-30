r = requests.get("http://abc.com", verify = False)
requests.get("http://abc.com", verify = False)

# s = socket.socket(AF.NET, IO.STREAM)
# s.bind((ip, 4000))

session = requests.Session()
session.verify = False

def func():
    return requests.get("http://abc.com", verify = False)