import csv

def clearCSV():
    with open('smells.csv', 'w+') as csvfile:
        csvfile.close()