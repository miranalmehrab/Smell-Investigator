s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind('', 4000)
s.bind('0.0.0.0', 3134)
s.bind('8.8.8.8', 8000)
