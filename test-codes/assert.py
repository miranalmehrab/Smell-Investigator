def getHello():
    return "hello"

z = getHello()

assert x == "goodbye", "x should be 'hello'"
assert x == y
assert y == getHello()

assert getHello() == x

assert isinstance(x, int), 'x should be int'