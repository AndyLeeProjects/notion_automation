# -*- coding: utf-8 -*-

from pprint import pprint 
from Google_API import Google 
import numpy as np
import pandas as pd
from datetime import datetime
import json 
import sys
sys.path.append('C:\\NotionUpdate\\progress\\notion_automation')
from secret import secret

class GoogleCalendarAPI:
    def __init__(self, CLIENT_SECRET_FILE:str, API_NAME:str = 'calendar', API_VERSION:str = 'v3', 
    SCOPES:list = ['https://www.googleapis.com/auth/calendar'], calendar_id:str = None, years_filter: list = None, months_filter: list = None):
        """__init__(): Set up for Google Calendar API and also pass in assigned filters

        Args:
            CLIENT_SECRET_FILE (str): file location of the credentials.json file
            API_NAME (str): Name of the API (calendar)
            API_VERSION (str): Specified API version
            SCOPES (list): Specified scopes
            years_filter (list, optional): specified years for the data retrieval. Defaults to None.
            months_filter (list, optional): specified months for the data retrieval. Defaults to None.
        """
        # API Set up
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.API_NAME = API_NAME
        self.API_VERSION = API_VERSION
        self.SCOPES = SCOPES

        # Assign filters 
        self.years_filter = years_filter
        self.months_filter = months_filter

        # If filters for years & months are not specified, get current year & month data 
        currentMonth = '{:02d}'.format(datetime.now().month)
        nextMonth = '{:02d}'.format(datetime.now().month + 1)
        currentYear = str(datetime.now().year)

        if self.years_filter == None:
            self.years_filter = [currentYear]
        if self.months_filter == None:
            self.months_filter = [currentMonth, nextMonth]


    def get_CalendarData(self):
        """
        get_CalendarData(): Using the API setup & the assigned filters, retrieve data using Google Calendar API
        """
        # Pass in necessary parameters
        service = Google.Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)
        page_token = None

        self.calendar_jsonData = []
        while True:
            
            # Call data 
            events = service.events().list(calendarId='anddy0622@gmail.com', pageToken=page_token).execute()
            for event in events['items']:

                try:
                    # Get year and month in string format from the JSON data
                    year = event['start']['dateTime'][:4]
                    month = event['start']['dateTime'][5:7]

                    # if assigned year & month are matched, append
                    if year in self.years_filter and month in self.months_filter:
                        self.calendar_jsonData.append(event)
                except KeyError:
                    pass
            page_token = events.get('nextPageToken')
            if not page_token:
                break
    
    def organize_CalendarData(self):
        """
        organize_CalendarData(): This method organizes the list of JSON data into a nice dataframe
        """
        keys = ['id','kind', 'summary', 'creator', 'organizer', 'status', 'start', 'end', 'timeZone', 'attendees', 'conferenceData', 'recurringEventId', 'sequence']
        self.calendar_data = {}

        # Get today's date
        today_date = str(datetime.today())[:10]
        for event in self.calendar_jsonData:
            try:
                if event['start']['dateTime'][:10] >= today_date:
                    for key in keys:
                        try:
                            self.calendar_data.setdefault(key, []).append(self.json_extract(key, event))
                        except:
                            self.calendar_data.setdefault(key, []).append(np.nan)
            except KeyError:
                pass
        
        self.calendar_data = pd.DataFrame(self.calendar_data)
        return self.calendar_data
            
    def get_todayTasks(self):
        """get_todayTasks

        Returns:
            list: list of today's tasks (pandas DF)
        """
        currentDay = str(datetime.today())[:10]
        today_tasks = [self.calendar_data.index[date]
                        for date in range(len(self.calendar_data))
                        if self.calendar_data['start'].iloc[date][:10] == currentDay]
        
        return self.calendar_data.loc[today_tasks]
        


    def json_extract(self, key:str, event:json):
        """
        json_extract(): Since the variables have different depth of JSON format, 
        this function provides appropriate depth for each variable. 

        Args:
            key (str): keys for the variables (ex. timeZone, start & end(date), attendees, conferenceData)
            event (json): json data

        Returns:
            _type_: _description_
        """
        if key == 'start' or key == 'end':
            return event[key]['dateTime']
        elif key == 'timeZone':
            return event[key]['timeZone']
        elif key == 'attendees':
            return event[key][0]['responseStatus']
        elif key == 'conferenceData':
            return event[key]['entryPoints'][0]['uri']
        elif key == 'creator' or key == 'organizer':
            return event[key]['email']
        else:
            return event[key]
    
    def execute_all(self, get_data:str = "today_tasks"):
        """
        execute_all(): Executes all codes above and returns data depending on the users' preferences:
            - today tasks
            - upcoming tasks

        Args:
            get_data (str, optional): _description_. Defaults to "today_tasks".

        Returns:
            dataframe: today's tasks or upcoming tasks in a dataframe format
        """
        self.get_CalendarData()
        upcoming_tasks = self.organize_CalendarData()
        today_tasks = self.get_todayTasks()

        if get_data == "today_tasks":
            return today_tasks
        else:
            return upcoming_tasks
        