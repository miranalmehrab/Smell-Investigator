import csv

def saveDetectedSmells(smell,filename):

    with open('detected_smells.csv', 'a') as fp:    
        name = filename.name
        name = name.split('/')[-1]

        fw = csv.writer(fp)
        if smell and filename: fw.writerow([name,smell])