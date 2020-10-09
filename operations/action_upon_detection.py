import os
from operations.write_to_csv_file import write_to_csv_file

def action_upon_detection(project_name, src_file, lineno, smell, msg, token):
    
    name = src_file.name
    name = name.split('/')[-1]

    print(msg +' at line '+ str(lineno))
    # write_to_csv_file('logs/smells/detected_smells.csv',[project_name,os.path.join(project_name, src_file),smell,msg, str(lineno), token])
    write_to_csv_file('logs/smells/detected_smells.csv',[project_name,src_file.name,smell,msg, str(lineno), token])