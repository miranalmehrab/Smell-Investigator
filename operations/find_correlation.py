from scipy.stats import pearsonr

from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file

def find_correlation():
    project_smells = list_csv_contents('logs/projects/total_smells_in_project.csv')
    project_descriptions = list_csv_contents('project-descriptions.csv')
    
    relations = []

    for project in project_smells:
        for description in project_descriptions:
            if project[0] == description[0]:
                relations.append([project[0], int(project[1]), description[0], int(description[4])])
                break

    for i in range(1,len(project_descriptions)):
        already_included = False
        
        for relation in relations:
            if relation[0] == project_descriptions[i][0]:
                already_included = True
                break

        if already_included == False:
            print([project_descriptions[i], 0, project_descriptions[i], project_descriptions[i][4]])
            relations.append([project_descriptions[i][0], 0, project_descriptions[i][0], int(project_descriptions[i][3])])
            

    relations.sort(key = lambda x: x[1])
    x = []
    y = []

    for relation in relations:
        x.append(relation[1])
        y.append(relation[3])

        print(relation)
        write_to_csv_file('logs/relations/x.csv', [relation[1]])
        write_to_csv_file('logs/relations/y.csv', [relation[3]])
        write_to_csv_file('logs/relations/x-y.csv', [relation[1], relation[3]])

    correlation, _ = pearsonr(x, y)
    print('Pearsons correlation: %.4f' % correlation)
