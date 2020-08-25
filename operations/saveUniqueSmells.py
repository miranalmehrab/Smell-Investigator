import csv

def saveUniqueSmells(smell):

    with open('logs/uniqueSmells.csv', 'a') as fp: 
        
        fw = csv.writer(fp)
        fw.writerow(smell)