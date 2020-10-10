import os
from .write_to_csv_file import write_to_csv_file
from .list_csv_contents import list_csv_contents

def clear_file_contents(output_file_path):
    fp = open(output_file_path, 'w+')
    fp.close()


def list_smells_in_projects_sequentially():

    contents = list_csv_contents('./../bandits_results.csv')   
    project_smells = []
    
    output_file_path = './../bandits_total_results.csv'
    clear_file_contents(output_file_path)
    
    for content in contents:
        should_skip = False
        for name_part in content[0].split('/'):
            if name_part.find('test') != -1:
                should_skip = True
                break

        if should_skip is False:        
            name = content[0].split('/')[3]
            already_included = False

            for smell in project_smells:
                if name in smell and content[3] in smell:
                    already_included = True
                    smell[2] = int(smell[2]) + 1
                    break

            if already_included is False:
                project_smells.append([name, content[3], 1])
    
    total_smell_count = 0
    for smell in project_smells:
        print(smell)
        total_smell_count += int(smell[2])
        write_to_csv_file(output_file_path, smell)

    print('total smell counts %s' %total_smell_count)




def match_project_name_and_description_name(project_smells, project_descriptions):
    desc_names = []
    smell_names = []

    for smell in project_smells:
        smell_names.append([smell[0], 0])

    for description in project_descriptions:
        desc_names.append(description[0])
 
    for smell in smell_names:
        if smell[0] in desc_names:
            smell[1] = True

    unmatched_projects_count = 0
    for smell in smell_names:
        if smell[1] is False:
            
            print(smell[0])
            unmatched_projects_count += 1

    print('unmatched projects count %s' %unmatched_projects_count)
    

def match_project_categories_from_bandit_results():
    project_descriptions = list_csv_contents('./project-descriptions.csv')
    project_smells = list_csv_contents('./../bandits_total_results.csv')
    
    project_descriptions.pop(0) #removing column names
    project_categories = []

    # match_project_name_and_description_name(project_smells, project_descriptions)
         

    for smell in project_smells:
        project_name = smell[0]
        project_category_name = None
        
        smell_name = smell[1]
        smell_count = int(smell[2])

        already_included = False

        for description in project_descriptions:
            if project_name == description[0]: 
                project_category_name = description[2]
                break
        
        for project_category in project_categories:
            if project_category[0] == project_category_name and project_category[1] == smell_name:
                project_category[2] += int(smell_count)
                already_included = True
                break

        if already_included is False:
            project_categories.append([project_category_name, smell_name, int(smell_count)])

    
    total_smells_in_categories = []
    for category in project_categories:

        already_included = False
        for total_smell in total_smells_in_categories:
            if category[0] in total_smell:
                total_smell[1] = int(total_smell[1]) + int(category[2])
                already_included = True
                break
        
        if already_included is False:
            total_smells_in_categories.append([category[0], int(category[2])])

    total_smell_count = 0
    for total_smell in total_smells_in_categories:
        total_smell_count += int(total_smell[1])
    
    print(total_smells_in_categories)
    print('total smell count in categories %s' %total_smell_count)

    clear_file_contents('./../total_smell_in_categories.csv')
    for total_smell in total_smells_in_categories:
        write_to_csv_file('./../total_smell_in_categories.csv', total_smell)


    clear_file_contents('./../project_categories.csv')
    
    project_categories.sort(key = lambda x: x[0])
    for category in project_categories:
        print(category)
        write_to_csv_file('./../project_categories.csv', [category[0], '%s & - & %s \\\\ \\hline' % (category[1], str(category[2]))])