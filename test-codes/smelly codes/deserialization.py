import pickle

mylist = ['a', 'b', 'c', 'd']
with open('datafile.txt', 'wb') as fh:
   		pickle.dump(mylist, fh)

pickle_off = open ("datafile.txt", "rb")
emp = pickle.load(pickle_off)
pickle.load(pickle_off)

def getFile():
    pickle_off = open ("datafile.txt", "rb")
    return pickle.load(pickle_off)
