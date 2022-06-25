# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 22:12:20 2022

@author: anddy
"""
import sys
sys.path.append('C:\\NotionUpdate\\progress\\myPackage')
import NotionprocessReadData as NRD
import os, os.path


def remove_names():
    print("****************** GITHUB DATA UPDATE ******************")
    year = 20
    month = 1
    
    DIR = r'C:\NotionUpdate\progress\Data'
    
    # Subtracting 1 for all_dat.csv
    dir_len = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) - 1

    c = 1
    while True:
        file_name = str(month).zfill(2) + str(year) + '.csv'
        
        try:
            month_dat = mon.monthly(month, year)
            
            ####### Delete Name Columns #######
            month_dat = month_dat.drop(columns=["Name"])
            try:
                month_dat = month_dat.drop(columns=["Key words"])
            except KeyError:
                pass
            try:
                month_dat = month_dat.drop(columns=["Events"])
            except KeyError:
                pass
            
            month_dat.to_csv(r"C:\NotionUpdate\progress\git\notion_automation\Data\%s" % file_name, index=False)
            try:
                month_dat.to_csv(r"D:\git\self_evaluation\progress\Data\%s" % file_name, index=False)
                month_dat.to_csv(r"D:\git\self_evaluation\progress\Data\%s" % file_name, index=False)
            except:
                pass
            print("%s/%s Name column deleted & saved" % (month,year))
            c += 1
        except FileNotFoundError:
            if dir_len == c:
                print("Completed\n\n")
                break
            else:
                pass
        if month > 12:
            
            year += 1
            month = 0

        month += 1

mon = NRD.read_data()
remove_names()