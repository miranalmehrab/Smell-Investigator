import os
from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file 


def save_individual_smell_occurence_count():    
    unique_smell_counts = []
    smells = list_csv_contents('logs/smells/detected_smells.csv')

    for smell in smells:
        found = False
        for row in unique_smell_counts:
            if smell[2] in row:
                row[1] = row[1]+1
                found = True
                break   

        if found is False:
            unique_smell_counts.append([smell[2], 1])

    unique_smell_counts.sort(key = lambda x: x[1], reverse = True)
    for smell_count in unique_smell_counts:
        write_to_csv_file('logs/smells/smell_frequency.csv',smell_count)    



def save_detected_smells_in_separate_file():
    smells = list_csv_contents('logs/smells/detected_smells.csv')
    
    for smell in smells:
        
        token = smell[-1]
        filename = smell[1]
        identified_smell = smell[2]
        file_path = os.path.join('./logs/smell-categories/{filename}.csv'.format(filename = identified_smell)) 
        
        if os.path.isfile(file_path) is False:
            with open(file_path, 'w') as fp:
                pass
        
        write_to_csv_file(file_path, [filename, token])

def save_smell_frequency():
    save_individual_smell_occurence_count()
    save_detected_smells_in_separate_file()
