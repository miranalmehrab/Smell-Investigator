import csv

def csvFileContents(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader: rows.append(row)

    return rows

def printResultsAndErrors(detected_smells,reference_smells,parsing_errors,token_errors):
    print('------------------------------ Result ------------------------------ ')
    
    print('')
    print('detected number of smells: '+ str(len(detected_smells)))
    print('total number of smells: '+ str(len(reference_smells)))
    
    print('')
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

        if found == False:uniqueCounts.append([smell[1], 0])

    print('')
    print('---------------------- '+header+' --------------------')
    for count in uniqueCounts:
        print(count)



def compareDetectionAccuracy():
    reference_smells = csvFileContents('test-codes/smells.csv')
    smellOccurenceCount(reference_smells, 'reference smells')