import os
import json
import subprocess

from .write_to_csv_file import write_to_csv_file 
from .list_csv_contents import list_csv_contents

def open_smell_location():
    vscode_open_commands = []
    smell_descriptions = list_csv_contents('curr-smell.csv')
    
    for description in smell_descriptions:
        line_info = description[1].split(',')[1]
        vscode_open_command = 'code -g '+description[0]+':'+line_info.split(':')[1].strip().replace(' ', '\\')
        
        vscode_open_commands.append(vscode_open_command)

    for vscode_open_command in vscode_open_commands:
        print(vscode_open_command)