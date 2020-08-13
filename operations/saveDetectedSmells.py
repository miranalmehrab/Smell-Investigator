import csv

def saveDetectedSmells(smell,filename):

    with open('detected_smells.csv', 'a') as fp:    
        fw = csv.writer(fp)
        if smell and filename: fw.writerow([smell, filename])