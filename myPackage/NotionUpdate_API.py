# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 18:26:56 2021

@author: anddy
"""
import requests
import sys
from datetime import time as time_time
from datetime import date
sys.path.append('C:\\NotionUpdate\\progress')
from secret import secret



DATABASE_ID = secret.evaluation_db("DATABASE_ID")
NOTION_URL = 'https://api.notion.com/v1/databases/'
token_key = secret.notion_API("token_key")

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
        return list(data_json["results"][0]["properties"].keys())
    
    
    def get_projects_data(self,data_json,projects):
        projects_data = {}
        temp = []
        for p in projects:
            preset = data_json['results'][0]['properties'][p]
            if preset['type'] == 'formula':
                projects_data[p] = [data_json["results"][i]["properties"][p]["formula"]['number']
                                    for i in range(len(data_json["results"])-1,-1,-1)]
            elif preset['type'] == 'date':
                projects_data[p] = [data_json["results"][i]["properties"][p]['date']['start']
                                    for i in range(len(data_json["results"])-1,-1,-1)]
            elif preset['type'] == 'number':
                for i in range(len(data_json["results"])-1,-1,-1):
                    try:
                        temp.append(data_json["results"][i]["properties"][p]['number'])
                    except KeyError:
                        temp.append(0)
                projects_data[p] = temp
                temp = []
            elif preset['type'] == 'rich_text':
                temp = []
                for i in range(len(data_json["results"])-1,-1,-1):    
                    try:
                        temp.append(data_json["results"][i]["properties"][p]['rich_text'][0]['plain_text'])
                    except:
                        temp.append(0)
                projects_data[p] = temp
                temp = []
            elif preset['type'] == 'title':
                projects_data[p] = [data_json["results"][i]["properties"][p]['title'][0]['plain_text']
                                    for i in range(len(data_json["results"])-1,-1,-1)]
        return projects_data
        
                    
                

nsync = NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data = nsync.get_projects_data(data,projects)



from notion.client import NotionClient
import time

def uploadEvaluationJPG():
    token_v2 = secret.notion_API("token_v2")
    client = NotionClient(token_v2=token_v2)
    # connect page
    url = 'https://www.notion.so/Home-4c8126a86ee7449597275f600cc2b51b'
    page = client.get_block(url)
    
    time.sleep(1)
    
    newchild = page.children.add_new('image')
    time.sleep(1)
    newchild.upload_file(r"C:\NotionUpdate\progress\jpg files\Monthly Evaluation\month.jpg")
    newchild.move_to(page.children[1],"before")
    page.children[0].remove()

    





















