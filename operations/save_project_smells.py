from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file

def save_total_count_of_detected_smells_in_projects():
    project_smells = []
    smells = list_csv_contents('logs/different_smells_in_project.csv')

    for smell in smells:
        smell_matched = False
        
        for project_smell in project_smells:
            if smell[0] in project_smell:

                project_smell[1] = int(project_smell[1]) + int(smell[2]) 
                smell_matched = True
                break

        if smell_matched is False:
            project_smells.append([smell[0], int(smell[2])])

    project_smells.sort(key = lambda x: x[1], reverse = True) #sorting the smells according to frequency
    for project_smell in project_smells:
        write_to_csv_file('logs/total_smells_in_project.csv', project_smell)


def save_detected_different_smells_frequency_in_projects():
    project_smells = []
    smells = list_csv_contents('logs/detected_smells.csv')
    
    for smell in smells:
        smell = [smell[0], smell[2]]
        match_found = False

        for project_smell in project_smells:
            if smell[0] in project_smell and smell[1] in project_smell:
                
                project_smell[2] = project_smell[2]+1
                match_found = True
                break   

        if match_found is False:
            project_smells.append([smell[0],smell[1],1])

    project_smells.sort(key = lambda x: x[0]) #sorting the smells according to project names
    for project_smell in project_smells:
      write_to_csv_file('logs/different_smells_in_project.csv', project_smell)