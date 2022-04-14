# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 22:12:20 2022

@author: anddy
"""
import sys
sys.path.append('C:\\NotionUpdate\\progress\\myPackage')
import NotionprocessReadData as NRD

year = 20
month = 1
mon = NRD.read_data()

while True:
    file_name = str(month).zfill(2) + str(year) + '.csv'
    
    try:
        month_dat = mon.monthly(month, year)
        
        ####### Delete Name Columns #######
        month_dat = month_dat.drop(columns=["Name"])
        
        month_dat.to_csv(r"C:\NotionUpdate\progress\git\notion_automation\Data\%s" % file_name, index=False)
        try:
            month_dat.to_csv(r"D:\git\self_evaluation\progress\Data\%s" % file_name, index=False)
        except:
            pass
        print("Name column deleted")
    except FileNotFoundError:
        pass
    if month > 12:
        year += 1
        month = 0
    if month == 4 and year == 22:
        break
    month += 1
    
    