import csv

def saveParsingExceptions(error,filename):

    with open('logs/parsingExceptions.csv', 'a') as fp: 
        name = filename.name
        name = name.split('/')[-1]
   
        fw = csv.writer(fp)
        if error and filename: fw.writerow([name,error])