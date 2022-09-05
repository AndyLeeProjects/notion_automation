# -*- coding: utf-8 -*-

import requests
import sys
import numpy as np
import time
from slacker import Slacker
from datetime import datetime

sys.path.append('C:\\NotionUpdate\\progress\\notion_automation')
from myPackage import std_risetime
from secret import secret
import Connect_Notion as Notion

# ************* DO NOT DELETE *************
import notion_durationDB
from myPackage import notion_routine_API # saves morning routine
# *****************************************

class NotionSync:
    def __init__(self, database_id: str, token_key: str):

        ## Since the token_key can be reusable, let us store it
        self.token_key = token_key
        
        # Using database_id and token_key, read the designated database
        global Notion
        Notion = Notion.ConnectNotionDB(database_id, self.token_key)
        self.data = Notion.retrieve_data()
        self.titles = list(self.data.keys())
    

    def get_morning_routine(self):
        
        # Create a dictionary that stores all the morning routine variables
        routine_dic = {}

        # Reading in minutes
        reading = str(list(self.data[self.data['To-do'] == 'Personal Reading']['Duration'])[0])
        routine_dic['reading'] = reading if reading != 'nan' else 0

        # Rise time in minutes
        rise_time = str(list(self.data[self.data['To-do'] == 'Rise Time & Phone Free (1hr)']['Duration'])[0])
        routine_dic['rise_time'] = rise_time if rise_time != 'nan' else 0

        # Meditation in minutes
        meditation = str(list(self.data[self.data['To-do'] == 'Meditation']['Duration'])[0])
        routine_dic['meditation'] = meditation if meditation != 'nan' else 0

        # run in km
        run = str(list(self.data[self.data['To-do'] == 'Phone Free Before Sleep (30 min)/ run (km)']['Duration'])[0])
        routine_dic['run'] = run if run != 'nan' else 0

        # Total morning routine completed
        routine_dic['total_routine_checked'] = len([i for i in self.data['Checkbox'] if i == True])

        self.routine_dic = routine_dic


    def get_TotalEstimate(self, todo_databaseId):
        
        # Redefine the following variables for cleaner code
        total_routine_checked = int(self.routine_dic['total_routine_checked'])
        rise_time = float(self.routine_dic['rise_time'])
        meditation = float(self.routine_dic['meditation'])
        reading = float(self.routine_dic['reading'])
        run = float(self.routine_dic['run'])

        
        import Connect_Notion as Notion

        Notion = Notion.ConnectNotionDB(todo_databaseId, self.token_key)
        todo_data = Notion.retrieve_data()
        self.estimates = ''
        
        progress = '\nRoutine: '
        for task in range(6):
            if task >= total_routine_checked:
                progress += '◇'
            else:
                progress += '◈'
            if task % 4 == 0:
                progress += ' '
        self.estimates += '%s\n'%(progress)
        total_todo_today = len(todo_data[todo_data['Status'] == 'Today']['To do'])                
        total_todo_checked = sum(todo_data[todo_data['Status'] == 'Today']['To do'])                
        
        progress += '\nProgress: '
        for task in range(total_todo_today):
            if task >= total_todo_checked:
                progress += '◇'
            else:
                progress += '◈'
            if task % 4 == 0:
                progress += ' '
        self.progress = progress
        self.estimates += '%s\n\n'%(progress)
        
        total_todo_today = total_todo_today + 6
        total_todo_checked = total_todo_checked + total_routine_checked
        
        if total_todo_today < 14:
            work_done = round(total_todo_checked / (3.33 * total_todo_today) * 1000) / 10
        else:
            work_done = round(total_todo_checked / (3.03 * total_todo_today) * 1000) / 10
            
        # Get Average for the remaining variables (ESTIMATE)
        '''
        
        *** Recalculate Estimate model using Probability ***
        
        '''

        # Read Evaluation data to utilize them to estimate present value
        import Connect_Notion as Notion 
        Notion = Notion.ConnectNotionDB(secret.evaluation_db('database_id'), self.token_key)
        evaluation_data = Notion.retrieve_data()
        
        # Set Average days to estaimate values
        if len(evaluation_data['Name']) > 2:
            est_days = 3
        else:
            est_days = len(evaluation_data['Name'])
        
        # Get the most current update of rise time from std_risetime.py
        co = std_risetime.changed_risetime()    
        
        if rise_time == None:
            rise_time = np.average(evaluation_data['Rise time'][-est_days:])
            est = 'Rise Time EST: '
        else:
            est = '* Rise Time: '
            
        if rise_time > 0:
            rise_time_est = -round(rise_time * (rise_time - rise_time / 1.01) * 0.04 * 100) / 100
            self.estimates += est + str(time.strftime('%H:%M',time.gmtime(rise_time*60+co[list(co.keys())[-1]]))) + '\n'
        else:
            rise_time_est = round(rise_time * (rise_time - rise_time / 1.01) * 0.04 * 100) / 100
            self.estimates += est + str(time.strftime('%H:%M',time.gmtime(rise_time*60+co[list(co.keys())[-1]]))) + '\n'
        
        if meditation == 0:
            medit_est = np.average(evaluation_data['Meditation (min)'][-est_days:])
            self.estimates += 'Meditation EST: ' + str(round(medit_est,2)) + '\n' 
            medit_est = round(medit_est / 181 * 1000) / 10
        else:
            medit_est = round(meditation / 181 * 1000) / 10
            self.estimates += '* Meditation: ' + str(round(meditation,2)) + '\n' 
        
        if reading == 0:
            reading_est = np.average(evaluation_data['Personal Reading'][-est_days:])
            self.estimates += 'Reading EST: ' + str(round(reading_est,2)) + '\n' 
            reading_est = round(reading_est / 65 * 100) / 10
        else:
            reading_est = round(reading / 65 * 100) / 10
            self.estimates += '* Reading: ' + str(round(reading,2)) + '\n'     
        
        screen_time_est = np.average(evaluation_data['*Screen time'][-est_days:])
        self.estimates += 'Screen Time EST: %dh %dm\n'%(screen_time_est//60, screen_time_est%60)
        screen_time_est = round((screen_time_est / screen_time_est * 1000 - screen_time_est) / 376000 * 100000) / 10
        
        pickup_est = np.average(evaluation_data['*Phone pickups'][-est_days:])
        self.estimates += 'Pick Up EST: ' + str(round(pickup_est,2)) + '\n' 
        pickup_est = round((pickup_est / pickup_est * 340 - pickup_est) / 279800 * 100 * 1000) / 10
        
        drink_est = np.average(evaluation_data['Drink? (over 3 beer)'][-est_days:])*-3
        #self.estimates += 'Drink EST: ' + str(round(drink_est,2)) + '\n' 

        if run == 0:
            run_est = (np.average(evaluation_data['Run (km)'][-est_days:]))
        else:
            run_est = (run / 85 * 10000) / 100
            self.estimates += '* Run: ' + str(round(run,3)) + 'km\n'
        
        multiple_est = np.average(evaluation_data['*Multiple (1~5)'][-est_days:])
        self.estimates += 'Multiple EST: ' + str(round(multiple_est,2)) + '\n' 
        multiple_est = multiple_est * (1.2 + 6 / multiple_est)
        
        self.totalEST = round(work_done + rise_time_est + medit_est+
                      screen_time_est + pickup_est + drink_est + run_est +
                      multiple_est + reading_est,2)
        
        
    
    
    def morning_journal(self, mj_databaseId):

        # Get morning journal data using Notion_API.py
        import Connect_Notion as Notion
        Notion = Notion.ConnectNotionDB(mj_databaseId, self.token_key)
        mj_data = Notion.retrieve_data()
        today = datetime.today()
        today_date = today.strftime('%Y-%m-%d')

        # If the most recent morning journal was not written today, do not include journal content
        if max(mj_data['Date']) != today_date:
            today_promises_str = ''
            estimated_workHours_str = ''
            thankful_for_str = ''
            pass
        else:
            today_promises = list(mj_data[mj_data['Date'] == today_date]['PROMISE'])[0]
            estimated_workHours_str = "EST Work Hours: " + mj_data[mj_data['Date'] == today_date]['Total Work Hours'] + '\n'
            thankful_for_str = '\nThankful for: ' + '\n\t- ' + mj_data[mj_data['Date'] == today_date]['Thankful for ...'] + '\n'
            c = 1                     
            today_promises_str = '\n\nToday\'s Promise: '
            if today_promises == []:
                today_promises_str = ''
            else:
                if isinstance(today_promises, list):
                    for p in range(len(today_promises)):
                        today_promises_str += '\n\t' + str(p + 1) + '. ' + today_promises[p]
                else:
                    today_promises_str += '\n\t' + today_promises

        message = '''****************************************\nUpdated Time: %s   < %.2f >\n****************************************\n\nToday's Estimated Percentage : %.2f%%\n'''%(datetime.now().strftime('%m/%d %H:%M'),  \
                self.totalEST,self.totalEST) + estimated_workHours_str + self.progress + \
                     today_promises_str + '\n' + thankful_for_str + '\n'
        # Change self.progress -> self.estimates if you want to see the estimates variables

        self.message = message
        print(self.message)

    def send_slackMessage(self):
        # Send a Message using Slack
        now = datetime.now()
        hour = now.strftime('%H')
        minute = now.strftime('%M')

        # Send every 3 hours
        if int(hour) % 3 == 0 and int(minute) < 2:
            data = {
                'token': secret.connect_slack(key = 'token_key', app_name = 'progress_report'),
                'channel': secret.connect_slack(key = 'user_id_hourly_update'),    # User ID.
                'as_user': True,
                'text': self.message
            }
            
            result = requests.post(url='https://slack.com/api/chat.postMessage',
                        data=data)
        else:
            pass
        time.sleep(1)
    
    def execute_all(self):
        # To do list database
        # Compute the Estimations & Rest of the Evaluation variables
        todo_databaseId = secret.task_scheduleDB('database_id')
        self.get_morning_routine()
        self.get_TotalEstimate(todo_databaseId)

        # Morning Routine database
        # Get the Morning Principles & Promises and others
        mj_databaseId = secret.morning_journalDB('database_id')
        self.morning_journal(mj_databaseId)

        self.send_slackMessage()

# Mornig Routine
database_id = secret.notion_API('database_id')
token_key = secret.notion_API('token_key')
nsync = NotionSync(database_id, token_key)
nsync.execute_all()










