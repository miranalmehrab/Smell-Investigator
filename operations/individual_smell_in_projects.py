from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file

def individual_smell_in_projects():
    unique_projects_count = []
    smells_in_projects = list_csv_contents('logs/different_smells_in_project.csv')
    
    for smells_in_project in smells_in_projects:
        already_in = False

        for project in unique_projects_count:
            if project[0] == smells_in_project[1]: 
                already_in = True
                project[1] += 1

        if already_in == False: 
            unique_projects_count.append([smells_in_project[1],1])
    
    for project in unique_projects_count:
        write_to_csv_file('logs/project_counts.csv',project)
