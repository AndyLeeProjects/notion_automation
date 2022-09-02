from pprint import pprint 
import Google 

CLIENT_SECRET_FILE = r"C:\NotionUpdate\progress\notion_automation\Google_API\credentials.json"
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Google.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

page_token = None
while True:
  events = service.events().list(calendarId='anddy0622@gmail.com', pageToken=page_token).execute()
  for event in events['items']:
    try:
      print(event)
    except:
      pass
  page_token = events.get('nextPageToken')
  if not page_token:
    break


