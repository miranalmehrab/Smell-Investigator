# ip = '127.0.0.1'

s = socket.socket(AF.NET, IO.STREAM)
s.bind((ip, 4000))
s.bind('', '')

self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self.sock.connect(('127.0.0.1', 4000))

