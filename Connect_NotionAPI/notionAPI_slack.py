# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 13:30:44 2021

@author: anddy
"""

import requests
import sys
import numpy as np
import time
from slacker import Slacker
from datetime import datetime

sys.path.append('C:\\NotionUpdate\progress')
from Connect_NotionAPI import NotionUpdate_API as NAPI
from myPackage import std_risetime
from secret import secret



DATABASE_ID = secret.notion_API("DATABASE_ID")
token_key = secret.notion_API("token_key")
NOTION_URL = 'https://api.notion.com/v1/databases/'

class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self,integration_token=token_key):
        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={"Authorization": token_key, "Notion-Version":'2021-08-16'})
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
        todo_temp = []
        for p in projects:
            if "Related" in p or "you" in p:
                pass
            elif p !="To-do" and p != 'Duration':
                for i in range(len(data_json["results"])):
                    try:
                        todo_temp.append(data_json["results"][i]["properties"][p]["checkbox"])
                    except:
                        todo_temp.append(None)
                projects_data[p] = todo_temp
            elif p=="To-do" or p=="Not to-do":
                names = [data_json['results'][i]['properties'][p]['title'][0]['text']['content']
                                    for i in range(len(data_json["results"]))]
            elif p=="Duration":
                for i in range(len(data_json["results"])):
                    try:
                        duration_temp.append(data_json['results'][i]['properties']['Duration']['number'])
                    except:
                        duration_temp.append(None)
                projects_data[p] = duration_temp

        # When everything is NULL, it causes KeyError 
        # Run it only if Duration title is in the database
        if 'Duraiton' in projects:
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
                if meditation == None:
                    meditation = 0
            elif names[i] == 'Personal Reading':
                PR = projects_data['Duration'][i]
                try:
                    if PR > 0:
                        reading = PR
                    else:
                        reading = 0
                except:
                    reading = 0
            elif names[i] == 'Rise Time & Phone Free (1hr)':
                rise_time = projects_data['Duration'][i]
    
            elif names[i] == 'Phone Free Before Sleep (30 min)/ run (km)':
                run = projects_data['Duration'][i]
                if run == None:
                    run = 0
                
            if projects_data['Checkbox'][i] == True:
                total_checked.append('Checked')
            
        total_checked = len(total_checked)
        
        return total_checked, meditation, rise_time, reading, run


    def get_TotalEstimate(self, data, total_checked, rise_time, meditation, reading, run):
        
        nsync_mon = NAPI.NotionSync()
        data_mon = NAPI.nsync.query_databases()
        projects_mon = NAPI.nsync.get_projects_titles(data_mon)
        projects_data_mon = NAPI.nsync.get_projects_data(data_mon,projects_mon)

        estimates = ''
        
        morning_routine_progress = '\nRoutine: '
        for task in range(6):
            if task >= total_checked:
                morning_routine_progress += '◇'
            else:
                morning_routine_progress += '◈'
            if (task+1)% 5 == 0:
                morning_routine_progress += ' '
        estimates += '%s\n'%(morning_routine_progress)
        
        todo_today = []
        todo_checked = []
        for i in range(len(data['results'])):
            status = data['results'][i]['properties']['Status 1']['select']['name']
            if status == 'Today':
                todo_today.append(status)
                if data['results'][i]['properties']['To do']['checkbox'] == True:
                    todo_checked.append('Checked')
                
        
        total_todo_today = len(todo_today)
        total_todo_checked = len(todo_checked)
        progress = 'Progress: '
        for task in range(total_todo_today):
            if task >= total_todo_checked:
                progress += '◇'
            else:
                progress += '◈'
            if (task+1)% 5 == 0:
                progress += ' '
        estimates += '%s\n\n'%(progress)
        
        total_todo_today = len(todo_today) + 6
        total_todo_checked = len(todo_checked) + total_checked
        
        if total_todo_today < 14:
            work_done = round(total_todo_checked / (3.33 * total_todo_today) * 1000) / 10
        else:
            work_done = round(total_todo_checked / (3.03 * total_todo_today) * 1000) / 10
            
        # Get Average for the remaining variables (ESTIMATE)
        '''
        
        *** Recalculate Estimate model using Probability ***
        
        '''

        
        # Set Average days to estaimate values
        if len(projects_data_mon['Name']) > 2:
            est_days = 3
        else:
            est_days = len(projects_data_mon['Name'])
        
        # Get the most current update of rise time from secret.py
        co = std_risetime.changed_risetime()    
        
        if rise_time == None:
            rise_time = np.average(projects_data_mon['Rise time'][-est_days:])
            est = 'Rise Time EST: '
        else:
            est = '* Rise Time: '
            
        if rise_time > 0:
            rise_time_est = -round(rise_time * (rise_time - rise_time / 1.01) * 0.04 * 100) / 100
            estimates += est + str(time.strftime('%H:%M',time.gmtime(rise_time*60+co[list(co.keys())[-1]]))) + '\n'
        else:
            rise_time_est = round(rise_time * (rise_time - rise_time / 1.01) * 0.04 * 100) / 100
            estimates += est + str(time.strftime('%H:%M',time.gmtime(rise_time*60+co[list(co.keys())[-1]]))) + '\n'
        
        if meditation == 0:
            medit_est = np.average(projects_data_mon['Meditation (min)'][-est_days:])
            estimates += 'Meditation EST: ' + str(round(medit_est,2)) + '\n' 
            medit_est = round(medit_est / 181 * 1000) / 10
        else:
            medit_est = round(meditation / 181 * 1000) / 10
            estimates += '* Meditation: ' + str(round(meditation,2)) + '\n' 
        
        if reading == 0:
            reading_est = np.average(projects_data_mon['Personal Reading'][-est_days:])
            estimates += 'Reading EST: ' + str(round(reading_est,2)) + '\n' 
            reading_est = round(reading_est / 65 * 100) / 10
        else:
            reading_est = round(reading / 65 * 100) / 10
            estimates += '* Reading: ' + str(round(reading,2)) + '\n'     
        
        screen_time_est = np.average(projects_data_mon['*Screen time'][-est_days:])
        estimates += 'Screen Time EST: %dh %dm\n'%(screen_time_est//60, screen_time_est%60)
        screen_time_est = round((screen_time_est / screen_time_est * 1000 - screen_time_est) / 376000 * 100000) / 10
        
        pickup_est = np.average(projects_data_mon['*Phone pickups'][-est_days:])
        estimates += 'Pick Up EST: ' + str(round(pickup_est,2)) + '\n' 
        pickup_est = round((pickup_est / pickup_est * 340 - pickup_est) / 279800 * 100 * 1000) / 10
        
        drink_est = np.average(projects_data_mon['Drink? (over 3 beer)'][-est_days:])*-3
        #estimates += 'Drink EST: ' + str(round(drink_est,2)) + '\n' 

        if run == 0:
            run_est = (np.average(projects_data_mon['Run (km)'][-est_days:]))
        else:
            run_est = (run / 85 * 10000) / 100
            estimates += '* Run: ' + str(round(run,3)) + 'km\n'
        
        multiple_est = np.average(projects_data_mon['*Multiple (1~5)'][-est_days:]*100)
        estimates += 'Multiple EST: ' + str(round(multiple_est,2)) + '\n' 
        multiple_est = multiple_est * (1.2 + 6 / multiple_est)
        
        
        total = round(work_done + rise_time_est + medit_est+
                      screen_time_est + pickup_est + drink_est + run_est +
                      multiple_est + reading_est,2)
        return total, estimates
    
                
                    
    
    
    def morning_principles(self, data_json, projects):
        today = datetime.today()
        today_date = today.strftime("%Y-%m-%d")
        if data_json['results'][0]['properties']['Date']['date']['start'] != today_date:
            today_promises_str = ''
            relation_principles_str = ''
            habit_principles_str = ''
            pass
        else:
            principles = data_json['results'][0]['properties']['Relationship principle']['multi_select']
            relation_principles = [data_json['results'][0]['properties']['Relationship principle']['multi_select'][p]['name']
                                for p in range(len(principles))]
            
            promises = data_json['results'][0]['properties']['PROMISE']['multi_select']
            today_promises = [data_json['results'][0]['properties']['PROMISE']['multi_select'][p]['name']
                                for p in range(len(promises))]
            habits = data_json['results'][0]['properties']['Today\'s habit']['multi_select']
            today_habits = [data_json['results'][0]['properties']['Today\'s habit']['multi_select'][p]['name']
                                for p in range(len(habits))]
            habit_principles_str = '\n-------------- Habit principles ------------- \n'
            
            today_habits = today_habits[0].replace(';','\n')
            habit_principles_str += today_habits + '\n'
            
            relation_principles_str = '\n---------- Relationship principles ---------- \n'
            c = 1                     
            for p in range(len(relation_principles)):
                relation_principles_str += str(c)+'. '+ relation_principles[p] + '\n'
                c += 1
            today_promises_str = '\n\nToday\'s Promise: '
            if today_promises == []:
                today_promises_str = ''
            else:
                for p in range(len(today_promises)):
                    today_promises_str += today_promises[p]
                    try:
                        today_promises[p+1]
                        today_promises_str += ', '
                    except:
                        pass
            
        return habit_principles_str, relation_principles_str, today_promises_str 
        
    def get_work_total(self, data, projects):
        total_work = []
        
        for i in range(len(data['results'])):
            if data['results'][13]['properties']['Status 1']['select']['name'] == 'Work':
                name = data['results'][3]['properties']['Name']['title'][0]['plain_text']
                total_work.append(name)
    
# Morning Routine
nsync = NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data,names = nsync.get_projects_data(data,projects)

total_checked = nsync.MorningRoutine(projects_data, names)[0]
meditation = nsync.MorningRoutine(projects_data, names)[1]
rise_time = nsync.MorningRoutine(projects_data, names)[2]
reading = nsync.MorningRoutine(projects_data, names)[3]
run = nsync.MorningRoutine(projects_data, names)[4]


# To do list database
# Compute the Estimations & Rest of the Evaluation variables
DATABASE_ID = secret.todo_db("DATABASE_ID")
nsync = NotionSync()
data = nsync.query_databases()
totalestimates, estimates = nsync.get_TotalEstimate(data, total_checked, rise_time, meditation, reading, run)

# Morning Routine database
# Get the Morning Principles & Promises and others
DATABASE_ID = secret.morning_routine_db("DATABASE_ID")

nsync = NotionSync()
morning_data = nsync.query_databases()
projects_morning = nsync.get_projects_titles(morning_data)
habits, relationship, promises = nsync.morning_principles(morning_data, projects_morning)


# Send a Message using Slack
slack = Slacker(secret.slack_token("slack_token"))
now = datetime.now()
dt_string = now.strftime("%m/%d %H:%M")

message = '''
****************************************
Updated Time: %s   < %.2f >
****************************************

Today's Estimated Percentage : %.2f%%
'''%(dt_string, totalestimates,totalestimates) + estimates + habits + relationship + promises + '\n'
print(message)
file = r"C:\NotionUpdate\progress\jpg files\Monthly Evaluation\month.jpg"
slack.chat.post_message('#connect_notion', message)
#slack.files.upload(file,message,  channels='#connect_notion')


time.sleep(1)





