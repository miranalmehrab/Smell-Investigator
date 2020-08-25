from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file 

def save_individual_projects_smells():
    project_smells = []
    
    smells = list_csv_contents('logs/projectSmells.csv')

    for smell in smells:
        smell_matched = False
        
        for project_smell in project_smells:
            if smell[0] in project_smell:

                project_smell[1] = int(project_smell[1]) + int(smell[2]) 
                smell_matched = True
                break

        if smell_matched is False:
            project_smells.append([smell[0], int(smell[2])])

    project_smells.sort(key = lambda x: x[1], reverse = True)
    
    for project_smell in project_smells:
        write_to_csv_file('logs/projectGist.csv', project_smell)
