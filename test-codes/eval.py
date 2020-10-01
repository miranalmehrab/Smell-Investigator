# def func():
#     expr = input("Enter the function(in terms of x):") 
#     x = int(input("Enter the value of x:")) 

#     return eval(expr)    

# expr = input("Enter the function(in terms of x):") 

# x = int(input("Enter the value of x:")) 

# eval(expr)
# exec(expr)		
# y = eval(expr)

expr = input("Enter the function(in terms of x):") 

sys.argv(expr)

s = sys.argv(expr)

def func():
    return sys.argv(expr)
