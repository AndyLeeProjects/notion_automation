<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 13:30:44 2021

@author: anddy
"""

import requests
import sys
import numpy as np
sys.path.append('C:\\NotionUpdate\progress\Connect_NotionAPI')
from datetime import datetime
sys.path.append('C:\\NotionUpdate\progress')
from secret import secret
import pandas as pd
import os



DATABASE_ID = secret.notion_API("DATABASE_ID")
token_key = secret.notion_API("token_key")
NOTION_URL = 'https://api.notion.com/v1/databases/'
class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self,integration_token=token_key):
        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={"Authorization": token_key, "Notion-Version":'2021-05-13'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(self,data_json):
        most_properties = [len(data_json['results'][i]['properties'])
                                for i in range(len(data_json["results"]))]
        return list(data_json["results"][np.argmax(most_properties)]["properties"].keys())
    

    def get_projects_data(self,data_json,projects):
        projects_data = {}
        duration_temp = []        
        for p in projects:
            if "Related" in p:
                pass
            elif p !="To-do" and p != 'Duration':
                projects_data[p] = [data_json["results"][i]["properties"][p]["checkbox"]
                                    for i in range(len(data_json["results"]))]
            elif p=="To-do":
                names = [data['results'][i]['properties']['To-do']['title'][0]['text']['content']
                                    for i in range(len(data_json["results"]))]
            elif p=="Duration":
                for i in range(len(data_json["results"])):
                    try:
                        duration_temp.append(data['results'][i]['properties']['Duration']['number'])
                    except:
                        duration_temp.append(None)
                projects_data[p] = duration_temp

        # When everything is NULL, it causes KeyError
        try:
            projects_data['Duration']
        except KeyError:
            projects_data['Duration'] = [None]*len(names)

        return projects_data,names
    
    
    
    def MorningRoutine(self, projects_data, names):
        total_checked = []
        for i in range(len(names)):
            if names[i] == 'Meditation':
                meditation = projects_data['Duration'][i]
                meditation_checked = projects_data['Checkbox'][i]
                if meditation == None:
                    meditation = 0
            elif names[i] == 'Personal Reading':
                PR = projects_data['Duration'][i]
                reading_check = projects_data['Checkbox'][i]
                try:
                    if PR > 0:
                        reading = PR
                    else:
                        reading = 0
                except:
                    reading = 0
            elif names[i] == 'Rise Time & Phone Free (1hr)':
                rise_time = projects_data['Duration'][i]
                rise_time_check = projects_data['Checkbox'][i]
    
            elif names[i] == 'Phone Free Before Sleep (30 min)/ run (km)':
                run = projects_data['Duration'][i]
                before_sleep_check = projects_data['Checkbox'][i]
                if run == None:
                    run = 0
            elif names[i] == 'Morning Thoughts':
                morning_thoughts_check = projects_data['Checkbox'][i]
            elif names[i] == 'Push up':
                push_up_check = projects_data['Checkbox'][i]
                
            if projects_data['Checkbox'][i] == True:
                total_checked.append('Checked')
            
        total_checked = len(total_checked)
        
        return total_checked, meditation, rise_time, reading, run, \
            reading_check, rise_time_check, before_sleep_check, morning_thoughts_check, \
            push_up_check, meditation_checked
            
    def accru_morning_routine(self, projects_data, names):
        total_checked = nsync.MorningRoutine(projects_data, names)[0]
        meditation_min = nsync.MorningRoutine(projects_data, names)[1]
        rise_time_min = nsync.MorningRoutine(projects_data, names)[2]
        reading_min = nsync.MorningRoutine(projects_data, names)[3]
        run_km = nsync.MorningRoutine(projects_data, names)[4]
        reading_check = nsync.MorningRoutine(projects_data, names)[5]
        rise_time_check = nsync.MorningRoutine(projects_data, names)[6]
        before_sleep_check = nsync.MorningRoutine(projects_data, names)[7]
        morning_thoughts_check = nsync.MorningRoutine(projects_data, names)[8]
        push_up_check = nsync.MorningRoutine(projects_data, names)[9]
        meditation_check = nsync.MorningRoutine(projects_data, names)[10]
        date = datetime.today().strftime('%#m/%d/%Y')
        
        # Make a diction for a new row
        new_row = {'Date': date, 'total_checked': total_checked, 'before_sleep_check':before_sleep_check,
                   'rise_time_check': rise_time_check, 'meditation_min': meditation_min,
                   'meditation_check':meditation_check, 'rise_time_min':rise_time_min, 
                   'reading_check':reading_check, 'reading_min':reading_min,
                   'run_km':run_km, 'morning_thoughts_check':morning_thoughts_check,
                   'push_up_check':push_up_check}
        
        # Create a new data frame with above dict
        new_row = pd.DataFrame(data = new_row, index = [0])
        
        
        # Read csv file
        routine = pd.read_csv('C:\\NotionUpdate\progress\Connect_NotionAPI\morning_routine.csv',
                                  sep = ',', index_col = 0)
        # Reset index numbers (in order)
        try:
            routine = routine.reset_index()
        except:
            pass

        # Total checked in routine dataframe
        routine_total_checked = routine['total_checked'][len(routine['total_checked'])-1]
        
        # Compare "total_checked" and "routine_total_checked" to update the newest values

        if new_row['Date'][0] in list(routine['Date']) and total_checked <= routine_total_checked:
            pass
        else:
            if new_row['Date'][0] in list(routine['Date']) and total_checked > routine_total_checked:
                routine = routine.drop([routine.index[-1]])
            # Add the created row to existing csv file
            routine = pd.concat([routine, new_row], ignore_index = True, axis = 0)
            # Remove existing directory and Replace it with created dataframe
            os.remove('C:\\NotionUpdate\progress\Connect_NotionAPI\morning_routine.csv')
            # Save a csv file to replace the old one
            routine.to_csv('C:\\NotionUpdate\progress\Connect_NotionAPI\morning_routine.csv', encoding='utf-8')
            try:
                routine.to_csv('D:\Spring 2022\Project\morning_routine.csv')
            except:
                # This occurs when I don't have my usb plugged in
                pass



# Morning Routine
nsync = NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data,names = nsync.get_projects_data(data,projects)
nsync.accru_morning_routine(projects_data, names)









=======
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 13:30:44 2021

@author: anddy
"""

