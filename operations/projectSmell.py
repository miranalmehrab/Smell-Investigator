import csv

def csvFileContents(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader: rows.append(row)

    return rows


def write_smells(smells):
    with open('logs/projectSmells.csv', 'w') as fp:    
        fw = csv.writer(fp)
        for smell in smells:
            fw.writerow(smells)

def save_project_smells(project_name):
    smells = csvFileContents('detected_smells.csv')
    projectSmells = []
    
    for smell in smells:
        splited_smell = smell.split(',')
        smell = [splited_smell[0], splited_smell[2]]

        found = False
        for project in projectSmells:
            
            if smell[0] in project:
                smell[1] = smell[1]+1
                found = True
                break   

        if found is False:
            projectSmells.append([smell[0],smell[1],0])

    projectSmells.sort(key = lambda x: x[0])
    write_smells(projectSmells)
    
    