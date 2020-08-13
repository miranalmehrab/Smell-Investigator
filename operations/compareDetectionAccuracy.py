import csv

def csvFileContents(filename):
    
    rows = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader: rows.append(row)

    return rows

def compareDetectionAccuracy():
    
    reference_rows = csvFileContents('smells.csv')
    detected_rows = csvFileContents('detected_smells.csv')

    