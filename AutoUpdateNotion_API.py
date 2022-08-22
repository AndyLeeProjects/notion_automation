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
from myPackage import NotionUpdate_API as NAPI
from myPackage import change_background as cb
from myPackage import Monthly_Eval as pMon
from myPackage import Read_Data as NRD

# Modify the data for git representation(Privacy reasons)
from myPackage import remove_names_git



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
            return  ['Duration_EST', 'D_Tasks', 'D_Title', 'pageId']
            
                
    
    def get_projects_data(self, data, projects):
        proj_data = {}
        
        for p in projects:
            if p == "Due Date":
                # Each block's Due Dates
                due_temp = []
                for i in range(len(data["results"])):
                    try:
                        due_temp.append(data['results'][i]['properties']['Due Date']['date']['start'])
                    except:
                        due_temp.append(0)
                
                proj_data[p] = due_temp
                
            elif p == "Date":
                # Each block's Dates(Mon,Tue,...,Sun)
                date_temp = []
                for i in range(len(data["results"])):
                    block = data['results'][i]['properties']['Date']['multi_select']
                    temp_p = [block[date]["name"]
                              for date in range(len(block))]
                    date_temp.append(temp_p)
                proj_data[p] = date_temp
            
            elif p == "pageId":
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
                    try:
                        task_temp.append(data['results'][i]['properties'][p]['number'])
                    except:
                        task_temp.append(0)
                proj_data[p] = task_temp 
                                    
            # Organize the duration data for each task/ block
                # the data is recorded as '1hr' or '30min' so we need to unify them into minute elements
            elif p == "Duration_EST":
                duration_temp = []
                try:
                    for i in range(len(data["results"])):
                        try:
                            duration = data['results'][i]['properties']['Duration_EST']['select']['name']
                            if 'hr' in duration:
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
            if CNotion.is_time_between(time_time(13,00),time_time(23,59)) == True:
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
        data_eval = NAPI.nsync.query_databases()
        projects_eval = NAPI.nsync.get_projects_titles(data_eval)
        projects_data_eval = pd.DataFrame(NAPI.nsync.get_projects_data(data_eval,projects_eval))
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
        #NAPI.uploadEvaluationJPG()
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
    

        

databaseId = secret.todo_db("DATABASE_ID")
token = secret.notion_API("token_key")
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}
    
# Schedule my tasks 
CNotion = Connect_Notion()
proj_data = CNotion.connect_DB("Task Database")

# Update Schedule
CNotion.update_Schedule(proj_data)

# Read Evaluation Database in Notion using different database ID
databaseId = secret.evaluation_db("DATABASE_ID")
CNotion = Connect_Notion()
data = CNotion.read_Database(databaseId, headers)
projects = CNotion.get_projects_titles(data, "Task Database")
eval_data = CNotion.get_evaluation_data(data, projects)

# Update Total Duration Estimate Database
# Reconnect to get updated database
databaseId = secret.todo_db("DATABASE_ID")
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








        
        
        
        