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
        project_name = None
        for smell in smells:
            
            if project_name is None:
                project_name = smell[0]
                fw.writerow(smell)

            elif project_name is not None:
                if project_name != smell[0]:
                    
                    project_name = smell[0]
                    fw.writerow([])
                    fw.writerow([])    
                    fw.writerow(smell)
                    
                else: fw.writerow(smell)

def save_project_smells():
    smells = csvFileContents('detected_smells.csv')
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
    
    