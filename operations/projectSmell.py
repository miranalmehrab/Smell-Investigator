import csv
from operations.write_to_csv_file import write_to_csv_file

def csvFileContents(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader: rows.append(row)

    return rows


def write_smells(smells):

    project_name = None
    for smell in smells:
        
        if project_name is None:
            project_name = smell[0]
            write_to_csv_file('logs/projectSmells.csv', smell)

        elif project_name is not None and project_name != smell[0]:    
            project_name = smell[0]
            write_to_csv_file('logs/projectSmells.csv', smell)
                
        else: 
            write_to_csv_file('logs/projectSmells.csv', smell)


def save_project_smells():
    smells = csvFileContents('logs/detected_smells.csv')
    projectSmells = []
    
    for smell in smells:
        smell = [smell[0], smell[2]]
        
        found = False
        for project in projectSmells:
            
            if smell[0] in project and smell[1] in project:
                project[2] = project[2]+1
                found = True
                break   

        if found is False:
            projectSmells.append([smell[0],smell[1],1])

    projectSmells.sort(key = lambda x: x[0])
    
    counter = 0
    for x in projectSmells: 
        counter += int(x[2])
        # print(x)

    # print(len(projectSmells))
    # print('total smell count '+str(counter))
    write_smells(projectSmells)
    
    