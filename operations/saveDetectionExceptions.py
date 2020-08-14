import csv

def saveDetectionExceptions(error,filename):

    with open('logs/detectionExceptions.csv', 'a') as fp:
        name = filename.name
        name = name.split('/')[-1]
    
        fw = csv.writer(fp)
        if error and filename: fw.writerow([name,error])