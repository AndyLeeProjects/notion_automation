#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:14:50 2021

@author: andylee
"""

import os, sys
sys.path.append('C:\\NotionUpdate\\progress\\myPackage')
import NotionprocessMonth as pMon
import NotionprocessReadData as NReadData
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import selenium.common.exceptions as CE
import calendar
sys.path.append('C:\\NotionUpdate\progress')
from Connect_NotionAPI import Notion_Schedular as Schedular
from Connect_NotionAPI import numpy as np
from Connect_NotionAPI import NotionUpdate_API as NAPI
import pandas as pd
from secret import secret
#import notionAPI_slack as Nslack


class Notion_Automation:
    def __init__(self):
        pass
    
    # Closes Popups if they occur
    def closePopUps(driver):
        try:
            alert_obj = driver.switch_to.alert
            alert_obj.accept()
        except:
            pass
        
    # With 2 inputted time, it checks if the current time is between the inputted times
    def is_time_between(self, begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.now().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else: # crosses midnight
            return check_time >= begin_time or check_time <= end_time
    

        
    def Update_Schedule(self, driver):                                                    
        WebDriverWait(driver,6).until(EC.presence_of_element_located((By.XPATH,'//*[@id="notion-app"]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[7]/div/div')))
        
        # Set dates & weekdays variables for scheduling
        week_days = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
        year = int(datetime.today().strftime('%Y'))
        month = int(datetime.today().strftime('%m'))
        day = int(datetime.today().strftime('%d'))
        week_day_num = calendar.weekday(year,month,day)
        today = week_days[week_day_num]
        row = 2
        col = 1
        
        # Date for today
            # To check every block if they match today's date or week day
        now = datetime.today()
        dt_string = now.strftime("%Y-%m-%d")
        
        data = Schedular.nsync.query_databases()
        projects = Schedular.nsync.get_projects_titles(data)
        projects_data = Schedular.nsync.get_projects_data(data,projects)
        count = 0
        
        # make it sleep 2 seconds and get the correct path using while loop
        time.sleep(2)
        task_block_xpath = '//*[@id="notion-app"]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[11]/div[2]/div/div[2]/div/div/div[2]/div[2]'
        while True:
            while True:
                if count >= len(data['results']):
                    break
                print('col: ', col, 'row: ', row)
                print(count)
                try:
                    count += 1                                                              
                    
                    WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, task_block_xpath + '/div[%d]/div[%d]/a/div'%(col,row))))
                    block = driver.find_element_by_xpath(task_block_xpath + '/div[%d]/div[%d]/a/div'%(col,row))
                    try:                                     
                        name = driver.find_element_by_xpath(task_block_xpath + '/div[%d]/div[%d]/a/div/div[2]'%(col,row))
                    except:
                        count -=1
                        break
                    print('***************************')
                    print(name.text)
                    # Get Index where the name matches the schedular Name dictionary
                    index_loc = np.where(np.array(projects_data['Name']) == name.text)[0][0]
    
                    print('Current Status: ',projects_data['Status 1'][index_loc])     
                    print('Days Repeated: ', projects_data['Date'][index_loc])
                    if projects_data['Date'][index_loc] == [] and \
                        projects_data['Due Date'][index_loc] == 0:
                        raise ValueError('Skip Row')
                    else:
                                        
                        status_xpath = '//*[@id="notion-app"]/div/div[2]/div[2]/div/div[2]/div[3]/div[1]/div[2]/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div[2]/div'
                        status_list_xpath = '//*[@id="notion-app"]/div/div[2]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[%d]/div/div/div[2]'
                        
                        if today in projects_data['Date'][index_loc] and \
                        projects_data['Status 1'][index_loc] == 'Today':
                            pass
                        
                        # DO NOT NEED to be 'Today', but it is 
                        elif today not in projects_data['Date'][index_loc] and \
                        projects_data['Status 1'][index_loc] == 'Today':
                            
                            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, task_block_xpath + '/div[%d]/div[%d]'%(col,row))))
                            block.click() 
    
                            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, status_xpath)))
                            status = driver.find_element_by_xpath(status_xpath)
                            status.click()
    
                            title = projects_data['Name'][index_loc].split(':')[0]
                            print(title)
    
                            c = 1
                            while True:                                                                 
                                                                                                        
                                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, status_list_xpath%c)))
                                s = driver.find_element_by_xpath(status_list_xpath%c)
                                print('s.text & name: ', s.text, title)
                                if s.text == title:
                                    s.click()
                                    break
    
                                c += 1
    
                            projects_data['Status 1'][index_loc] = title
                            print('\nSuccessfully Adjusted to %s!' % title)
                            row -= 1
                            count -= 1
                            time.sleep(.1)
                            driver.back()
                            
                        # NEEDS to be 'Today', but it is not
                        elif (today in projects_data['Date'][index_loc] and \
                        projects_data['Status 1'][index_loc] != 'Today') or \
                        projects_data['Due Date'][index_loc] == dt_string:
                            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, task_block_xpath + '/div[%d]/div[%d]'%(col,row))))
                            block.click()                                                                   
                            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, status_xpath)))
                            status = driver.find_element_by_xpath(status_xpath)
                            status.click()
                            c = 1
                            while True:
                                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, status_list_xpath%c)))
                                s = driver.find_element_by_xpath(status_list_xpath%c)
                                if s.text == 'Today':
                                    break
                                c += 1
                            s.click()
                                
                            projects_data['Status 1'][index_loc] = 'Today'
                            print('\nSuccessfully Adjusted to Today!')
                            row -= 1
                            time.sleep(.1)
                            driver.back()
                        else:
                            pass
                    
                except CE.TimeoutException:
                    count -= 1
                    # Tmeout exception occurs when finished reading each COLUMN
                    break
                except:
                    # exception occurs when 
                    pass
                print()
                row += 1
            row = 2
            col += 1
            if count >= len(data['results']):
                    break
            
    
    def Notion_login(self, driver):
        import time
        #driver = webdriver.Chrome('C:\\NotionUpdate\\progress\\chromedriver.exe')
        driver.get("https://www.notion.so/ko/login")
        driver.maximize_window()
    
        # ID
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="notion-email-input-1"]')))
        driver.find_element_by_xpath('//*[@id="notion-email-input-1"]').click()
        username = driver.find_element_by_xpath('//*[@id="notion-email-input-1"]')
        username.send_keys(secret.notion_login("username"))
    
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="notion-app"]/div/div[1]/main/section/div/div/div/div[2]/div[3]/form/div[4]')))
        driver.find_element_by_xpath('//*[@id="notion-app"]/div/div[1]/main/section/div/div/div/div[2]/div[3]/form/div[4]').click()
    
        # Password
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="notion-password-input-2"]')))
        password = driver.find_element_by_xpath('//*[@id="notion-password-input-2"]')
        password.send_keys(secret.notion_login("username"))
        time.sleep(.9)
        
        # Log in 
        ActionChains(driver).send_keys(Keys.ENTER)
        login_button = driver.find_element_by_xpath('//*[@id="notion-app"]/div/div[1]/main/section/div/div/div/div[2]/div[3]/form/div[4]')
        login_button.click()
        time.sleep(3)
        try:
            for i in range(5):
                login_button.click()
        except:
            pass
    
    
    def Notion_Home_Update(self, driver):
        from datetime import time as time_time
        
        # Do not update schedule between 11:59am to 23:59pm
            # Because it can mess up the finalized tasks
        if NAuto.is_time_between(time_time(11,59),time_time(23,59)) == True:
            pass
        else:
            NAuto.Update_Schedule() 
        
    
        
        # Modify & Write in the number of Total To-do list
        data = Schedular.nsync.query_databases()
        projects = Schedular.nsync.get_projects_titles(data)    
        projects_data = Schedular.nsync.get_projects_data(data,projects)
        
        todo_count = projects_data['Status 1'].count('Today') + 6

        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="notion-app"]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[7]/div/div')))
        total_todo = driver.find_element_by_xpath('//*[@id="notion-app"]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[7]/div/div')
        total_todo.click()     
                     
        if len(total_todo.text) == 20:
            total_todo.send_keys(Keys.BACKSPACE+Keys.BACKSPACE)
        else:
            total_todo.send_keys(Keys.BACKSPACE)
        total_todo.send_keys(todo_count)


    
    def Notion_Evalpage_Update(self, driver):
        # Go to Evaluation Page
        evaluation_page_url = "https://www.notion.so/andyhomepage/103aadb3035f470f88e33801328c0f34?v=d9973f85ed534a7cbab33b57e0645c3b"
        driver.get(evaluation_page_url)
        time.sleep(4)
    
        ActionChains(driver).send_keys(Keys.ENTER)
        time.sleep(4)
        ActionChains(driver).send_keys(Keys.ENTER)
        driver.get(evaluation_page_url)
            
    
    def Notion_Evalpage_exportCSV(self, driver):
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="notion-app"]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div')))
        # Export CSV        
        driver.find_elements_by_css_selector('.dots')[0].click()                                                        
        WebDriverWait(driver,2.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="notion-app"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[1]/div[3]/div[2]/div')))                         
        driver.find_element_by_xpath('//*[@id="notion-app"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[1]/div[4]/div[1]/div').click()
        time.sleep(.8)               
        print('Downloading the csv file...')
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="notion-app"]/div/div[2]/div[2]/div/div[2]/div/div[4]/div[2]')))
        driver.find_element_by_xpath('//*[@id="notion-app"]/div/div[2]/div[2]/div/div[2]/div/div[5]/div[2]').click()
        time.sleep(6)
        print('Completed')
    
    
    def Delete_Unnecesary_Files(self):
        path = 'C:\\Users\\anddy\\Downloads'
        os.chdir(path)
    
    
        # Find the most recent file
        recent = [1,0]
        index = 0
        all_exports = []
        
        # There may be multiple zip files, so get the most recent file
        for item in os.scandir(path):
            if 'Export-' in item.name:
                fileInfo = [item.name, item.path, item.stat().st_size, item.stat().st_atime]
                temp =  item.stat().st_atime
    
                all_exports.append(fileInfo)
                if float(recent[0]) < float(temp):
                    recent.pop(0)
                    recent.pop(0)
                    recent.append(temp)
                    recent.append(index)
                index += 1
    
    
        path_to_zip_file = all_exports[recent[1]][1]
        if '.crdownload' in path_to_zip_file:
            path_to_zip_file = path_to_zip_file.replace('.crdownload','')
        
        # Export the zip file to two separate folders 
        directory_to_extract = [r'C:\NotionUpdate\progress\Data','D:\Personal\progress\Data']
        # Unzip File
        import zipfile
        for directory in directory_to_extract:
            # Check if the D drive is plugged in. If not, pass
            try:
                os.chdir(directory)
            except:
                break
            time.sleep(4)
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref: # from
                zip_ref.extractall(directory) # to 
        
            # Change Directory to the Unzipzzed Folder
            os.chdir(directory)
        
            # Rename the file 
            month = datetime.today().strftime('%m')
            year = datetime.today().strftime('%Y')[2:]
            new_fileName = month + year + '.csv'
    
            for i in os.listdir():
                i = i.split('.')
                if ' ' in i[0]:
                    origName = i[0] + '.' + i[1]
        
            try:
                os.rename(origName,new_fileName)
            except FileExistsError:
                os.remove(new_fileName)
                os.rename(origName,new_fileName)
    
        # Delete the Downloaded Zip File (Don't need it anymore since unzipped to Data Folder)
        os.chdir(path)
        os.remove(path_to_zip_file.split('\\')[-1])
        print()
        print('Unnecessary Files Deleted')
        print()
        print('Monthly Evaluation Function Running...')
    
        # Wait until the program stops running
        os.chdir("C:\\NotionUpdate\\progress\\jpg files\\Monthly Evaluation")
    
    def Notion_Home_jpgUpdate(self, driver):
        # Go back home for a visualization update
        driver.get("https://www.notion.so/andyhomepage/Home-4c8126a86ee7449597275f600cc2b51b")
            
        data_eval = NAPI.nsync.query_databases()
        projects_eval = NAPI.nsync.get_projects_titles(data_eval)
        projects_data_eval = pd.DataFrame(NAPI.nsync.get_projects_data(data_eval,projects_eval))
        projects_data_eval = projects_data_eval.rename(columns={'*Finished': 'Finished', '*Multiple (1~5)': 'Multiple','*Phone pickups':'Phone pickups',
                                       '*Screen time':'Screen time','Drink (%)':'Drink %', 'Drink? (over 3 beer)':'Drink',
                                       'Meditation (%)':'Meditation %', 'Meditation (min)':'Meditation', 'Multiple (%)':'Multiple %',
                                       'Pick up (%)':'Pick up %', 'Reading (%)':'Reading %', 'Rise time (%)':'Rise time %',
                                       'Run (%)':'Run %', 'Run (km)':'Run', 'Screen Time (%)':'Screen Time %', 'Work done (%)': 'Work done %',
                                       'Overall Satisfaction':'Satisfaction','Personal Reading':'Reading','Tech Consumption':'Tech',
                                       'Total To-do List':'Tot To-do', 'Phone pickups':'Pickups'})

        # Monthly Evaluation Plot
        pMon.monthly_eval(projects_data_eval) # Replace it with projects_data_eval
        NAPI.uploadEvaluationJPG()
        print()
        print('Self Evaluation JPG Uploaded')
        
        # Export all_dat to csv for further analysis in Rstudio 
        mon = NReadData.read_data()
        all_data = pd.DataFrame(mon.all_data('RSTUDIO')[0])
        try:
            all_data.to_csv('D:/Spring 2022/Project/all_dat.csv')
            print()
            print('all_dat updated to D drive')
        except:
            # This occurs when I don't have my usb plugged in
            pass
        
        time.sleep(1)
        print()
        print('Update Completed')
        time.sleep(2)
        driver.quit()
    
    
        


driver = webdriver.Chrome('C:\\NotionUpdate\\progress\\chromedriver.exe')
NAuto = Notion_Automation()

# Login to the home page 
NAuto.Notion_login(driver)

# Make Modifications in the home page
    # Schedule my to-do lists for today
    # Change the total # of to-do lists
NAuto.Notion_Home_Update(driver)

# Go to Evaluation Page
    # Download CSV file
NAuto.Notion_Evalpage_Update(driver)
NAuto.Notion_Evalpage_exportCSV(driver)

# Delete Unnecesary files including just downloaded ones 
NAuto.Delete_Unnecesary_Files()

# Go back to the Home page & Update the visualization
NAuto.Notion_Home_jpgUpdate(driver)














