# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 13:30:44 2021

@author: anddy
"""

import requests, sys
import numpy as np
from datetime import datetime, timedelta, time

sys.path.append('C:\\NotionUpdate\\progress\\notion_automation')
from secret import secret
import pandas as pd
import os
import mysql.connector as MC



class NotionSync:
    def __init__(self, database_id, token_key):
        import Notion_API as Notion
        self.database_id = database_id
        self.token_key = token_key    
        
        Notion = Notion.ConnectNotionDB(self.database_id, self.token_key)
        self.data = Notion.retrieve_data()
        self.titles = list(self.data.keys())


    def accru_morning_routine(self):
        # Connect to MySQL DB (Self_Evaluation)
        db = MC.connect(
            host="localhost",
            user="root",
            passwd=secret.self_evaluation_DB("pwd"),
            database="Self_Evaluation"
            )
        mycursor = db.cursor()

        total_checked = len([i for i in self.data['Checkbox'] if i == True])

        reading_check = str(list(self.data[self.data['To-do'] == 'Personal Reading']['Checkbox'])[0])

        rise_time_check = str(list(self.data[self.data['To-do'] == 'Rise Time & Phone Free (1hr)']['Checkbox'])[0])
        before_sleep_check = str(list(self.data[self.data['To-do'] == 'Phone Free Before Sleep (30 min)/ run (km)']['Checkbox'])[0])
        morning_thoughts_check = str(list(self.data[self.data['To-do'] == 'Morning Thoughts']['Checkbox'])[0])
        push_up_check = str(list(self.data[self.data['To-do'] == 'Push up']['Checkbox'])[0])
        meditation_check = str(list(self.data[self.data['To-do'] == 'Meditation']['Checkbox'])[0])

        # If the time is between midnight and 2 AM, still register it as the day before 
        today = datetime.today()
        if NotionSync.is_time_between(time(00,00),time(1,59)) == True:
            today = today - timedelta(days=1)
        else:
            pass
        today_date = today.strftime("%#m/%d/%Y")

        # Make a diction for a new row
        new_row = {'Date': today_date, 'total_checked': total_checked, 'before_sleep_check':before_sleep_check,
                   'rise_time_check': rise_time_check, 'meditation_check':meditation_check,
                   'reading_check':reading_check, 'morning_thoughts_check':morning_thoughts_check,
                   'push_up_check':push_up_check}
        
        # Create a new data frame with above dict
        new_row = pd.DataFrame(data = new_row, index = [0])
        new_row['Date'] = new_row['Date'].astype('datetime64[ns]')
        
        # Read csv file
        routine = pd.read_csv(r'C:\NotionUpdate\progress\notion_automation\Data\morning_routine.csv', sep = ',', index_col = 0)
        routine['Date'] = routine['Date'].astype('datetime64[ns]')
        
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
        elif NotionSync.is_time_between(time(6,00),time(11,59)) == True:
                # Drop the last index & add the new row
                routine = routine.drop([routine.index[-1]])
                routine = pd.concat([routine, new_row], ignore_index = True, axis = 0)
                routine.to_csv(r'C:\NotionUpdate\progress\notion_automation\Data\morning_routine.csv', encoding='utf-8')
        else:
            if new_row['Date'][0] in list(routine['Date']) and total_checked > routine_total_checked:
                routine = routine.drop([routine.index[-1]])
            # Add the created row to existing csv file
            routine = pd.concat([routine, new_row], ignore_index = True, axis = 0)
            # Remove existing directory and Replace it with created dataframe
            os.remove(r'C:\NotionUpdate\progress\notion_automation\Data\morning_routine.csv')
            # Save a csv file to replace the old one
            routine.to_csv(r'C:\NotionUpdate\progress\notion_automation\Data\morning_routine.csv', encoding='utf-8')
            try:            
                routine.to_csv(r'D:\Spring 2022\Project\morning_routine.csv')
                routine.to_csv(r'D:\Personal\progress\Data\morning_routine.csv')
                routine.to_csv(r'D:\Personal\progress\notion_automation\Data\morning_routine.csv')

            except:
                # This occurs when I don't have my usb plugged in
                pass

    def is_time_between(begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.now().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else: # crosses midnight
            return check_time >= begin_time or check_time <= end_time
    
    def execute_all(self):
        self.accru_morning_routine()




# Morning Routine
database_id = secret.notion_API("database_id")
token_key = secret.notion_API("token_key")

nsync = NotionSync(database_id, token_key)
nsync.execute_all()








