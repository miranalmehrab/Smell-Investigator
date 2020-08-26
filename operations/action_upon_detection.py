from operations.write_to_csv_file import write_to_csv_file

def action_upon_detection(project_name, src_file, lineno, smell, msg):
    
    name = src_file.name
    name = name.split('/')[-1]

    print(msg +' at line '+ str(lineno))
    write_to_csv_file('logs/detected_smells.csv',[project_name,name,smell, str(lineno)])
    

