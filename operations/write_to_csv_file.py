import csv

def write_to_csv_file(filename, content):
    
    with open(filename, 'a') as fp: 
        fw = csv.writer(fp)
        fw.writerow(content)