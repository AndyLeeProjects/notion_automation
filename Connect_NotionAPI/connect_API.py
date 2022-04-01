<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 00:23:34 2022

@author: anddy
"""

import requests


class NotionSync:
    def query_databases(token_key, DATABASE_ID, NOTION_URL):
        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={"Authorization": token_key, "Notion-Version":'2021-08-16'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(data_json):
        return list(data_json["results"][0]["properties"].keys())
=======
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 00:23:34 2022

@author: anddy
"""

import requests


class NotionSync:
    def query_databases(token_key, DATABASE_ID, NOTION_URL):
        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={"Authorization": token_key, "Notion-Version":'2021-08-16'})
        if response.status_code != 200:
            raise ValueError(f'Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(data_json):
        return list(data_json["results"][0]["properties"].keys())
>>>>>>> 572dc86 (update)
