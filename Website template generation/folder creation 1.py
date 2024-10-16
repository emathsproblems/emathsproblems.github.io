#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 10:28:00 2024

@author: bill
"""


#set up preferred file names

import glob
import os
# pip install titlecase
from titlecase import titlecase

docs_directory = '/home/bill/emathsproblems.github.io/docs/assets/documents/'
templates_directory = '/home/bill/emathsproblems.github.io/1_templates/'
components_directory = '/home/bill/emathsproblems.github.io/2_components/'

# directory = '/home/bill/emathsproblems.github.io/docs/assets/documents/'

file_type = '.odt'

#%%

# full_names = glob.glob(docs_directory + '**/*.pdf', recursive=True)
out_of_folder = glob.glob(docs_directory + '*' + file_type, recursive=False)
# full_names = glob.glob(docs_directory + '**/*.odt', recursive=True)

for doc in out_of_folder:
    file_name = os.path.basename(doc)
    folder_name = file_name.replace(file_type, '') + '/'
    try:
        os.makedirs(docs_directory + folder_name)
    except:
        None
    os.rename(doc, docs_directory + folder_name + file_name)

#%%
# removing punctuation and sorting out capitalisation

full_names = glob.glob(docs_directory + '**/*.odt', recursive=True)

directory_list = []
file_name_list = []

for full_name in full_names:
    
    file_path = os.path.dirname(full_name)
    new_name = os.path.basename(full_name)
           
    new_name = new_name.replace("'", "")
    new_name = new_name.replace("’", "")
    new_name = new_name.replace(",", " ")
    new_name = new_name.replace("-", " ")
            
    new_name = titlecase(new_name.split('.')[0]) + "." + ".".join(new_name.split('.')[1:])
    
    file_name_list.append(new_name)
    os.rename(full_name, file_path+'/'+new_name)


    subfolder = os.path.split(os.path.dirname(full_name))[1]
    new_subfolder = os.path.split(os.path.dirname(full_name))[1]

    new_subfolder = new_subfolder.replace("'", "")
    new_subfolder = new_subfolder.replace("’", "")
    new_subfolder = new_subfolder.replace(",", " ")
    new_subfolder = new_subfolder.replace("-", " ")

    new_subfolder = titlecase(new_subfolder)

    directory_list.append(new_subfolder)
    os.rename(docs_directory + subfolder, docs_directory + new_subfolder)

#%%
import csv
from difflib import SequenceMatcher


with open(docs_directory+'contents.csv', 'r') as f:
    reader = csv.reader(f)
    contents_data = list(reader)    

variable_data_pdf = []
prev_variables = ['filename', '{{{pdf}}}']
line_count = 0
with open(components_directory+'sidebar_var_list.txt', 'r') as f:
    for line in f:
        prev_variables.append(line.rstrip())
        line_count += 1
    # reader = csv.reader(f)
    # contents_data = list(reader)
variable_data_pdf.append(prev_variables)
collapse_position = -1
prev_collapse_folder = ''

match_file = {}
match_dir = {}

rename_dir = {}
rename_file = {}

for line in contents_data:
    rename_dir[line[0]] = line[1]
    rename_dir[line[2]] = line[3]
    
    displayed_folder = line[0]
    displayed_file = line[2]
    
    found_flag = False
    found_file = False
    found_folder = False
    if titlecase(displayed_folder) in directory_list and titlecase(displayed_file)+file_type in file_name_list:
        undisplayed_folder = titlecase(displayed_folder)
        undisplayed_file = titlecase(displayed_file)
        found_flag = True

    else:
        max_folder_score = 0.6
        for possible_dir_name in directory_list:
            score = SequenceMatcher(None, possible_dir_name, displayed_folder).ratio()
            if max_folder_score < score:
                max_folder_score = score
                undisplayed_folder = possible_dir_name
                found_folder = True
                
        max_file_score = 0.6
        for possible_file_name in file_name_list:
            score = SequenceMatcher(None, possible_file_name, displayed_file).ratio()
            if max_file_score < score:
                max_file_score = score
                undisplayed_file = possible_file_name.replace(file_type, '')
                found_file = True
                            
                
        if found_folder and found_file:
            found_flag = True
                
    # if found_flag2:
    #     print(displayed_folder)
    #     print(undisplayed_folder)
    #     print(displayed_file)
    #     print(undisplayed_file)
    #     print(max_score)         
                
    #     print()
                
    if not found_flag:
        print(displayed_folder)
        print(undisplayed_folder)
        print(displayed_file)
        print(undisplayed_file)
        print(max_score)         
    
        print()

    collapse_line = ['collapse'] * line_count
    if prev_collapse_folder != undisplayed_folder:
        collapse_position += 1
    collapse_line[collapse_position] = 'collapse show'
    prev_collapse_folder = str(undisplayed_folder)
            
    variable_data_pdf.append([undisplayed_file +'.html', undisplayed_folder + '/' + undisplayed_file +'.pdf'] + collapse_line)

    match_file[displayed_file] = undisplayed_file
    match_dir[displayed_folder] = undisplayed_folder

#%%
# with open(docs_directory + 'textbook_names.csv', 'w', newline='') as csvfile:
with open(templates_directory + 'textbook_data.csv', 'w', newline='') as csvfile:

    writer = csv.writer(csvfile)
    writer.writerows(variable_data_pdf)

#%%

with open(docs_directory+'contents.csv', 'r') as f:
    reader = csv.reader(f)
    contents_data = list(reader)


from collections import defaultdict

output_dict = defaultdict(list)

contents_order = []
for line in contents_data:
    if line[1] not in contents_order:
        contents_order.append(line[1])
        
    # output_dict[line[0]].append(match_dir[line[0]])
    # output_dict[line[1]].append(match_file[line[2]])
    output_dict[line[1]].append(line[3])
    # output_dict[line[0]].append(match_dir[line[0]] + '/' + match_file[line[2]] + '.html')
    output_dict[line[1]].append(match_file[line[2]] + '.html')

sidebar_output = []
sidebar_first_line = ['filename']
for i in range(1,30):
    sidebar_first_line.append('{{{' + str(i) + '}}}')
sidebar_output.append(sidebar_first_line)

for i in range(len(contents_order)):
    # output_line = ['sidebar_proc.html', 'Ch' + str(i), line[i], output_dict[line[i]]]
    
    # sidebar_output.append(['sidebar_proc.html', 'Ch' + str(i), contents_order[i], output_dict[contents_order[i]]])
    output_line = ['sidebar_proc.html', 'Ch' + str(i)] + [contents_order[i]] + output_dict[contents_order[i]]
    output_line += [''] * (30 - len(output_line))                  
                                                                        
    sidebar_output.append(output_line)
    
# for line in contents_order:
#     sidebar_output.append([line] + output_dict[line])

#%%

# with open(docs_directory + 'sidebar_formatted.csv', 'w', newline='') as csvfile:
with open(components_directory + 'sidebar_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(sidebar_output)
    
    
#%%
variable_data_pdf = []
prev_variables = ['filename']

with open(components_directory+'sidebar_var_list.txt', 'r') as f:
    for line in f:
        prev_variables.append(line.rstrip())
        line_count += 1
    # reader = csv.reader(f)
    # contents_data = list(reader)
variable_data_pdf.append(prev_variables)

collapse_line = ['index.html', 'collapse show'] + ['collapse'] * (len(variable_data_pdf[0])-2)

combined = variable_data_pdf + [collapse_line]

with open(templates_directory + 'index_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(combined)
    











    
    
    
