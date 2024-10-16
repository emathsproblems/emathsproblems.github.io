#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:25:55 2024

@author: bill
"""

import csv

website_directory = '/home/bill/emathsproblems.github.io/'
templates_directory = website_directory + '1_templates/'
components_directory = website_directory + '2_components/'
pages_directory = website_directory + '3_pages/'

order_filename = website_directory + '1_templates/1_build_order.txt'

import glob


order_data = []
with open(order_filename) as order_file:
    for line in order_file:
        order_data.append([line.split(' #### ')[0], line.split(' #### ')[1].rstrip(), line.split(' #### ')[2].rstrip()])
        
for file_pair in order_data:
    html_components = glob.glob(components_directory + '*.html')
   
    template_data = []
    with open(website_directory + file_pair[0]) as template_file:
        for line in template_file:
            template_data.append(line)
            
    replacement_data = []
    with open(website_directory + file_pair[1]) as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in datareader:
            replacement_data.append(row)        
            
            
            
            
    if file_pair[2] == 'concat':
        output_section = []
        repetitions = len(replacement_data[0]) - 1
        variables = len(replacement_data)
        template_length = len(template_data)
        new_var_num = 0
        variable_list = []
        
        for i in range(1,repetitions+1):              # iterate by number of columns
        # for i in range(1,2):              # iterate by number of columns
            
            replacement_dict = {}
            for j in range(variables):
                replacement_dict[replacement_data[j][0]] = replacement_data[j][i]

            for j in range(template_length):      # template line by line
            # for j in range(1):      
                missing_var = False
                missing_var = []
                line_text = template_data[j]
            
       
               
                for key in replacement_dict.keys():      # check each variable
                    # print(key)
                    # print(line_text)
                    # print(key in line_text)
                
                    if key in line_text:
                        if replacement_dict[key] != '':                        
                           line_text = line_text.replace(key, replacement_dict[key])
                        else:
                            missing_var = True
                            # print(key)
     
                while '((()))' in line_text:
                    variable_name = '{{{' + file_pair[0] + str(new_var_num) + '}}}'
                    variable_list.append(variable_name)
                    line_text = line_text.replace('((()))', variable_name, 1)
                    new_var_num += 1   
             
                # print(missing_var)
                if not missing_var:
                    output_section.append(line_text)         
                # else:
                    # print('missing var')                      
                    
                
    with open(website_directory + '/' + file_pair[0].split('.')[0] + '_proc.html', "w") as f:
        for line in output_section:
            f.write(line)
    
    with open(website_directory + '/' + file_pair[0].split('.')[0] + '_var_list.txt', "w") as f:
        for line in variable_list:
            f.write(line+'\n')
                    
            
            
                    
    if file_pair[2] == 'repeat':        
        repetitions = len(replacement_data[0]) - 1
        variables = len(replacement_data)
        template_length = len(template_data)
        new_var_num = 0
        variable_list = []
        
        
        for j in range(template_length):      # template line by line
            line_text = template_data[j]
        
            if '[[[' in line_text:              # html replacement
             # print(line_text)
             for component in html_components:
                 # print('[[[' + component.replace(components_directory,'') + ']]]')
                 if '[[[' + component.replace(components_directory,'') + ']]]' in line_text:
                     with open(component, 'r') as file:
                         file_text = file.read()
                     line_text = line_text.replace('[[[' + component.replace(components_directory,'') + ']]]', file_text)
                     # print('success')
                     # print(line_text)
                     # print()
            
            template_data[j] = line_text            
        
        
        for i in range(1,repetitions+1):              # iterate by number of columns
        # for i in range(1,2):              # iterate by number of columns
            output_section = []
            
            replacement_dict = {}
            for j in range(variables):
                replacement_dict[replacement_data[j][0]] = replacement_data[j][i]

            for j in range(template_length):      # template line by line
            # for j in range(1):      
                missing_var = False
                missing_var = []
                line_text = template_data[j]
              
                for key in replacement_dict.keys():      # check each variable
                    # print(key)
                    # print(line_text)
                    # print(key in line_text)
                
                    if key in line_text:
                        if replacement_dict[key] != '':                        
                           line_text = line_text.replace(key, replacement_dict[key])
                        else:
                            missing_var = True
     
                while '((()))' in line_text:
                    variable_name = '{{{' + file_pair[0] + str(new_var_num) + '}}}'
                    variable_list.append(variable_name)
                    line_text = line_text.replace('((()))', variable_name, 1)
                    new_var_num += 1   
             
                # print(missing_var)
                if not missing_var:
                    output_section.append(line_text)                               
                # else:
                    # print('missing var')
            
            
            # os.makedirs(os.path.dirname(website_directory + replacement_dict['filename']), exist_ok=True)
            
            with open(website_directory + replacement_dict['filename'], "w") as f:
                # print(website_directory + replacement_dict['filename'])
                for line in output_section:
                    f.write(line)
            
            with open(website_directory + replacement_dict['filename'].split('.')[0] + '_var_list.txt', "w") as f:
                for line in variable_list:
                    f.write(line+'\n')

                    
            