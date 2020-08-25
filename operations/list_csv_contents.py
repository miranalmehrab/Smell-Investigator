import csv

def list_csv_contents(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader: 
            rows.append(row)

    return rows