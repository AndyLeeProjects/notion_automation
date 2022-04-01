<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 00:38:08 2022

@author: anddy
"""

import sys
sys.path.append('C:\\NotionUpdate\progress\Connect_NotionAPI')
import notionAPI_slack as NSlack
from slacker import Slacker
import datetime as datetime


# Morning Routine
nsync = NSlack.NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data,names = nsync.get_projects_data(data,projects)

total_checked = nsync.MorningRoutine(projects_data, names)[0]
meditation = nsync.MorningRoutine(projects_data, names)[1]
rise_time = nsync.MorningRoutine(projects_data, names)[2]
reading = nsync.MorningRoutine(projects_data, names)[3]
run = nsync.MorningRoutine(projects_data, names)[4]


# Compute the Estimations & Rest of the Evaluation variables
DATABASE_ID = "2bab419dd8734e899ea28fb1ec412a49"
NOTION_URL = 'https://api.notion.com/v1/databases/'
token_key = 'secret_WCXYCVzuU52uLqAdYvJZRtpnd3UD4vR1c85iPFr0n55'

DATABASE_ID = "4435daff4bff4539a01b584e9f026a65"
nsync = NSlack.NotionSync()
data = nsync.query_databases()
totalestimates, estimates = nsync.get_TotalEstimate(data, total_checked, rise_time, meditation, reading, run)

# Get the Morning Principles & Promises and others
DATABASE_ID = '17c79d650c064c258faf15bea07a615c'
NOTION_URL = 'https://api.notion.com/v1/databases/'
token_key = 'secret_WCXYCVzuU52uLqAdYvJZRtpnd3UD4vR1c85iPFr0n55'

nsync = NSlack.NotionSync()
morning_data = nsync.query_databases()
projects_morning = nsync.get_projects_titles(morning_data)
habits, relationship, promises = nsync.morning_principles(morning_data, projects_morning)


# Send a Message using Slack
slack = Slacker('xoxb-1725203205332-1742890574128-X8e3acTMyzOmt8X7EtHgPh8O')
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































=======
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 00:38:08 2022

@author: anddy
"""

import sys
sys.path.append('C:\\NotionUpdate\progress\Connect_NotionAPI')
import notionAPI_slack as NSlack
from slacker import Slacker
import datetime as datetime


# Morning Routine
nsync = NSlack.NotionSync()
data = nsync.query_databases()
projects = nsync.get_projects_titles(data)
projects_data,names = nsync.get_projects_data(data,projects)

total_checked = nsync.MorningRoutine(projects_data, names)[0]
meditation = nsync.MorningRoutine(projects_data, names)[1]
rise_time = nsync.MorningRoutine(projects_data, names)[2]
reading = nsync.MorningRoutine(projects_data, names)[3]
run = nsync.MorningRoutine(projects_data, names)[4]


# Compute the Estimations & Rest of the Evaluation variables
DATABASE_ID = "2bab419dd8734e899ea28fb1ec412a49"
NOTION_URL = 'https://api.notion.com/v1/databases/'
token_key = 'secret_WCXYCVzuU52uLqAdYvJZRtpnd3UD4vR1c85iPFr0n55'

DATABASE_ID = "4435daff4bff4539a01b584e9f026a65"
nsync = NSlack.NotionSync()
data = nsync.query_databases()
totalestimates, estimates = nsync.get_TotalEstimate(data, total_checked, rise_time, meditation, reading, run)

# Get the Morning Principles & Promises and others
DATABASE_ID = '17c79d650c064c258faf15bea07a615c'
NOTION_URL = 'https://api.notion.com/v1/databases/'
token_key = 'secret_WCXYCVzuU52uLqAdYvJZRtpnd3UD4vR1c85iPFr0n55'

nsync = NSlack.NotionSync()
morning_data = nsync.query_databases()
projects_morning = nsync.get_projects_titles(morning_data)
habits, relationship, promises = nsync.morning_principles(morning_data, projects_morning)


# Send a Message using Slack
slack = Slacker('xoxb-1725203205332-1742890574128-X8e3acTMyzOmt8X7EtHgPh8O')
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































>>>>>>> 572dc86 (update)
