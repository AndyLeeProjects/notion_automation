# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:14:31 2021

@author: anddy
"""
import datetime 


def changed_risetime():
    
    
    changed_occurence = {'2021-02-01':32400,
                         '2021-06-24':28800, 
                         '2021-12-23':32400,
                         '2021-01-24':28800}
    
    
    return changed_occurence


changed_occurence = changed_risetime()

def rise_time_adjustment(dat, changed_occurence):


    dates = dat['Date'][-60:]
    dates = dates.reset_index()['Date']

    rt = dat['Rise time'][-60:]
    rt = rt.reset_index()['Rise time']
    new_rt = []
    c = 0
    changed_dates = list(changed_occurence.keys())
    changed_times = list(changed_occurence.values())
    
    initial_standard_time = changed_times[0]
    
    
    for i in range(len(dates)):
        for c in range(len(changed_dates)):
            if '/' in dates[i]:
                try:
                    datetimeobj = datetime.datetime.strptime(dates[i], '%m/%d/%Y')
                except:
                    datetimeobj = datetime.datetime.strptime(dates[i], '%m/%d/%y')
                    print(datetimeobj)
                date = datetimeobj.strftime('%Y-%m-%d')
            else:
                date = dates[i]
                
            try:
                if changed_dates[c] < date < changed_dates[c+1]:
                    time_diff = changed_times[c] - initial_standard_time # If new st is 8:00, it would be 8:00 - 9:00 = -60 min
                    new_rt.append(rt[i] + time_diff/60)
            except:
                if changed_dates[c] < date :
                    time_diff = changed_times[c] - initial_standard_time # If new st is 8:00, it would be 8:00 - 9:00 = -60 min
                    new_rt.append(rt[i] + time_diff/60)
            
    
    

    return new_rt












