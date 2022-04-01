# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 18:44:41 2021

@author: anddy
"""

from datetime import datetime
from slacker import Slacker
import time

import requests
import sys
import numpy as np
sys.path.append('C:\\NotionUpdate\progress\Connect_NotionAPI')
import NotionUpdate_API as NAPI
DATABASE_ID = "62ac6e95-661d-437c-944c-bfc594054b80"
NOTION_URL = 'https://api.notion.com/v1/databases/'
token_key = 'secret_WCXYCVzuU52uLqAdYvJZRtpnd3UD4vR1c85iPFr0n55'


class NotionSync:
    def __init__(self):
        pass

    def query_databases(self, integration_token=token_key):
        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={
                                 "Authorization": token_key, "Notion-Version": '2021-05-13'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            return response.json()

    def get_projects_titles(self, data_json):
        most_properties = [len(data_json['results'][i]['properties'])
                           for i in range(len(data_json["results"]))]
        return list(data_json["results"][np.argmax(most_properties)]["properties"].keys())

    
    def get_projects_data(self,data_json,projects):
        
        projects_data = {}   
        dates = []
        names = []
        checkin = []
        for p in projects:
            if p == 'Name':
                projects_data[p] = [data['results'][i]['properties']['Name']['title'][0]['plain_text']
                     for i in range(len(data_json['results']))]
                    
            elif p == 'Date':
                projects_data[p] = [data['results'][i]['properties']['Date']['date']['start'] + ' ~ ' + 
                                    data['results'][i]['properties']['Date']['date']['end']
                                    for i in range(len(data_json['results']))]
                for i in range(len(data_json['results'])):
                    checkin.append(data['results'][i]['properties']['Date']['date']['start'])
                projects_data['checkin'] = checkin
            
            elif p == 'Tags':
                projects_data[p] = [data['results'][i]['properties']['Tags']['multi_select'][0]['name']
                                   for i in range(len(data_json['results']))]
        return projects_data
    
    def checkin_today(self, projects_data):
        
        # Get today's date
        today = datetime.today()
        today_date = today.strftime("%Y-%m-%d")
        
        checkin_alert = '*****************************\n    %s 입실 목록\n*****************************\n'% today_date
        
        men_current = 0
        men_today = 0
        women_current = 0
        women_today = 0
        out_today = ''
        for checkin in range(len(projects_data['Name'])):
            date = projects_data['Date'][checkin].split(' ~ ')
            beg_date = date[0]
            end_date = date[1]
            
            num_peop = projects_data['Name'][checkin].split('(')
            num_peop = int(num_peop[1].strip(')'))
            
            
            if today_date == beg_date:
                if '민트' in projects_data['Tags'][checkin]:
                    men_today += num_peop
                else:
                    women_today += num_peop
            elif beg_date < today_date < end_date:
                if '민트' in projects_data['Tags'][checkin]:
                    men_current += num_peop
                else:
                    women_current += num_peop
            
            if projects_data['checkin'][checkin] == today_date:
                checkin_alert += projects_data['Name'][checkin] + '\n' + projects_data['Tags'][checkin]\
                + '\n' + projects_data['Date'][checkin] + '\n\n'
            
            if today_date == end_date:
                out_today += projects_data['Name'][checkin] + '\n'
        
        if men_today == 0 and women_today == 0:
            no_reser = '입실 없음\n'
        else:
            no_reser = ''
        checkin_alert += '%s-----------------------------\n*현재 현황* (당일 입실)\n남자: %d (%d)\n여자: %d (%d)\n\n-----------------------------\n*당일 퇴실*\n%s' \
            % (no_reser,men_current,men_today, women_current, women_today, out_today)
                            
        return checkin_alert
        
nsync = NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data = nsync.get_projects_data(data,projects)
checkin_alert = nsync.checkin_today(projects_data)


print(checkin_alert)

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer "+token},
                             data={"channel": channel, "text": text}
                             )
    print(response)


myToken = "xoxb-2209926566434-2195209412855-0NC5kEd4t1EoNz7OVEMHYjLQ"

post_message(myToken, "#general", checkin_alert)
