import csv

def csvFileContents(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader: rows.append(row)

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
            
            if smell[1] in row:
                row[1] = row[1]+1
                found = True
                break   

        if found is False:
            uniqueCounts.append([smell[1], 0])

    print('')
    print('---------------------- '+header+' --------------------')
    uniqueCounts.sort(key = lambda x: x[1], reverse = True)
    for smell_count in uniqueCounts:
        print(smell_count)


def show_results():
    detected_smells = csvFileContents('detected_smells.csv')
    parsing_errors = csvFileContents('logs/parsingExceptions.csv')
    token_errors = csvFileContents('logs/tokenLoadingExceptions.csv')
    
    printResultsAndErrors(detected_smells,parsing_errors,token_errors)
    smellOccurenceCount(detected_smells, 'detected smells')