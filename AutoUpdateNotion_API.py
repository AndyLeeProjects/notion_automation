# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 00:48:06 2022

@author: anddy
"""
import requests, json
import numpy as np
from datetime import datetime
import sys, os
import calendar
import pandas as pd
from datetime import time as time_time

if os.name == 'posix':
    sys.path.append('/Users/andylee/Desktop/git_prepFile/notion_automation')
else:
    sys.path.append('C:\\NotionUpdate\\progress\\notion_automation')
from secret import secret
from myPackage import organize_evaluation_data as oed
from myPackage import NotionUpdate_API as N_Update
from myPackage import change_background as cb
from myPackage import Monthly_Eval as pMon
from myPackage import Read_Data as NRD
import Notion_API as N_API

# Modify the data for git representation(Privacy reasons)
from myPackage import remove_names_git



class Connect_Notion:
    def __init__(self):
        # Get Token Key
        self.token_key = secret.notion_API("token_key")


        # Get Task Schedule Data -> task_data
        self.task_databaseId = secret.task_scheduleDB("database_id")
        self.task_data = N_API.ConnectNotionDB(self.eval_databaseId, self.token_key)

        # Get Evaluation Data -> eval_data
        self.eval_databaseId = secret.evaluation_db("database_id")
        self.eval_data = N_API.ConnectNotionDB(self.duration_databaseId, self.token_key)
        
        # Get Duration Data -> dur_data
        self.duration_databaseId = secret.durationDB('databaseId')
        self.dur_data = N_API.ConnectNotionDB(self.task_databaseId, self.token_key)
    
    # Get Evaluation Data from a separate database 
    def get_evaluation_data(self, data, projects):
        projects.pop(-1)        
        eval_data = oed.get_evaluation_data(projects, data)
        return eval_data
    
    
    # Overwrite the existing excel file with an updated data for duration_EST data & self-evaluation data
    def download_evaluationCSV(self, eval_data):
        date = eval_data['Date'][0].split('/')
        month = date[0]
        year = date[-1][-2:]
        file_name = month + year + '.csv'
        
        print('\n****************** Update Evaluation CSV Data ******************')
        
        eval_data.to_csv("C:\\NotionUpdate\\progress\\notion_automation\\month_Data\\%s" % file_name, index=False)
        # Download to my D drive if plugged in 
        try:
            eval_data.to_csv("D:\\Personal\\progress\\notion_automation\\month_Data\\%s" % file_name, index=False)
        except:
            pass
        print('Update Completed\n\n\n\n')
            
        
    def get_today(self, key):
        # Get today's date
        week_days = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
        year = int(datetime.today().strftime('%Y'))
        month = int(datetime.today().strftime('%m'))
        day = int(datetime.today().strftime('%d'))
        week_day_num = calendar.weekday(year,month,day)
        today = week_days[week_day_num]
        
        now = datetime.today()
        dt_string = now.strftime("%Y-%m-%d")
        
        # Determine if today is weekday
        if week_day_num > 4:
            weekday = 'Weekend'
        else:
            weekday = 'Weekday'
        
        if key == "day":
            return today
        elif key == "weekday":
            return weekday
        else:
            return dt_string
        
    
    # Update a block(task) to today's column
    def updateTask_to_today(self, pageId, headers):
        path = f"https://api.notion.com/v1/pages/{pageId}"
    
        updateData_to_next = {
            "properties": {
                "Status 1": {
                    "select": {
                                "name": "Today"
                        }
                    }        
                }
            }
        
        response = requests.request("PATCH", path, 
                                    headers=headers, data=json.dumps(updateData_to_next))
    
    # Update a block(task) from today's column to corresponding columns
    def updateTask_to_others(self, pageId, headers, category):
        path = f"https://api.notion.com/v1/pages/{pageId}"
    
        updateData_to_waitlist = {
            "properties": {
                "Status 1": {
                    "select": {
                                "name": category
                        }
                    }        
                }
            }
        
        response = requests.request("PATCH", path, 
                                    headers=headers, data=json.dumps(updateData_to_waitlist))
    


    # Update Schedule
    def update_Schedule(self, proj_data):
        today = CNotion.get_today("day")
        today_date = CNotion.get_today("date")
        weekday = CNotion.get_today("weekday")
        
        print("****************** Updating Today's Schedule ******************")
        for block in range(len(proj_data['Name'])):
            
            # If it's past 1:00 pm, don't reschedule it again
                # Since I may have made some modifications, which needs to be fixed
            if CNotion.is_time_between(time_time(13,00),time_time(2,00)) == True:
                return proj_data['Category_current'].count("Today")
            
            
            # Check if today(Mon,Tue,...,Sun) matches the block's day
                # 3 CASES that requires adjustment
                    # CASE 1: the block is NOT in Today column when it should be (Days)
                    # CASE 2: the block is in Today column wht it should NOT be  (Days)
                    # CASE 3: the block is NOT in Today column when it should be (Date)
                    
            
            # Check CASE 1
            block_dates = proj_data["Date"][block]
            if today in block_dates or weekday in block_dates or "Everyday" in block_dates:
                if proj_data["Category_current"][block] != "Today":
                    CNotion.updateTask_to_today(proj_data["pageId"][block], headers)
                    print("[%s] Block Updated" % proj_data["Name"][block])

            # Check CASE 2
            # If the block is incorrectly in Today's column send it back to its category(column)
            else:
                # disposable blocks(Used for one day: popped up meeting or laundry etc.)
                if proj_data['Date'][block] == [] and proj_data['Due Date'][block] == 0:
                    pass
                
                elif proj_data["Category_current"][block] == "Today" and today_date != proj_data["Due Date"][block]:
                    CNotion.updateTask_to_others(proj_data["pageId"][block], headers,
                                                 proj_data["Category"][block])
                    print("[%s] Block Updated" % proj_data["Name"][block])
            
            # Check CASE 3
            if today_date == proj_data["Due Date"][block]:
                if proj_data["Category_current"] != "Today":
                    CNotion.updateTask_to_today(proj_data["pageId"][block], headers)
                    print("[%s] Block Updated" % proj_data["Name"][block])
        
        print("\nUpdate Completed\n\n\n\n")
        
        # Return the total number of today's todo lists
        return proj_data['Category_current'].count("Today")
    
                
    
    def update_evaluationJPG(self):
        print("****************** Uploading evaluation.jpg file ******************")
        data_eval = N_Update.nsync.query_databases()
        projects_eval = N_Update.nsync.get_projects_titles(data_eval)
        projects_data_eval = pd.DataFrame(N_Update.nsync.get_projects_data(data_eval,projects_eval))
        projects_data_eval = projects_data_eval.rename(
            columns={'*Finished': 'Finished', '*Multiple (1~5)': 'Multiple','*Phone pickups':'Phone pickups',
                    '*Screen time':'Screen time','Drink (%)':'Drink %', 'Drink? (over 3 beer)':'Drink',
                    'Meditation (%)':'Meditation %', 'Meditation (min)':'Meditation', 'Multiple (%)':'Multiple %',
                    'Pick up (%)':'Pick up %', 'Reading (%)':'Reading %', 'Rise time (%)':'Rise time %',
                    'Run (%)':'Run %', 'Run (km)':'Run', 'Screen Time (%)':'Screen Time %', 'Work done (%)': 'Work done %',
                    'Overall Satisfaction':'Satisfaction','Personal Reading':'Reading','Tech Consumption':'Tech',
                    'Total To-do List':'Tot To-do', 'Phone pickups':'Pickups'})

        # Monthly Evaluation Plot
        pMon.monthly_eval(projects_data_eval, update_window = True) # Replace it with projects_data_eval
        if os.name != 'posix':
            cb.update_Background() # Change the windows background with the self-evaluation IMG 
        #N_Update.uploadEvaluationJPG()
        print('Upload Completed\n\n\n\n')
        
        # Save to D Drive (if plugged in) for further statistical analysis
        RDATA = NRD.read_data()
        all_dat = RDATA.all_data("include date")[0]
        RDATA.save_to_Ddrive(all_dat)


        
    
    def is_time_between(self, begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.now().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else: # crosses midnight
            return check_time >= begin_time or check_time <= end_time
    


# Schedule my tasks 
CNotion = Connect_Notion()
proj_data = CNotion.connect_DB("Task Database")

# Update Schedule
CNotion.update_Schedule(proj_data)

# Read Evaluation Database in Notion using different database ID

CNotion = Connect_Notion()
data = CNotion.read_Database(databaseId, headers)
projects = CNotion.get_projects_titles(data, "Task Database")
eval_data = CNotion.get_evaluation_data(data, projects)

# Update Total Duration Estimate Database
# Reconnect to get updated database

CNotion = Connect_Notion()
proj_data = CNotion.connect_DB("Task Database")

##### Update Duration DB #####
import notion_durationDB     #
##############################

# Download the evaluation data
CNotion.download_evaluationCSV(eval_data)

# Upload Evaluation Visualization 
CNotion.update_evaluationJPG()


# Update Visualization for monthly evaluation (D Drive)
try:
    if os.name == 'posix':
        sys.path.append(r'/Volumes/Programming/Personal/progress')
    else:
        sys.path.append(r'D:\Personal\progress\notion_automation')
    print("****************** Uploading evaluation.jpg file ******************")
    mon = pRd.read_data()
    cur_month = datetime.now().month
    cur_year = int(datetime.now().strftime('%y'))
    month = mon.monthly(cur_month, cur_year)
    pMon.monthly_eval(month)
    print("\nD drive evaluation JPG file Updated\n\n")
except:
    pass








        
        
        
        