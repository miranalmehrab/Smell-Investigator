from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file 

def print_results_and_errors(detected_smells, parsing_errors, token_errors, detection_errors):
    print('')
    print('------------------------------ Result ------------------------------ ')
    print('number of detected smells: '+ str(len(detected_smells)))
    print('number of token parsing errors: '+ str(len(parsing_errors)))
    print('number of token loading errors: '+ str(len(token_errors)))
    print('number of token detecting errors: '+ str(len(detection_errors)))


def show_detection_result():
    detected_smells = list_csv_contents('logs/smells/detected_smells.csv')
    parsing_errors = list_csv_contents('logs/errors/token_parsing_exceptions.csv')
    loading_errors = list_csv_contents('logs/errors/token_loading_exceptions.csv')
    detection_errors = list_csv_contents('logs/errors/token_detection_exceptions.csv')
    
    print_results_and_errors(detected_smells, parsing_errors, loading_errors, detection_errors)