from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file


def save_total_count_of_detected_smells_in_projects():
    project_smells = []
    smells = list_csv_contents('logs/projects/different_smells_in_project.csv')

    for smell in smells:
        already_included = False
        
        for project_smell in project_smells:
            if smell[0] in project_smell:

                project_smell[1] = int(project_smell[1]) + int(smell[2]) 
                already_included = True
                break

        if already_included is False:
            project_smells.append([smell[0], int(smell[2])])

    
    # for i in range(len(project_smells)):
    #     project_smells[i][0] = project_smells[i][0].replace('-master', '')

    # descriptions = list_csv_contents('projects.csv')
    # descriptions.pop(0)

    # for description in descriptions:
    #     already_included = False
        
    #     for project_smell in project_smells:
    #         if description[0] in project_smell:
    #             already_included = True
    #             break
        
    #     if already_included is False:
    #         project_smells.append([description[0], 0])

    project_smells.sort(key = lambda x: x[0][0]) #sorting the smells according to alphabetical name
    
    # for project in project_smells:
    #     print(project)
    print(len(project_smells))
    # print(len(descriptions))
    
    for project_smell in project_smells:
        write_to_csv_file('logs/projects/total_smells_in_project.csv', project_smell)
        write_to_csv_file('logs/projects/project_names.csv', [project_smell[0]])
        write_to_csv_file('logs/projects/project_smells_count.csv', [project_smell[1]])


def save_smells_categorized_according_to_project_type():
    descriptions = list_csv_contents('./../projects5.csv')
    projects = list_csv_contents('logs/projects/different_smells_in_project.csv')
    categorized_smell_in_projects = []

    # for i in range(len(projects)):
    #     projects[i][0] = projects[i][0].replace('-master', '')


    for project in projects:
        name = project[0]
        name_found = False
        
        smell = project[1]
        smell_count = project[2]
        project_type = None

        for description in descriptions:
            if name == description[0]:
                project_type = description[2]
                break

        for category in categorized_smell_in_projects:
            if category[0] == project_type and category[1] == smell:
                category[2] += int(smell_count)
                name_found = True
                break


        if name_found is False and project_type is not None:
            categorized_smell_in_projects.append([project_type, smell, int(smell_count)])

    categorized_smell_in_projects.sort(key = lambda x: x[0])

    total_smell_count = []

    for category in categorized_smell_in_projects:
        already_included = False
        
        for smell in total_smell_count:
            if smell[0] == category[0]:
                smell[1] += int(category[2])
                
                already_included = True
                break
        
        if already_included is False:
            total_smell_count.append([category[0], int(category[2])])
            
    for smell in total_smell_count:
        write_to_csv_file('logs/relations/x.csv', [smell[0]])
        write_to_csv_file('logs/relations/y.csv', [smell[1]])
        write_to_csv_file('logs/relations/x-y.csv', [smell[0], smell[1]])

        print(smell)


def save_unique_smell_count_in_project():
    projects = []
    smells = list_csv_contents('logs/projects/different_smells_in_project.csv')

    for smell in smells:
        project_found = False
        for project in projects:
            
            if smell[0] in project:
                project[1] += 1
                project_found = True
            
            if project_found is True: 
                break
            
        if project_found is False:
            projects.append([smell[0], 1])

    projects.sort(key = lambda x: x[0][0])
    
    for project in projects:
        write_to_csv_file('logs/projects/project_unique_smell_counts.csv', project)
        write_to_csv_file('logs/projects/x.csv', [project[0]])
        write_to_csv_file('logs/projects/y.csv', [project[1]])


def save_detected_different_smells_frequency_in_projects():
    project_smells = []
    smells = list_csv_contents('logs/smells/detected_smells.csv')
    
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
      write_to_csv_file('logs/projects/different_smells_in_project.csv', project_smell)