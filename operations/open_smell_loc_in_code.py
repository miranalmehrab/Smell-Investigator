import os
import json
import subprocess

from .write_to_csv_file import write_to_csv_file 
from .list_csv_contents import list_csv_contents

def open_smell_location():
    vscode_open_commands = []
    smell_descriptions = list_csv_contents('curr-smell.csv')
    
    unique_tokens = []
    token_repeatition_counter = 0

    for description in smell_descriptions:

        # if description[1] not in unique_tokens: 
        #     unique_tokens.append(description[1])
        # else: print(description[1])

        token_splits = description[1].split(',') 
        line_info = token_splits[1]

        file_name = ((description[0].strip().replace(' ', '\\ ')).strip().replace('(', '\\(')).strip().replace(')', '\\)')
        vscode_open_command = 'code -g '+ file_name +':'+line_info.split(':')[1].strip()
        # vscode_open_command = file_name +':'+line_info.split(':')[1].strip()        
        vscode_open_commands.append(vscode_open_command)
    
    # print(len(vscode_open_commands))
    # print(len(unique_tokens))
    # print('number of token repeatition - '+str(token_repeatition_counter))

    command_counter = 1
    for vscode_open_command in vscode_open_commands:
        if command_counter > 0 and command_counter < 101:
            print('file no. - '+str(command_counter) + ' ' + vscode_open_command)
        command_counter += 1
        
    #     try: os.system(vscode_open_command)
    #     except: print('Error opening source code - '+ str(counter)) 