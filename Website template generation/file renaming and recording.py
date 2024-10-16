#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:49:30 2024

@author: bill
"""

# put all files into folders
# create sheet with columns: Folder, Filename, HTML Filename, Displayed Filename





import glob
import os
# pip install titlecase
from titlecase import titlecase

directory = '/home/bill/emathsproblems.github.io/docs/assets/documents/'

full_names = glob.glob(directory + '**/*.pdf', recursive=True)

directory_list = []
file_name_list = []

for full_name in full_names:
    
    file_path = os.path.dirname(full_name)
    new_name = os.path.basename(full_name)
           
    if "'" in full_name:
        new_name = new_name.replace("'", "")
    if "’" in full_name:
        new_name = new_name.replace("’", "")
    if "-" in full_name:
        new_name = new_name.replace("-", " ")
            
    new_name = titlecase(new_name.split('.')[0]) + "." + ".".join(new_name.split('.')[1:])
    
    directory_list.append(file_path.replace(os.path.dirname(file_path) + '/', ''))
    file_name_list.append(new_name)
    
    os.rename(full_name, file_path+'/'+new_name)

#%%

import csv
from difflib import SequenceMatcher

with open(directory+'Contents.csv', 'r') as f:
    reader = csv.reader(f)
    contents_data = list(reader)
    
output_filenames = []
match_file = {}
match_dir = {}

for line in contents_data:
    sub_directory = line[0]

    if line[1] == '':
        file_name = line[0]
        file_path = ""
    else:
        file_name = line[1]
        file_path = line[0]
    
    max_score = 0
    for possible_file_name in file_name_list:
        score = SequenceMatcher(None, possible_file_name, file_name).ratio()
        if max_score < score:
            max_score = score
            match_file[file_name] = possible_file_name
    
    max_score = 0
    for possible_dir_name in directory_list:
        score = SequenceMatcher(None, possible_dir_name, file_path).ratio()
        if max_score < score:
            max_score = score
            match_dir[file_path] = possible_dir_name
    
#%%
import numpy as np

output_list = []

for line in contents_data:
    
    if line[1] == '':
        page_pdf = match_file[line[0]]
        page_html = page_pdf.replace('.pdf', '.html')
        output_list.append([page_html, page_pdf])
               
    else:
        page_pdf = match_file[line[1]]
        page_html = page_pdf.replace('.pdf', '.html')
               
        page_folder = match_dir[line[0]]
        
        output_list.append([page_html, page_folder + '/' + page_pdf])
    
np.savetxt(directory + 'filenames_formatted.csv', np.asarray(output_list), delimiter=',', fmt="%s")
    
#%%
import numpy as np
from collections import defaultdict

output_dict = defaultdict(list)
contents_order = []

for line in contents_data:
    if line[0] not in contents_order:
        contents_order.append(line[0])
    
    if line[1] == '':
        page_pdf = match_file[line[0]]
        page_plain = page_pdf.replace('.pdf', '')
        output_dict[page_plain].append(page_plain)
        
    else:
        page_pdf = match_file[line[1]]
        page_plain = page_pdf.replace('.pdf', '')
               
        page_folder = match_dir[line[0]]
        
        output_dict[page_folder].append(page_plain)
        
sidebar_output = []
for line in contents_order:
    sidebar_output.append([line] + output_dict[line])
    

# np.savetxt(directory + 'filenames_formatted.csv', np.asarray(output_list), delimiter=',', fmt="%s")
    

    
    
    
    
    