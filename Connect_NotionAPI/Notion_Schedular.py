<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:47:04 2021

@author: anddy
"""
import requests
import sys
import numpy as np
sys.path.append('C:\\NotionUpdate\\progress\\myPackage')


DATABASE_ID = "4435daff4bff4539a01b584e9f026a65"
NOTION_URL = 'https://api.notion.com/v1/databases/'
token_key = 'secret_WCXYCVzuU52uLqAdYvJZRtpnd3UD4vR1c85iPFr0n55'

class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self,integration_token=token_key):
        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={"Authorization": token_key, "Notion-Version":'2021-05-13'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(self,data_json):
        max_var = 0
        index = 0
        for i in range(len(data_json['results'])):
            try:
                if len(data_json['results'][i].keys()) > max_var:
                    max_var = len(data_json['results'][i].keys())
                    index = i 
            except:
                pass
        
        projects = list(data_json["results"][index]["properties"].keys())
        if 'Due Date' not in list(data_json["results"][index]["properties"].keys()):    
            projects.append('Due Date')
        
        return projects

    def get_projects_data(self,data_json,projects):        
        projects_data = {}
        preset = data_json['results']   
        date_temp = []
        due_date_temp = []
        for p in projects:
            if p == 'Date':
                for i in range(len(preset)):
                    if len(preset[i]['properties'][p]['multi_select']) == 0:
                        date_temp.append([])
                        pass
                    else:
                        temp = [preset[i]['properties'][p]['multi_select'][k]['name']
                            for k in range(len(preset[i]['properties'][p]['multi_select']))]
                            
                        date_temp.append(temp)

                projects_data[p] = date_temp
            elif p == 'Status 1':
                projects_data[p] = [preset[i]['properties']['Status 1']['select']['name']
                    for i in range(len(preset))]
            elif p == 'Name':
                projects_data[p] = [preset[i]['properties']['Name']['title'][0]['plain_text']
                    for i in range(len(preset))]
            elif p == 'Due Date':
                for i in range(len(preset)):
                    try:
                        temp = preset[i]['properties']['Due Date']['date']['start']
                    except:
                        temp = 0
                    due_date_temp.append(temp)
                projects_data[p] = due_date_temp
        
        return projects_data
        
    
nsync = NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data = nsync.get_projects_data(data,projects)


















=======
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:47:04 2021

@author: anddy
"""
import requests
import sys
import numpy as np
sys.path.append('C:\\NotionUpdate\\progress\\myPackage')


DATABASE_ID = "4435daff4bff4539a01b584e9f026a65"
NOTION_URL = 'https://api.notion.com/v1/databases/'
token_key = 'secret_WCXYCVzuU52uLqAdYvJZRtpnd3UD4vR1c85iPFr0n55'

class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self,integration_token=token_key):
        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={"Authorization": token_key, "Notion-Version":'2021-05-13'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(self,data_json):
        max_var = 0
        index = 0
        for i in range(len(data_json['results'])):
            try:
                if len(data_json['results'][i].keys()) > max_var:
                    max_var = len(data_json['results'][i].keys())
                    index = i 
            except:
                pass
        
        projects = list(data_json["results"][index]["properties"].keys())
        if 'Due Date' not in list(data_json["results"][index]["properties"].keys()):    
            projects.append('Due Date')
        
        return projects

    def get_projects_data(self,data_json,projects):        
        projects_data = {}
        preset = data_json['results']   
        date_temp = []
        due_date_temp = []
        for p in projects:
            if p == 'Date':
                for i in range(len(preset)):
                    if len(preset[i]['properties'][p]['multi_select']) == 0:
                        date_temp.append([])
                        pass
                    else:
                        temp = [preset[i]['properties'][p]['multi_select'][k]['name']
                            for k in range(len(preset[i]['properties'][p]['multi_select']))]
                            
                        date_temp.append(temp)

                projects_data[p] = date_temp
            elif p == 'Status 1':
                projects_data[p] = [preset[i]['properties']['Status 1']['select']['name']
                    for i in range(len(preset))]
            elif p == 'Name':
                projects_data[p] = [preset[i]['properties']['Name']['title'][0]['plain_text']
                    for i in range(len(preset))]
            elif p == 'Due Date':
                for i in range(len(preset)):
                    try:
                        temp = preset[i]['properties']['Due Date']['date']['start']
                    except:
                        temp = 0
                    due_date_temp.append(temp)
                projects_data[p] = due_date_temp
        
        return projects_data
        
    
nsync = NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data = nsync.get_projects_data(data,projects)


















>>>>>>> 572dc86 (update)
