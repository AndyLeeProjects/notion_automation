# -*- coding: utf-8 -*-

from pprint import pprint 
import Google 
import numpy as np
import pandas as pd
from datetime import datetime
import json 

CLIENT_SECRET_FILE = r"C:\NotionUpdate\progress\notion_automation\Google_API\credentials.json"
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_allData(years_filter = None, months_filter = None):
    service = Google.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    page_token = None
    today_date = str(datetime.today())[:10]
    data = []
    while True:
        events = service.events().list(calendarId='anddy0622@gmail.com', pageToken=page_token).execute()
        for event in events['items']:
            try:
                year = event['start']['dateTime'][:4]
                month = event['start']['dateTime'][5:7]
                print(year,month)
                if year in years_filter and month in months_filter:
                   data.append(event)
            except KeyError:
                pass
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return data
  
def run_summary(data):
    keys = ['id','kind', 'summary', 'status', 'start', 'end', 'timeZone', 'attendees', 'conferenceData']
    event_summaries = {}

    # Get today's date
    today_date = str(datetime.today())[:10]
    currentMonth = str(datetime.now().month)
    nextMonth = str(datetime.now().month +1)
    currentYear = str(datetime.now().year)
    currentDay = datetime.now().day
    for event in data:
        try:
            if event['start']['dateTime'][:10] >= today_date and \
                event['start']['dateTime'][:4] == currentYear:
                for key in keys:
                    try:
                        event_summaries.setdefault(key, []).append(json_extract(key, event, currentMonth, currentYear))
                    except:
                        event_summaries.setdefault(key, []).append(np.nan)
        except KeyError:
            pass
        
    return pd.DataFrame(event_summaries)

def json_extract(key, event, currentMonth, currentYear):
  if key == 'start' or key == 'end':
    date = event[key]['dateTime'].split('-')
    month = date[1].strip('0')
    year = date[0]
    print(month, year, currentMonth, currentYear)
    if year == currentYear and month == currentMonth:
      return event[key]['dateTime']
  elif key == 'timeZone':
    return event[key]['timeZone']
  elif key == 'attendees':
    return event[key][0]['responseStatus']
  elif key == 'conferenceData':
    return event[key]['entryPoints'][0]['uri']
  else:
    return event[key]  

data = get_allData()
df = run_summary(data)
df