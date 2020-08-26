from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file 


def print_results_and_errors(detected_smells, parsing_errors, token_errors, detection_errors):
    print('')
    print('------------------------------ Result ------------------------------ ')
    print('number of detected smells: '+ str(len(detected_smells)))
    print('number of token parsing errors: '+ str(len(parsing_errors)))
    print('number of token loading errors: '+ str(len(token_errors)))
    print('number of token detecting errors: '+ str(len(detection_errors)))


def save_individual_smell_occurence_count(smells):
    unique_smell_counts = []
    
    for smell in smells:
        found = False
        for row in unique_smell_counts:
            if smell[2] in row:
                row[1] = row[1]+1
                found = True
                break   

        if found is False:
            unique_smell_counts.append([smell[2], 0])

    unique_smell_counts.sort(key = lambda x: x[1], reverse = True)
    for smell_count in unique_smell_counts:
        write_to_csv_file('logs/unique_smell_count.csv',smell_count)    


def show_detection_result():
    detected_smells = list_csv_contents('logs/detected_smells.csv')
    parsing_errors = list_csv_contents('logs/token_parsing_exceptions.csv')
    loading_errors = list_csv_contents('logs/token_loading_exceptions.csv')
    detection_errors = list_csv_contents('logs/token_detection_exceptions.csv')
    
    save_individual_smell_occurence_count(detected_smells)
    print_results_and_errors(detected_smells, parsing_errors, loading_errors, detection_errors)