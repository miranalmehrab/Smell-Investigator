import csv
from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file 

def csvFileContents(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader: 
            rows.append(row)

    return rows

def printResultsAndErrors(detected_smells,parsing_errors,token_errors):
    print('')
    print('------------------------------ Result ------------------------------ ')
    print('detected number of smells: '+ str(len(detected_smells)))
    print('number of parsing errors: '+ str(len(parsing_errors)))
    print('number of token loading errors: '+ str(len(token_errors)))
    
def smellOccurenceCount(smells, header):
    uniqueCounts = []
    for smell in smells:
        found = False

        for row in uniqueCounts:
            if smell[2] in row:
                row[1] = row[1]+1
                found = True
                break   

        if found is False:
            uniqueCounts.append([smell[2], 0])

    print('')
    print('---------------------- '+header+' --------------------')
    
    uniqueCounts.sort(key = lambda x: x[1], reverse = True)
    for smell_count in uniqueCounts:
        write_to_csv_file('logs/uniqueSmells.csv',smell_count)    


def show_results():
    detected_smells = list_csv_contents('logs/detected_smells.csv')
    parsing_errors = list_csv_contents('logs/parsingExceptions.csv')
    token_errors = list_csv_contents('logs/tokenLoadingExceptions.csv')
    
    printResultsAndErrors(detected_smells,parsing_errors,token_errors)
    smellOccurenceCount(detected_smells, 'detected smells')