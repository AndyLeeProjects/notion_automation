# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:37:11 2021

@author: anddy
"""

import numpy as np
import sys, os
# Change the path name depending on the operating system
if os.name == 'posix':
    sys.path.append('/Volumes/Programming/Personal/progress/myPackage')
else:
    sys.path.append('C:\\NotionUpdate\progress\myPackage')
import NotionprocessCorr as pCor
import os
import pandas as pd


'''
Read Files
'''
    
class read_data():
    
    def __init__(self):
        pass
    
    
    # Read Monthly
    # monthly(5, 21)
    def monthly(self, month, year):

        # Change the path name depending on the operating system
        if os.name == 'nt':
            path = r'C:\\NotionUpdate\progress\Data\%s.csv'
        else:        
            path = r'/Volumes/Programming/Personal/progress/Data/%s.csv'
        file_name = str.zfill(str(month),2) + str(year)
        month_data = pd.read_csv(path % file_name)

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
                                   'Total To-do List':'Tot To-do', 'Phone pickups':'Pickups', 'Productivity & Focus':'Productivity'})
        return month_data

    def DeleteUnnecessaryVar(data,purpose):
        """
        Depending on the purpose of the use of the data, return appropriate columns
        """
        if 'include date' in purpose:
            deleteKeys = ['Finished','Meditation %','Multiple %',
                    'Rise time %','Screen time %','Pick up %',
                    'Drink %', 'Reading %', 'Books finished',
                    'Run %', 'Events','Screen Time %','Multiple EST']
        elif 'RSTUDIO' == purpose:
            deleteKeys = ['Meditation %','Multiple %',
                    'Rise time %','Screen time %','Pick up %',
                    'Drink %', 'Reading %', 'Books finished',
                    'Run %', 'Events','Screen Time %','Multiple EST']
        else:
            # Omit Date, since it only will be needed for monthly dependency
            deleteKeys = ['Date','Finished','Meditation %','Multiple %',
                    'Rise time %','Screen time %','Pick up %',
                    'Drink %', 'Reading %', 'Books finished',
                    'Run %', 'Events','Screen Time %', 'Multiple EST']

        for item in deleteKeys:
            try:
                del data[item]
            except:
                pass
        return data
    
    def combine_dataframes(months_dfs):
        all_dat = {}
        for month_var in months_dfs[-1].keys():
            for month_df in months_dfs:
                if month_var not in month_df:
                    pass
                elif 'Drink' in month_df[month_var]: # Error in Drink variable so pass 
                    pass
                    
                else:
                    all_dat.setdefault(month_var, [])
                    
                    # The date is in descending order so fix it 
                    reversed_list = list(reversed(month_df[month_var]))
                    
                    # Since j comes as a dataframe format, need to change into a list format
                    all_dat[month_var] += reversed_list
                    
        return all_dat


    def fill_data(months_dfs, purpose):
        all_dat = read_data.combine_dataframes(months_dfs)
        
        # If the size don't match, make the difference 0
        for i in all_dat.keys():
            if len(all_dat[i]) != len(all_dat['Name']):
                all_dat[i] = [0]*(len(all_dat['Name'])-len(all_dat[i]))+all_dat[i]
        
        # Delete unimportant, redundant factor 
        all_dat = read_data.DeleteUnnecessaryVar(all_dat, purpose)
        return all_dat

    def all_data(self, purpose):
        # Fix year & date when I began collecting data: September 2020
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
<<<<<<< HEAD
        all_dat = pd.DataFrame(pCor.CorSetUp(months_key, purpose))
        return all_dat, months_key
=======
            
        return pd.DataFrame(read_data.fill_data(months_key, purpose)), months_key
>>>>>>> 7e4030305dca870564d02494cb9440555ca1a5f6
    
    def save_to_Ddrive(self, all_dat):
        # Save the data in the D drive for further statistical analysis
        all_dat.to_csv(r'C:\NotionUpdate\progress\Data\all_dat.csv')
        try:
            all_dat.to_csv(r'D:\Spring 2022\Project\all_dat.csv')
            all_dat.to_csv(r'D:\Personal\progress\Data\all_dat.csv')
            print("all_dat.csv saved to D Drive")
            print()
        except:
            pass
    

<<<<<<< HEAD
#RDATA = read_data()
#mon = RDATA.monthly(12, 21)
#all_data = RDATA.all_data("include date")[0]
=======
            
        


>>>>>>> 7e4030305dca870564d02494cb9440555ca1a5f6







