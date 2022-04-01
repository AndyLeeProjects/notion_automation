<<<<<<< HEAD
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
        month_data = {}
        if len(str(month)) == 1:
            file_date = '0'+str(month) + str(year)
        else:
            file_date = str(month) + str(year)
        
        with open(path % file_date, encoding='utf-8') as file:
            file = file.readlines()
            titles = file[0].split(',')
            
            # Delete some of the encoding glitch
            titles[0] = titles[0].strip('\ufeff').replace('癤풬', 'N')
            del file[0]
            file.reverse()
            
            for line in file:
                line = line.split(',')
                # Read 3 Key words correctly
                key_words = []
                
                if len(line)>33:
                    
                    key_words.append([line[12].strip('\" '),line[13].replace(' ',''),line[14].strip('\"\' ')])
                    line[12] = key_words[0]
                    del line[13], line[13]
                
                
                # 'Created' element has comma in it, so all data after 'Created' gets shifted
                if ' ' in line[6] and year != 20: # year 20 had different format
                    line[6] = line[6]+line[7]
                    del line[7]
                else:
                    line[5] = line[5].split(' ')[0]

                for e in range(len(line)):
                    
                    titles[e] = titles[e].strip('\n')
                    month_data.setdefault(titles[e],[])        
                    try:
                        if line[e] == '':
                            month_data[titles[e]].append(float('0.0'))
                        elif type(line[e]) == type([]):
                            month_data[titles[e]].append(line[e])
                        else:
                            month_data[titles[e]].append(float(line[e].strip('\n')))
                    except:
                        try:
                            month_data[titles[e]].append(line[e].strip('\n'))
                        except:
                            pass
        try:
            sortedindex = np.argsort(month_data['Date'])
            for t in range(len(titles)):
                new_values = [month_data[titles[t]][index]
                    for index in sortedindex]
                month_data[titles[t]] = new_values
        except:
            pass
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
        all_dat = pCor.CorSetUp(months_key, purpose)
        return all_dat, months_key
            
                
                

mon = read_data()
month = mon.monthly(9,20)
all_data = mon.all_data('include date')[0]
months_key = mon.all_data('include date')[1]


=======
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
        month_data = {}
        if len(str(month)) == 1:
            file_date = '0'+str(month) + str(year)
        else:
            file_date = str(month) + str(year)
        
        with open(path % file_date, encoding='utf-8') as file:
            file = file.readlines()
            titles = file[0].split(',')
            
            # Delete some of the encoding glitch
            titles[0] = titles[0].strip('\ufeff').replace('癤풬', 'N')
            del file[0]
            file.reverse()
            
            for line in file:
                line = line.split(',')
                # Read 3 Key words correctly
                key_words = []
                
                if len(line)>33:
                    
                    key_words.append([line[12].strip('\" '),line[13].replace(' ',''),line[14].strip('\"\' ')])
                    line[12] = key_words[0]
                    del line[13], line[13]
                
                
                # 'Created' element has comma in it, so all data after 'Created' gets shifted
                if ' ' in line[6] and year != 20: # year 20 had different format
                    line[6] = line[6]+line[7]
                    del line[7]
                else:
                    line[5] = line[5].split(' ')[0]

                for e in range(len(line)):
                    
                    titles[e] = titles[e].strip('\n')
                    month_data.setdefault(titles[e],[])        
                    try:
                        if line[e] == '':
                            month_data[titles[e]].append(float('0.0'))
                        elif type(line[e]) == type([]):
                            month_data[titles[e]].append(line[e])
                        else:
                            month_data[titles[e]].append(float(line[e].strip('\n')))
                    except:
                        try:
                            month_data[titles[e]].append(line[e].strip('\n'))
                        except:
                            pass
        try:
            sortedindex = np.argsort(month_data['Date'])
            for t in range(len(titles)):
                new_values = [month_data[titles[t]][index]
                    for index in sortedindex]
                month_data[titles[t]] = new_values
        except:
            pass
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
        all_dat = pCor.CorSetUp(months_key, purpose)
        return all_dat, months_key
            
                
                

mon = read_data()
month = mon.monthly(9,20)
all_data = mon.all_data('include date')[0]
months_key = mon.all_data('include date')[1]


>>>>>>> 572dc86 (update)
