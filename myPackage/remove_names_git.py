"""
Created on Mon Apr  4 22:12:20 2022
@author: anddy
"""
import sys
import os
if os.name == 'posix':
    sys.path.append('/Users/andylee/Desktop/git_prepFile/notion_automation')
    DIR = r'/Users/andylee/Desktop/git_prepFile/notion_automation/month_Data'
    filesave_path1 = r'/Users/andylee/Desktop/git_prepFile/notion_automation/month_Data/%s'
    filesave_path_all = r'/Users/andylee/Desktop/git_prepFile/notion_automation/Data/all_dat.csv'
else:
    sys.path.append('C:\\NotionUpdate\\progress')
    DIR = r'C:\NotionUpdate\progress\month_Data'
    filesave_path1 = r"C:\NotionUpdate\progress\notion_automation\month_Data\%s"
    filesave_path2 = 'D:\\git\\self_evaluation\\progress\\month_Data\\%s'
    filesave_path_all = r'C:\NotionUpdate\progress\notion_automation\Data\all_dat.csv'
from myPackage import Read_Data as NRD
"""
The purpose for this python script is to prepare the monthly csv files so that
they can be uploaded to github. The main modification includes getting rid of
the names of the daily evaluations, which can be too private to publicize.
"""

def remove_names_all():
    all_dat = mon.all_data('include date')[0]
    try:
        all_dat = all_dat.drop(columns=["Name"])
    except KeyError:
        pass
    all_dat.to_csv(filesave_path_all)

def remove_names_month():
    print("****************** GITHUB DATA UPDATE ******************")
    # Set beginning year & month (When Data Collection Began)
    year = 20
    month = 9
    # Subtracting 1 for all_dat.csv
    dir_len = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    c = 1
    while True:
        file_name = str(month).zfill(2) + str(year) + '.csv'
        try:
            month_dat = mon.monthly(month, year)
            ####### Delete Name Columns #######
            try:
                month_dat = month_dat.drop(columns=["Name"])
            except KeyError:
                pass
            try:
                month_dat = month_dat.drop(columns=["Key words"])
            except KeyError:
                pass
            try:
                month_dat = month_dat.drop(columns=["Events"])
            except KeyError:
                pass
            month_dat.to_csv(filesave_path1 % file_name, index=False)
            try:
                month_dat.to_csv(filesave_path2 % file_name, index=False)
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
remove_names_all()
remove_names_month()    