import requests
import sys
import numpy as np
sys.path.append('C:\\NotionUpdate\progress\Connect_NotionAPI')
from datetime import datetime
sys.path.append('C:\\NotionUpdate\progress')
from secret import secret
import pandas as pd
import os



DATABASE_ID = secret.notion_API("DATABASE_ID")
token_key = secret.notion_API("token_key")
NOTION_URL = 'https://api.notion.com/v1/databases/'
class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self,integration_token=token_key):
        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={"Authorization": token_key, "Notion-Version":'2021-05-13'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(self,data_json):
        most_properties = [len(data_json['results'][i]['properties'])
                                for i in range(len(data_json["results"]))]
        return list(data_json["results"][np.argmax(most_properties)]["properties"].keys())
    

    def get_projects_data(self,data_json,projects):
        projects_data = {}
        duration_temp = []        
        for p in projects:
            if "Related" in p:
                pass
            elif p !="To-do" and p != 'Duration':
                projects_data[p] = [data_json["results"][i]["properties"][p]["checkbox"]
                                    for i in range(len(data_json["results"]))]
            elif p=="To-do":
                names = [data['results'][i]['properties']['To-do']['title'][0]['text']['content']
                                    for i in range(len(data_json["results"]))]
            elif p=="Duration":
                for i in range(len(data_json["results"])):
                    try:
                        duration_temp.append(data['results'][i]['properties']['Duration']['number'])
                    except:
                        duration_temp.append(None)
                projects_data[p] = duration_temp

        # When everything is NULL, it causes KeyError
        try:
            projects_data['Duration']
        except KeyError:
            projects_data['Duration'] = [None]*len(names)

        return projects_data,names
    
    
    
    def MorningRoutine(self, projects_data, names):
        total_checked = []
        for i in range(len(names)):
            if names[i] == 'Meditation':
                meditation = projects_data['Duration'][i]
                meditation_checked = projects_data['Checkbox'][i]
                if meditation == None:
                    meditation = 0
            elif names[i] == 'Personal Reading':
                PR = projects_data['Duration'][i]
                reading_check = projects_data['Checkbox'][i]
                try:
                    if PR > 0:
                        reading = PR
                    else:
                        reading = 0
                except:
                    reading = 0
            elif names[i] == 'Rise Time & Phone Free (1hr)':
                rise_time = projects_data['Duration'][i]
                rise_time_check = projects_data['Checkbox'][i]
    
            elif names[i] == 'Phone Free Before Sleep (30 min)/ run (km)':
                run = projects_data['Duration'][i]
                before_sleep_check = projects_data['Checkbox'][i]
                if run == None:
                    run = 0
            elif names[i] == 'Morning Thoughts':
                morning_thoughts_check = projects_data['Checkbox'][i]
            elif names[i] == 'Push up':
                push_up_check = projects_data['Checkbox'][i]
                
            if projects_data['Checkbox'][i] == True:
                total_checked.append('Checked')
            
        total_checked = len(total_checked)
        
        return total_checked, meditation, rise_time, reading, run, \
            reading_check, rise_time_check, before_sleep_check, morning_thoughts_check, \
            push_up_check, meditation_checked
            
    def accru_morning_routine(self, projects_data, names):
        total_checked = nsync.MorningRoutine(projects_data, names)[0]
        meditation_min = nsync.MorningRoutine(projects_data, names)[1]
        rise_time_min = nsync.MorningRoutine(projects_data, names)[2]
        reading_min = nsync.MorningRoutine(projects_data, names)[3]
        run_km = nsync.MorningRoutine(projects_data, names)[4]
        reading_check = nsync.MorningRoutine(projects_data, names)[5]
        rise_time_check = nsync.MorningRoutine(projects_data, names)[6]
        before_sleep_check = nsync.MorningRoutine(projects_data, names)[7]
        morning_thoughts_check = nsync.MorningRoutine(projects_data, names)[8]
        push_up_check = nsync.MorningRoutine(projects_data, names)[9]
        meditation_check = nsync.MorningRoutine(projects_data, names)[10]
        date = datetime.today().strftime('%#m/%d/%Y')
        
        # Make a diction for a new row
        new_row = {'Date': date, 'total_checked': total_checked, 'before_sleep_check':before_sleep_check,
                   'rise_time_check': rise_time_check, 'meditation_min': meditation_min,
                   'meditation_check':meditation_check, 'rise_time_min':rise_time_min, 
                   'reading_check':reading_check, 'reading_min':reading_min,
                   'run_km':run_km, 'morning_thoughts_check':morning_thoughts_check,
                   'push_up_check':push_up_check}
        
        # Create a new data frame with above dict
        new_row = pd.DataFrame(data = new_row, index = [0])
        
        
        # Read csv file
        routine = pd.read_csv('C:\\NotionUpdate\progress\Connect_NotionAPI\morning_routine.csv',
                                  sep = ',', index_col = 0)
        # Reset index numbers (in order)
        try:
            routine = routine.reset_index()
        except:
            pass

        # Total checked in routine dataframe
        routine_total_checked = routine['total_checked'][len(routine['total_checked'])-1]
        
        # Compare "total_checked" and "routine_total_checked" to update the newest values

        if new_row['Date'][0] in list(routine['Date']) and total_checked <= routine_total_checked:
            pass
        else:
            if new_row['Date'][0] in list(routine['Date']) and total_checked > routine_total_checked:
                routine = routine.drop([routine.index[-1]])
            # Add the created row to existing csv file
            routine = pd.concat([routine, new_row], ignore_index = True, axis = 0)
            # Remove existing directory and Replace it with created dataframe
            os.remove('C:\\NotionUpdate\progress\Connect_NotionAPI\morning_routine.csv')
            # Save a csv file to replace the old one
            routine.to_csv('C:\\NotionUpdate\progress\Connect_NotionAPI\morning_routine.csv', encoding='utf-8')
            try:
                routine.to_csv('D:\Spring 2022\Project\morning_routine.csv')
            except:
                # This occurs when I don't have my usb plugged in
                pass



# Morning Routine
nsync = NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data,names = nsync.get_projects_data(data,projects)
nsync.accru_morning_routine(projects_data, names)









>>>>>>> 572dc86 (update)
