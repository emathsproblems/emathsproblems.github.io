#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 12:54:04 2024

@author: bill
"""

website_directory = '/home/bill/emathsproblems.github.io/'
components_directory = '2_components'
order_filename = website_directory + '1_templates/1_build_order.txt'

order_data = []
html_components = []
with open(order_filename) as order_file:
    for line in order_file:
        if line.split(' #### ')[0].split('/')[0] == components_directory:
            html_components.append([line.split(' #### ')[0], line.split(' #### ')[3]])

for html_component in html_components:
    with open(website_directory + html_component[0]) as component_file:
        var_list = []
        for entry in component_file:
            if '((()))' in entry:
                for i in range(int(html_component[1].rstrip())):
                    var_list.append('{{{' + html_component[0] + str(i) + '}}}')

    if var_list != []:
        with open(website_directory + '/' + html_component[0].split('.')[0] + '_var_list.txt', "w") as f:
            for line in var_list:
                f.write(line+'\n')
    
    
    
    
    