username = "root"
password = "root"
x = 20

def getX():
    return 20

if 1 == getX()+2+ getX():
    print(1)

if getX()==1:
    print(1)


if True and True:
    print(True)

if getX():
    print(x)

if x:
    print(x)

if x == getX():
    print(x)

if x != 20:
    print(x)

if x >= 20:
    print(x)

if x <= 20:
    print(x)

if x > 20:
    print(x)

if x < 20:
    print(x)

if username == "root" and password == "root":
    logIn()

if username == "root" or password == "root":
    logIn()

if username:
    logIn()

if username and password:
    logIn()

if username or password:
    logIn()

if username is not password:
    print(password)

names = ['root', 'root1']
if username in names:
    print(username)