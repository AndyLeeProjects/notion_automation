# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:37:11 2021

@author: anddy
"""

import numpy as np
import sys
sys.path.append('C:\\NotionUpdate\\progress\\myPackage')
import NotionprocessCorr as pCor
import os
import pandas as pd


'''
**********************************************************************
*****************************[Read Files]*****************************
**********************************************************************
'''


if os.name == 'nt':
        path = 'C:\\NotionUpdate\progress\Data\%s.csv'
else:
    path = '/Volumes/Programming/Personal/progress/Data/%s.csv'
    
class read_data():
    
    def __init__(self):
        pass
    
    
    # Read Monthly
    # monthly(5, 21)
    def monthly(self, month, year):
        file_name = str.zfill(str(month),2) + str(year) + '.csv'
        month_data = pd.read_csv(r'C:\NotionUpdate\progress\Data\%s' % file_name)

                

        # Since these keys are represented by '⭐️', we need to change them into 
        # numerical values.
        keys = ['Social', 'Tech Consumption','Overall Satisfaction','Mentality','Productivity']
        try:
            if '⭐️' in str(month_data['Social']):
                for key in keys:
                    values = []
                    for v in month_data[key]:
                        if v == 0:
                            values.append(v)
                        else:
                            values.append(len(v)/2)
                    month_data[key] = values
        except:
            pass
        month_data = pd.DataFrame(month_data)
        # Rename the titles
        month_data = month_data.rename(columns={'*Finished': 'Finished', '*Multiple (1~5)': 'Multiple','*Phone pickups':'Phone pickups',
                                   '*Screen time':'Screen time','Drink (%)':'Drink %', 'Drink? (over 3 beer)':'Drink',
                                   'Meditation (%)':'Meditation %', 'Meditation (min)':'Meditation', 'Multiple (%)':'Multiple %',
                                   'Pick up (%)':'Pick up %', 'Reading (%)':'Reading %', 'Rise time (%)':'Rise time %',
                                   'Run (%)':'Run %', 'Run (km)':'Run', 'Screen Time (%)':'Screen Time %', 'Work done (%)': 'Work done %',
                                   'Overall Satisfaction':'Satisfaction','Personal Reading':'Reading','Tech Consumption':'Tech',
                                   'Total To-do List':'Tot To-do', 'Phone pickups':'Pickups'})
        return month_data
    
    def all_data(self, purpose):
        year = 20
        month = 9
        months_key = []
        while True:
            try:
                
                if month == 13:
                    month = 1
                    year += 1
                months_key.append(self.monthly(month, year))
            except:
                
                break
            month += 1
        all_dat = pd.DataFrame(pCor.CorSetUp(months_key, purpose))
        
        return all_dat, months_key
    
    def save_to_Ddrive(self, all_dat):
        # Save the data in the D drive for further statistical analysis
        try:
            all_dat.to_csv(r'D:\Spring 2022\Project\all_dat.csv')
            print("all_dat.csv saved to D Drive")
            print()
        except:
            pass
            
                










