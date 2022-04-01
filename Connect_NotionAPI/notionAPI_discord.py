# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 13:37:19 2021

@author: anddy
"""

''' Outline

1. Connect to Notion data
    - Connect using OPST HTTP request
    - Save the key in secrets.py filei
    - Allow the Notion Integration key to access the page we want to share

2. Decrypt data from Notion

3. Connect to secondary platform

4. Push Data to Discord

5. Discuss how to productionalize this

'''

import requests


DATABASE_ID = "*************************************"
NOTION_URL = 'https://api.notion.com/v1/databases/'
token_key = '*************************************'
query = {"filter": [{"property": "Sync","checkbox": {"equals": True}}]}

database_url = NOTION_URL + DATABASE_ID + "/query"
response = requests.post(database_url, headers={"Authorization": token_key, "Notion-Version":'2021-05-13'},
                         data = query)
response.json()['results']

## Information that I want
# - Title
# - Checkbox info
# - Duration

from slacker import Slacker

slack = Slacker('*************************************')

# Send a message to #general channel
slack.chat.post_message('#connect_notion', )



















