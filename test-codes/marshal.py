import marshal

data = {'twelve', 'feep'} 

bytesData = marshal.dumps(data) 
readdata = marshal.loads(bytesData)
