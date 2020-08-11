x = "hello"
y = x

def getHello():
    return "hello"

z = getHello()

assert x == "hell"+"o"
assert x == "goodbye", "x should be 'hello'"
assert x == y
assert y == getHello()

assert getHello() == x