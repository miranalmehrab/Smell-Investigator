import csv

def saveAsCSV(filename,smell):
    with open('smells.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([filename, smell])