from operations.save_project_smells import save_detected_different_smells_frequency_in_projects
from operations.save_project_smells import save_smells_categorized_according_to_project_type
# from operations.find_correlation import find_correlation

from operations.list_csv_contents import list_csv_contents
from operations.write_to_csv_file import write_to_csv_file

from operations.save_smell_frequency import save_smell_frequency
from operations.show_detection_result import show_detection_result
from operations.individual_smell_introduction import individual_smell_introduction_in_total_number_of_projects

from operations.save_project_smells import save_total_smell_counts_in_projects
from operations.save_project_smells import save_unique_smell_counts_in_projects

from operations.run_bandit_on_folder import run_bandit_on_folder
from operations.run_bandit_on_folder import summerize_bandit_output
from operations.run_bandit_on_folder import show_specific_smells

from operations.bandit_operations import list_smells_in_projects_sequentially
from operations.bandit_operations import match_project_categories_from_bandit_results

from operations.bandit_operations import total_frequency_of_smells
from operations.bandit_operations import number_of_smelly_projects

from operations.open_smell_loc_in_code import open_smell_location 

from run_on_single_code import RunOnSingleSourceCode
from run_on_code_folder import  RunDetectionOnSourceCodeFolder


def main():
    token_folder_name = './test-codes/token-generation/'
    token_test_files = ['assign.py', 'comparison.py', 'expression.py', 'function_def.py', 'imports.py', 'src.py']

    smell_folder_name = './test-codes/smelly-codes/'
    smell_test_files = [
                            'assert_used.py','bad_file_permission.py','command_injection.py','debug_true.py','deserialization.py',
                            'dynamic_evaluation.py','empty_password.py','hardcoded_secret.py','http_only.py','ignore_exception.py',
                            'ip_binding.py','no_certificate_validation.py','no_integrity.py', 'sql_injection.py','temp_dir.py',
                            'weak_cryptography.py', 'xss.py','yaml_used.py'   
                    ]

    # src_file_name = token_folder_name + token_test_files[0]
    src_file_name = smell_folder_name + smell_test_files[3]         
    single_code = RunOnSingleSourceCode(src_file_name, False, True)
    single_code.analyze_single_code()

    # code_folder_name = './../final-unzips/'
    # code_folder = RunDetectionOnSourceCodeFolder(code_folder_name, False, False)
    # code_folder.run_analyze_code_folder()

    # open_smell_location()
    
    # show_categories_in_project_descriptions()
    # find_correlation()
    

    # <---------------------------------------- bandit operations starts from here ----------------------------------------> 
    # run_bandit_on_folder()
    # summerize_bandit_output()
    # list_smells_in_projects_sequentially()

    # match_project_categories_from_bandit_results()
    # show_specific_smells()
    
    # total_frequency_of_smells()
    # number_of_smelly_projects()

    
if __name__ == "__main__":
    main()
