import csv

def saveBugFix(node, params):

    with open('logs/bugFix.csv', 'a') as fp:    
        fw = csv.writer(fp)
        fw.writerow([node,params])
