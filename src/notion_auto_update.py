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
#sys.path.append(r"c:\NotionUpdate\progress\notion_automation")

from secret import secret
from myPackage import NotionUpdate_API as N_Update
from myPackage import change_background as cb
from myPackage import Monthly_Eval as pMon
from myPackage import Read_Data as NRD
from connect_notion import ConnectNotionDB as Connect_NotionAPI
from update_notion import * # Update_Notion & create_today_task
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
    def download_evaluation_csv(self):

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
        
    def update_schedule_calendar(self):
        # Connect to Google Calendar API 
        CLIENT_SECRET_FILE = secret.GoogleCalendar_connect('credentials')
        calendarId = secret.GoogleCalendar_connect('calendarId')
        GoogleCal = CalendarAPI(CLIENT_SECRET_FILE = CLIENT_SECRET_FILE, calendar_id=calendarId)

        # Get today's tasks
        self.today_tasks_Google = GoogleCal.execute_all("today_tasks")
        
        # Get all upcoming tasks
        self.upcoming_tasks_Google = GoogleCal.execute_all("upcoming_tasks")

        # Sort the today's schedules that were created by me (matched by email)
        my_schedule = [self.today_tasks_Google.index[i]
                        for i in range(len(self.today_tasks_Google))
                        if calendarId ==  self.today_tasks_Google['creator'].iloc[i]]
        my_schedule = self.today_tasks_Google.loc[my_schedule]

        # In the case of redundant tasks, accumulate the total duration
        task_duration_Google = {}

        # Get Duration of each task that were created by "me"
        for task in range(len(self.today_tasks_Google)):
            start_time = self.today_tasks_Google['start'].iloc[task].split('T')[1].split(':')
            start_hr = int(start_time[0])
            start_min = int(start_time[1])
            end_time = self.today_tasks_Google['end'].iloc[task].split('T')[1].split(':')
            end_hr = int(end_time[0])
            end_min = int(end_time[1])

            # Get task name
            task_name_Google = self.today_tasks_Google['summary'].iloc[task]

            # Personal Filter
            if "Andy Lee and" in task_name_Google:
                task_name_Google = task_name_Google.replace(" | Other", "")
                task_name_Google = task_name_Google.replace("Andy Lee and ", "Pathrise: Meeting with ")

            # Get task duration
            task_duration = (end_hr * 60 + end_min) - (start_hr * 60 + start_min)

            # Accumulate Duration (in case of redundancy of schedules)
            try:
                task_duration_Google[task_name_Google] += task_duration
            except KeyError:
                task_duration_Google[task_name_Google] = task_duration

            # Redefine below variables for the simplicity
            task_duration = task_duration_Google[task_name_Google]
            task_status = self.today_tasks_Google['attendees'].iloc[task]
            timesort = int(start_time[0] + start_time[1]) # timesort is used to sort the database in order in Notion
            if int(start_time[0]) // 12 == 0:
                start_time = start_time[0] + ":" + start_time[1] + " am"
            else:
                start_time = str(int(start_time[0])% 12) + ":" + start_time[1] + " pm"
            
            meeting_url = self.today_tasks_Google['conferenceData'].iloc[task]

            # convert the duration into -hr -min format
            if task_duration % 60 == 0:
                task_duration = f'{task_duration // 60}hr'
            elif task_duration < 60:
                task_duration = f'{task_duration % 60}min'
            else:
                task_duration = f'{task_duration // 60}hr {task_duration % 60}min'
            # If the task name exists in the Notion Task DB, then Update
            ## Else, create a new task
            ## --> If the time is between 12:00am and 4:00am, no updates needed
            if self.is_time_between(time_time(23,59),time_time(4,00)) == False:

                # Case where the task in Google Calendar is ALREADY IN the Notion Task DB
                ## Modify the total duration EST
                if task_name_Google in list(self.task_data['Name']):
                    
                    if str(meeting_url) != str(np.nan):
                        # Change the Duration_EST (to task_duration) & Starting Time (to start_time) & timesort & URL
                        update_notion({"Duration_EST": {"select":{"name":task_duration}}, 
                                    "Time": {"rich_text": [{"type": "text", "text": {"content": "Time: "}, "annotations":{"bold":True}},
                                                           {"type": "text", "text": {"content": start_time}}]},
                                    "timesort": {"number": timesort},
                                    "web 1": {"url": meeting_url}}, 
                                    self.task_data[self.task_data['Name'] == task_name_Google]['pageId'].iloc[0], headers = self.headers)
                    else:
                        # Change the Duration_EST (to task_duration) & Starting Time (to start_time) & timesort
                        update_notion({"Duration_EST": {"select":{"name":task_duration}}, 
                                       "Time": {"rich_text": [{"type": "text", "text": {"content": "Time: "}, "annotations":{"bold":True}},
                                                           {"type": "text", "text": {"content": start_time}}]},
                                       "timesort": {"number": timesort}}, 
                                    self.task_data[self.task_data['Name'] == task_name_Google]['pageId'].iloc[0], headers = self.headers)
                    print("<", task_name_Google,", ", task_duration, ">  Updated")
                    print()
                # Case where the task in Google Calendar is NOT IN the Notion Task DB
                ## Create a new task in Notion Task DB
                ### status shows my confirm status on the schedule
                elif task_status == "accepted" or str(task_status) == str(np.nan):
                    create_today_task(task_name_Google, task_duration, self.task_databaseId, start_time,
                                    meeting_url, timesort,  self.headers)
                    print("<", task_name_Google,", ", task_duration, ">  Created")
                    print()

    # Update Schedule
    def update_Schedule(self):
        today = self.get_today("day")
        today_date = self.get_today("date")
        weekday = self.get_today("weekday")
        
        print("****************** Updating Today's Schedule ******************")

        for block in range(len(self.task_data['Name'])):
            
            # If it's past 1:00 pm, don't reschedule it again
            ## Fix any changes made to the automated schedule
            if self.is_time_between(time_time(13,00),time_time(2,00)) == True:
               print('\n\n')
               return self.task_data['Status'].value_counts()["Today"]
            
            
            # Check if today(Mon,Tue,...,Sun) matches the block's day
                # 3 CASES that requires adjustment
                    # CASE 1: the block is NOT in Today column when it should be (Days)
                    # CASE 2: the block is in Today column wht it should NOT be  (Days)
                    # CASE 3: the block is NOT in Today column when it should be (Date)
                    
            
            # Check CASE 1
            # In the case block_dates is np.nan, change the type to str (from float)
            ## block_dates example: ['Wed', 'Thur', 'Sat', 'Sun']
            block_dates = self.task_data["Date"].iloc[block]
            
            # np.nan is passed as float, so change it into a string.
            if isinstance(block_dates, float):
                block_dates = str(block_dates)

            if today in block_dates or weekday in block_dates or "Everyday" in block_dates:
                if self.task_data["Status"].iloc[block] != "Today":
                    update_notion({"Status":{"select": {"name": "Today"}}} , self.task_data["pageId"].iloc[block], self.headers)
                    print("[%s] Block Updated" % self.task_data["Name"].iloc[block])

            # Check CASE 2
            # If the block is incorrectly in Today's column send it back to its category(column)
            else:
                # disposable blocks(Used for one day: popped up meeting or laundry etc.)
                if str(self.task_data['Date'].iloc[block]) == str(np.nan) and str(self.task_data['Due Date'].iloc[block]) == str(np.nan):
                    pass
                
                # Send them back to its own category 
                ## Code to get the Category Name --> self.task_data["Name"].iloc[block].split(':')[0]
                elif self.task_data["Status"].iloc[block] == "Today" and today_date != self.task_data["Due Date"].iloc[block] and \
                    today not in block_dates:
                    update_notion({"Status":{"select": {"name": self.task_data["Name"].iloc[block].split(':')[0]}}} , self.task_data["pageId"].iloc[block], self.headers)
                    print("[%s] Block Updated" % self.task_data["Name"].iloc[block])
            
            # Check CASE 3
            if today_date == self.task_data["Due Date"].iloc[block]:
                if self.task_data["Status"].iloc[block] != "Today":
                    update_notion({"Status": {"select": {"name": "Today"}}} , self.task_data["pageId"].iloc[block], self.headers)
                    print("[%s] Block Updated" % self.task_data["Name"].iloc[block])
            
        
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

        # Updates & Creates Tasks from Google Calendar API
        self.update_schedule_calendar()

        ##### Update Duration DB #####
        import notion_duration_db 

        if self.is_time_between(time_time(21,1),time_time(2,00)) == True or \
           self.is_time_between(time_time(7,00),time_time(11,00)) == True:
            # Download the evaluation data
            self.download_evaluation_csv()

            # Upload Evaluation Visualization 
            self.update_evaluationJPG()


# Schedule my tasks 
CNotion = Connect_Notion()
CNotion.execute_all()










        
        
        
