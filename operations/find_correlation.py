from scipy.stats import pearsonr

from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file

def find_correlation():
    project_smells = list_csv_contents('logs/projects/total_smell_counts_in_projects.csv')
    project_descriptions = list_csv_contents('project-descriptions.csv')
    
    relations = []

    for project in project_smells:
        for description in project_descriptions:
            if project[0] == description[0]:
                relations.append([project[0], int(project[1]), description[0], int(description[4])])
                break
    
    relations.sort(key = lambda x: x[3]) #sorting according to smell count #ascending
    
    x = []
    y = []

    for relation in relations:
        x.append(relation[1])
        y.append(int(relation[3]))

        print(relation)
        write_to_csv_file('logs/relations/x.csv', [relation[3]])
        write_to_csv_file('logs/relations/y.csv', [relation[1]])
        write_to_csv_file('logs/relations/x-y.csv', [relation[1], relation[3]])

    # print(relations)
    # print(x)
    # print(y)

    correlation, _ = pearsonr(x, y)
    print('Pearsons correlation: %.4f' % correlation)
