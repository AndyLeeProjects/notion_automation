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
    sys.path.append('C:\\NotionUpdate\\progress')
    duration_path1 = r'C:\NotionUpdate\progress\notion_automation\Data\duration_est.csv'
    duration_path2 = r'D:\Personal\progress\notion_automation\Data\duration_est.csv'
from secret import secret
from myPackage import organize_evaluation_data as oed
#from Connect_NotionAPI import NotionUpdate_API as NAPI
from myPackage import Monthly_Eval as pMon
from myPackage import Read_Data as NRD
from datetime import time as time_time
from datetime import timedelta


class Connect_Notion:
    def __init__(self):
        pass    
    
    # Retrieve Database from Notion
    def read_Database(self, databaseId, headers):
        readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"
    
        res = requests.request("POST", readUrl, headers=headers)
        data = res.json()
        # print(res.text)
    
        with open('./db.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        return data
    
    
    # Organize & Convert JSON format into dictionary
    def get_projects_titles(self,data_json, database_name):
        most_properties = [len(data_json['results'][i]['properties'])
                                for i in range(len(data_json["results"]))]
        
        project_keys = list(data_json["results"][np.argmax(most_properties)]["properties"].keys()) 
        
        
        # When the database is Empty, the variable title will not be read.
        # Thus, we need to make sure every varaible title is in our projects_key list
        if database_name == "Task Database":
            # since we are using 2 different data sets for the same code
            if "Due Date" not in project_keys and "Meditation (%)" not in project_keys:
                return project_keys + ["Due Date","pageId"]
            else:
                return project_keys + ["pageId"]
        else:
            project_keys = project_keys + ['pageId']
            if 'Duration_EST' not in project_keys:
                return project_keys + ["Duration_EST"]
            elif 'D_Tasks' not in project_keys:
                return project_keys + ['D_tasks']
            else:
                return project_keys + ["Duration_EST", "D_tasks"]
    
    def get_projects_data(self, data, projects):
        proj_data = {}
        
        for p in projects:                
            
            if p == "pageId":
                proj_data[p] = [data['results'][i]['id']
                                    for i in range(len(data["results"]))]
            
            elif p == "To do":
                proj_data[p] = [data['results'][i]['properties']['To do']['checkbox']
                                    for i in range(len(data["results"]))]
            
            elif p == "Name":
                names = []
                for i in range(len(data["results"])):
                    try:
                        names.append(data['results'][i]['properties']['Name']['title'][0]['text']['content'].split(': ')[1])
                    except:
                        names.append(data['results'][i]['properties']['Name']['title'][0]['text']['content'])
                proj_data["Name"] = names
                proj_data["Category"] = [data['results'][i]['properties']['Name']['title'][0]['text']['content'].split(': ')[0]
                                    for i in range(len(data["results"]))]
                proj_data["Category_current"] = [data['results'][i]['properties']['Status 1']['select']['name']
                                    for i in range(len(data["results"]))]
            
            elif p == "D_Title":
                proj_data[p] = [data['results'][i]['properties'][p]['title'][0]['plain_text']
                                    for i in range(len(data["results"]))]
            
            elif p == "D_Tasks":
                task_temp = []
                for i in range(len(data["results"])):
                    task_temp.append(data['results'][i]['properties'][p]['number'])
                proj_data[p] = task_temp 
                                    
            # Organize the duration data for each task/ block
                # the data is recorded as '1hr' or '30min' so we need to unify them into minute elements
            elif p == "Duration_EST":
                duration_temp = []
                try:
                    for i in range(len(data["results"])):
                        try:
                            duration = data['results'][i]['properties']['Duration_EST']['select']['name']
                            if ' ' in duration:
                                duration = duration.split(' ')
                                hour = int(duration[0].strip('hr'))*60
                                minute = int(duration[1].strip('min'))
                                duration = hour + minute
                            elif 'hr' in duration:
                                duration = int(duration.strip('hr'))*60
                            else:
                                duration = int(duration.strip('min'))
                            duration_temp.append(duration)
                        except:
                            duration_temp.append(0)
                except:
                    duration_temp = [0]*3
                proj_data[p] = duration_temp                                    
            
            else:
                pass
                

        return proj_data
    
    # Connects & Organizes Data
        # Runs Everything above
    def connect_DB(self, database_name):
        data = CNotion.read_Database(databaseId, headers)
        projects = CNotion.get_projects_titles(data,database_name)
        proj_data = CNotion.get_projects_data(data, projects)
        return proj_data

    
                    
    def updateDuration_EST(self, pageId, headers, duration):
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
                                    headers=headers, data=json.dumps(updateDuration_EST)) 

    def updateDuration_Tasks(self, pageId, headers, tasks):
        updateUrl_to_waitlist = f"https://api.notion.com/v1/pages/{pageId}"
    
        updateDuration_Tasks = {
            "properties": {
                "D_Tasks": {
                    "number": tasks
                }        
            }
        }
        
        
        response = requests.request("PATCH", updateUrl_to_waitlist, 
                                    headers=headers, data=json.dumps(updateDuration_Tasks)) 

    
    def get_DurationTime_EST(self, proj_data):
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
        for task in range(len(proj_data['To do'])):
            task_duration = proj_data['Duration_EST'][task]
            task_status = proj_data['To do'][task]
            
            # Only look at Today's Column 
            if proj_data['Category_current'][task] == "Today":
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
        duration_dic = {'tot_durationEST':tot_durationEST,
                        'tot_numTasks':len(tot_numTasks),
                        'fin_durationEST':fin_durationEST,
                        'fin_numTasks':len(fin_numTasks),
                        'rem_durationEST':rem_durationEST,
                        'rem_numTasks':len(rem_numTasks)}
        return duration_dic
    
    def update_DurationDB(self, duration_dic, D_proj_data):
        print("Uploading to Duration DB...")
        # Update Total, Finished, Remaining Durations & Tasks for Today
        for row in range(3):
            if D_proj_data['D_Title'][row] == "Total Work Hours EST":
                CNotion.updateDuration_EST(D_proj_data['pageId'][row], 
                                           headers, 
                                           duration_dic['tot_durationEST'])
                CNotion.updateDuration_Tasks(D_proj_data['pageId'][row], 
                                           headers, 
                                           duration_dic['tot_numTasks'])     
                
            elif D_proj_data['D_Title'][row] == "Total Work Hours Finished":
                CNotion.updateDuration_EST(D_proj_data['pageId'][row], 
                                           headers, 
                                           duration_dic['fin_durationEST'])        
                CNotion.updateDuration_Tasks(D_proj_data['pageId'][row], 
                                           headers, 
                                           duration_dic['fin_numTasks'])        
            else:
                CNotion.updateDuration_EST(D_proj_data['pageId'][row], 
                                           headers, 
                                           duration_dic['rem_durationEST'])        
                CNotion.updateDuration_Tasks(D_proj_data['pageId'][row], 
                                           headers, 
                                           duration_dic['rem_numTasks'])       
        print('Update Completed\n\n\n\n')
                
    def update_durationCSV(self, duration_dic):
        # ADD Duration variables(For further statistical analysis)
        new_row = pd.DataFrame(duration_dic, index = [0])
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
    

            
        
print('Updating Duration Database...')
databaseId = secret.todo_db("database_id")
token = secret.notion_API("token_key")
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

CNotion = Connect_Notion()
proj_data = CNotion.connect_DB("Task Database")


# Update Total Duration Estimate Database
duration_dic = CNotion.get_DurationTime_EST(proj_data)
databaseId = secret.durationTime_EST("database_id")
D_proj_data = CNotion.connect_DB("Duration Database")

# Update Duration Database
CNotion.update_DurationDB(duration_dic,D_proj_data)

# Update duration_est.csvs
CNotion.update_durationCSV(duration_dic)







        
        
        
        