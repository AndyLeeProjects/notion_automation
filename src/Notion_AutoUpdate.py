# -*- coding: utf-8 -*-

import requests, json
import numpy as np
from datetime import datetime
import sys, os
import calendar
import pandas as pd
from datetime import time as time_time

# Direct to specified path to use the modules below
os.chdir(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from secret import secret
from myPackage import NotionUpdate_API as N_Update
from myPackage import change_background as cb
from myPackage import Monthly_Eval as pMon
from myPackage import Read_Data as NRD
from Notion_API import ConnectNotionDB as Connect_NotionAPI
from Google_API.calendar_automation import GoogleCalendarAPI as CalendarAPI

# Modify the data for git representation(Privacy reasons)
from myPackage import remove_names_git


class Connect_Notion:
    def __init__(self):
        # Get Token Key
        self.token_key = secret.notion_API("token_key")

        # Get Task Schedule Data -> task_data
        self.task_databaseId = secret.task_scheduleDB("database_id")
        TASK = Connect_NotionAPI(self.task_databaseId, self.token_key)
        self.task_data = TASK.retrieve_data()

        # Get Evaluation Data -> eval_data
        self.eval_databaseId = secret.evaluation_db("database_id")
        EVAL = Connect_NotionAPI(self.eval_databaseId, self.token_key)
        self.eval_data = EVAL.retrieve_data()

        # Get Duration Data -> dur_data
        self.duration_databaseId = secret.durationDB('database_id')
        DUR = Connect_NotionAPI(self.duration_databaseId, self.token_key)
        self.dur_data = DUR.retrieve_data()    

        self.headers = {
            "Authorization": "Bearer " + self.token_key,
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13"
        }
    
    # Overwrite the existing excel file with an updated data for duration_EST data & self-evaluation data
    def download_evaluationCSV(self):

        # String Manipulation to create file names
        date = self.eval_data['Date'][0].split('-')
        month = date[1]
        year = date[0][-2:]
        file_name = month + year + '.csv'
        
        print('\n****************** Update Evaluation CSV Data ******************')
        
        self.eval_data.to_csv("C:\\NotionUpdate\\progress\\notion_automation\\month_Data\\%s" % file_name, index=False)
        # Download to my D drive if plugged in 
        try:
            self.eval_data.to_csv("D:\\Personal\\progress\\notion_automation\\month_Data\\%s" % file_name, index=False)
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
    def updateTask_to_today(self, pageId):
        path = f"https://api.notion.com/v1/pages/{pageId}"
    
        updateData_to_next = {
            "properties": {
                "Status": {
                    "select": {
                                "name": "Today"
                        }
                    }        
                }
            }
        
        response = requests.request("PATCH", path, 
                                    headers=self.headers, data=json.dumps(updateData_to_next))
    
    # Update a block(task) from today's column to corresponding columns
    def updateTask_to_others(self, pageId, category):
        path = f"https://api.notion.com/v1/pages/{pageId}"
    
        updateData_to_waitlist = {
            "properties": {
                "Status": {
                    "select": {
                                "name": category
                        }
                    }        
                }
            }
        
        response = requests.request("PATCH", path, 
                                    headers=self.headers, data=json.dumps(updateData_to_waitlist))
    

    def createTask(self, task_name, task_duration):
        path = "https://api.notion.com/v1/pages"

        newPageData = {
            "parent": {"database_id": self.task_databaseId},
            "properties": {
                "Name": [
                    {"type": "text",
                    "text":{
                        "content": task_name
                    }}
                ],
                "Duration_EST": [
                    {"name": task_duration}
                ]
            }
        }

        response = requests.post(path, json=newPageData, headers=self.headers)

    def update_ScheduleCalendar(self):
        
        # Connect to Google Calendar API 
        CLIENT_SECRET_FILE = secret.GoogleCalendar_connect('credentials')
        calendarId = secret.GoogleCalendar_connect('calendarId')
        GoogleCal = CalendarAPI(CLIENT_SECRET_FILE = CLIENT_SECRET_FILE, calendar_id=calendarId)

        # Get today's tasks
        self.today_tasks = GoogleCal.execute_all("today_tasks")
        
        # Get all upcoming tasks
        self.upcoming_tasks = GoogleCal.execute_all("upcoming_tasks")

        # Sort the today's schedules that were created by me
        my_schedule = [self.today_tasks.index[i]
                        for i in range(len(self.today_tasks))
                        if calendarId ==  self.today_tasks['creator'].iloc[i]]
        my_schedule = self.today_tasks.loc[my_schedule]
        
        # Get Duration of each task
        for task in range(len(self.today_tasks['summary'])):
            start_time = self.today_tasks['start'].iloc[task].split('T')[1].split(':')
            start_hr = int(start_time[0])
            start_min = int(start_time[1])
            end_time = self.today_tasks['end'].iloc[task].split('T')[1].split(':')
            end_hr = int(end_time[0])
            end_min = int(end_time[1])

            # Get task name
            task_name = self.today_tasks['summary'].iloc[task]

            # Get task duration
            task_duration = (end_hr * 60 + end_min) - (start_hr * 60 + start_min)
            
            # convert the duration into -hr -min format
            if task_duration % 60 == 0:
                task_duration = f'{task_duration // 60}hr'
            elif task_duration < 60:
                task_duration = f'{task_duration % 60}min'
            else:
                task_duration = f'{task_duration // 60}hr {task_duration % 60}min'
            
            #self.createTask(task_name, task_duration)


    # Update Schedule
    def update_Schedule(self):
        today = CNotion.get_today("day")
        today_date = CNotion.get_today("date")
        weekday = CNotion.get_today("weekday")
        
        print("****************** Updating Today's Schedule ******************")

        # Set up progress bar variables
        l = len(self.task_data['Name'])
        #Connect_NotionAPI.printProgressBar(0, l, prefix = 'Task Update Progress: ', suffix = 'Complete')

        for block in range(len(self.task_data['Name'])):
            
            # If it's past 1:00 pm, don't reschedule it again
            ## Fix any changes made to the automated schedule
            if CNotion.is_time_between(time_time(13,00),time_time(2,00)) == True:
               print('\n\n')
               return self.task_data['Status'].value_counts()["Today"]
            
            
            # Check if today(Mon,Tue,...,Sun) matches the block's day
                # 3 CASES that requires adjustment
                    # CASE 1: the block is NOT in Today column when it should be (Days)
                    # CASE 2: the block is in Today column wht it should NOT be  (Days)
                    # CASE 3: the block is NOT in Today column when it should be (Date)
                    
            
            # Check CASE 1
            block_dates = self.task_data["Date"].iloc[block]
            
            # np.nan is passed as float, so change it into a string.
            if isinstance(block_dates, float):
                block_dates = str(block_dates)

            if today in block_dates or weekday in block_dates or "Everyday" in block_dates:
                if self.task_data["Status"].iloc[block] != "Today":
                    CNotion.updateTask_to_today(self.task_data["pageId"].iloc[block])
                    print("[%s] Block Updated" % self.task_data["Name"].iloc[block])

            # Check CASE 2
            # If the block is incorrectly in Today's column send it back to its category(column)
            else:
                # disposable blocks(Used for one day: popped up meeting or laundry etc.)
                if self.task_data['Date'].iloc[block] == [] and self.task_data['Due Date'].iloc[block] == 0:
                    pass
                
                elif self.task_data["Status"].iloc[block] == "Today" and today_date != self.task_data["Due Date"].iloc[block]:
                    CNotion.updateTask_to_others(self.task_data["pageId"].iloc[block],
                                                 self.task_data["Status"].iloc[block])
                    print("[%s] Block Updated" % self.task_data["Name"].iloc[block])
            
            # Check CASE 3
            if today_date == self.task_data["Due Date"].iloc[block]:
                if self.task_data["Status"].iloc[block] != "Today":
                    CNotion.updateTask_to_today(self.task_data["pageId"].iloc[block])
                    print("[%s] Block Updated" % self.task_data["Name"].iloc[block])
            
            #Connect_NotionAPI.printProgressBar(block + 1, l, prefix = 'Task Update Progress: ', suffix = 'Complete')
        
        print("\nUpdate Completed\n\n\n\n")
        
        # Return the total number of today's todo lists
        return self.task_data['Status'].value_counts()['Today']
    
                
    
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
        print('Upload Completed\n\n\n\n')
        
        # Save to D Drive (if plugged in) for further statistical analysis
        RDATA = NRD.read_data()
        all_dat = RDATA.all_data("include date")[0]
        RDATA.save_to_Ddrive(all_dat)
        # Save another img with update_window == False in the D drive
        pMon.monthly_eval(projects_data_eval, update_window = False) 


    def is_time_between(self, begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.now().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else: # crosses midnight
            return check_time >= begin_time or check_time <= end_time
    
    def execute_all(self):
        # Update Schedule
        self.update_Schedule()
        ##### Update Duration DB #####
        import notion_durationDB 

        # Download the evaluation data
        self.download_evaluationCSV()

        # Upload Evaluation Visualization 
        self.update_evaluationJPG()


# Schedule my tasks 
CNotion = Connect_Notion()
CNotion.execute_all()
CNotion.update_ScheduleCalendar()










        
        
        
