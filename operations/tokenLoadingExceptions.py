import csv

def tokenLoadingExceptions(token,filename):

    with open('logs/tokenLoadingExceptions.csv', 'a') as fp:
        name = filename.name
        name = name.split('/')[-1]
    
        fw = csv.writer(fp)
        if token and filename: fw.writerow([name,token])