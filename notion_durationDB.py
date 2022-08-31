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
if os.name == 'posix':
    sys.path.append('/Users/andylee/Desktop/git_prepFile/notion_automation')
    duration_path1 = r'/Users/andylee/Desktop/git_prepFile/notion_automation/Data/duration_est.csv'
else:
    sys.path.append('C:\\NotionUpdate\\progress\\notion_automation')
    duration_path1 = r'C:\NotionUpdate\progress\notion_automation\Data\duration_est.csv'
    duration_path2 = r'D:\Personal\progress\notion_automation\Data\duration_est.csv'
from secret import secret
from myPackage import organize_evaluation_data as oed
from myPackage import Monthly_Eval as pMon
from myPackage import Read_Data as NRD
from datetime import time as time_time
from datetime import timedelta
import Notion_API as N_API


class Connect_Notion:
    def __init__(self):

        self.token_key = secret.notion_API("token_key")

        # Get Task Schedule Data -> task_data
        self.task_databaseId = secret.task_scheduleDB("database_id")
        TASK = N_API.ConnectNotionDB(self.task_databaseId, self.token_key)
        self.task_data = TASK.retrieve_data()

        # Get Duration Data -> dur_data
        self.duration_databaseId = secret.durationDB('database_id')
        DUR = N_API.ConnectNotionDB(self.duration_databaseId, self.token_key)
        self.dur_data = DUR.retrieve_data()    
        self.headers = {
            "Authorization": "Bearer " + self.token_key,
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13"
        }

                    
    def updateDuration_EST(self, pageId, duration):
        updateUrl_to_waitlist = f"https://api.notion.com/v1/pages/{pageId}"
    
        updateDuration_EST = {
            "properties": {
                "Duration_EST": {
                    "rich_text":[{
                        "text":{
                            "content":duration    
                        }
                    }]
                }        
            }
        }
        
        
        response = requests.request("PATCH", updateUrl_to_waitlist, 
                                    headers=self.headers, data=json.dumps(updateDuration_EST)) 

    def updateDuration_Tasks(self, pageId, tasks):
        updateUrl_to_waitlist = f"https://api.notion.com/v1/pages/{pageId}"
    
        updateDuration_Tasks = {
            "properties": {
                "D_Tasks": {
                    "number": tasks
                }        
            }
        }
        
        
        response = requests.request("PATCH", updateUrl_to_waitlist, 
                                    headers=self.headers, data=json.dumps(updateDuration_Tasks)) 

    
    def get_DurationTime_EST(self):
        print('****************** Updating Duration Database ******************')
        # Get 3 values
            # 1. Total Task Duration EST   AND   Total num of Tasks
            # 2. Finished Task Druation    AND   Total num of Finished Tasks
            # 3. Remaining Task Duration   AND   Total num of Remaining Tasks
        
        tot_durationEST = 0
        tot_numTasks = []
        fin_durationEST = 0
        fin_numTasks = []
        rem_durationEST = 0
        rem_numTasks = []
        print("Calculating Durations...")
        for task in range(len(self.task_data['To do'])):
            
            # Since the duration_EST comes in as "-hr -min", it needs to be manipulated
            task_duration = str(self.task_data['Duration_EST'][task])

            ## Also, if Duration_EST is empty, it is passed as np.nan (float). This case, convert it 
            ## to a 0.
            
            # Case1: -min
            if 'hr' not in task_duration and 'min' in task_duration:
                task_duration = int(task_duration.strip('min'))
            
            # Case2: -hr
            elif 'hr' in task_duration and 'min' not in task_duration:
                task_duration = int(task_duration.strip('hr')) * 60
            
            # Case3: -hr -min
            elif 'hr' in task_duration and 'min' in task_duration:
                # Get hour & minutes separately
                hour, minutes = task_duration.split(' ')
                hour = int(hour.strip('hr'))
                minutes = int(minutes.strip('min'))

                # Get the total duration estimates in minutes
                task_duration = hour * 60 + minutes
            
            else:
                task_duration = 0


            task_status = self.task_data['To do'][task]
            
            # Only look at Today's Column 
            if self.task_data['Status'][task] == "Today":
                tot_durationEST += task_duration
                tot_numTasks.append(task)
                
                # If task is Finished
                if task_status == True:
                    fin_durationEST += task_duration
                    fin_numTasks.append(task)
                    
                # If task is NOT Finished
                else:
                    rem_durationEST += task_duration
                    rem_numTasks.append(task)
        
        # Change Duration EST values into easier []hr []min format
        tot_durationEST = "%dhr %dmin" % (tot_durationEST // 60, tot_durationEST % 60)
        fin_durationEST = "%dhr %dmin" % (fin_durationEST // 60, fin_durationEST % 60)
        rem_durationEST = "%dhr %dmin" % (rem_durationEST // 60, rem_durationEST % 60)
        
        # Make it into a dictionary for convenience
        self.duration_dic = {'tot_durationEST':tot_durationEST,
                        'tot_numTasks':len(tot_numTasks),
                        'fin_durationEST':fin_durationEST,
                        'fin_numTasks':len(fin_numTasks),
                        'rem_durationEST':rem_durationEST,
                        'rem_numTasks':len(rem_numTasks)}
    
    def update_DurationDB(self):
        print("Uploading to Duration DB...")
        # Update Total, Finished, Remaining Durations & Tasks for Today
        for row in range(3):
            if self.dur_data['D_Title'][row] == "Total Work Hours EST":
                CNotion.updateDuration_EST(self.dur_data['pageId'][row],  
                                           self.duration_dic['tot_durationEST'])
                CNotion.updateDuration_Tasks(self.dur_data['pageId'][row], 
                                           self.duration_dic['tot_numTasks'])     
                
            elif self.dur_data['D_Title'][row] == "Total Work Hours Finished":
                CNotion.updateDuration_EST(self.dur_data['pageId'][row], 
                                           self.duration_dic['fin_durationEST'])        
                CNotion.updateDuration_Tasks(self.dur_data['pageId'][row], 
                                           self.duration_dic['fin_numTasks'])        
            else:
                CNotion.updateDuration_EST(self.dur_data['pageId'][row], 
                                           self.duration_dic['rem_durationEST'])        
                CNotion.updateDuration_Tasks(self.dur_data['pageId'][row], 
                                           self.duration_dic['rem_numTasks'])       
        print('Update Completed\n\n\n\n')
                
    def update_durationCSV(self):
        # ADD Duration variables(For further statistical analysis)
        new_row = pd.DataFrame(self.duration_dic, index = [0])
        today = datetime.today()
        if CNotion.is_time_between(time_time(00,00),time_time(1,59)) == True:
            today = today - timedelta(days=1)
        else:
            pass
        today_date = today.strftime("%m/%d/%Y")

        duration_df = pd.read_csv(duration_path1,
                                  sep = ',', index_col = 0)

        new_row['Date'] = today_date
            

        if new_row['Date'][0] in list(duration_df['Date']):
            
            if new_row['fin_numTasks'][0] <= duration_df['fin_numTasks'][0]:
                pass
            else:
                if new_row['Date'][0] in list(duration_df['Date']) and new_row['fin_numTasks'][0] > duration_df['fin_numTasks'][0]:
                    duration_df = duration_df.drop([duration_df.index[-1]])
                    duration_df = pd.concat([duration_df, new_row], ignore_index = True, axis = 0)
                    
                    duration_df.to_csv(duration_path1)
        else:
            duration_df = pd.concat([duration_df, new_row], ignore_index = True, axis = 0)
            duration_df.to_csv(duration_path1)
            
        
        try:
            duration_df.to_csv(duration_path2)
        except:
            pass

    def is_time_between(self, begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.now().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else: # crosses midnight
            return check_time >= begin_time or check_time <= end_time
    
    def execute_all(self):
        # Update Total Duration Estimate Database
        self.get_DurationTime_EST()

        # Update Duration Database
        self.update_DurationDB()

        # Update duration_est.csvs
        self.update_durationCSV()

    

            
        
print('Updating Duration Database...')

CNotion = Connect_Notion()
CNotion.execute_all()








        
        
        
        