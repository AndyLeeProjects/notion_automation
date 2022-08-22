# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:31:41 2021

@author: anddy
"""
    
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os, sys
if os.name == 'posix':
    sys.path.append('/Volumes/Programming/Personal/progress/myPackage')
else:
    sys.path.append('C:\\NotionUpdate\\progress\\notion_automation\\myPackage')
import Read_Data as pRd
import std_risetime as srt
import time
from datetime import datetime
month_read = pRd.read_data()


    
def risetime_Goal(avg_time):
    rt_goal = 0
    # Set up a correct rise time limit
    changed_occurence = srt.changed_risetime()
    a = list(changed_occurence.values())
    limit = (a[-1] - a[0])/60
    
    
    if avg_time - (avg_time**2)/280 > limit:
        rt_goal = avg_time - (avg_time**2)/280
    else:
        rt_goal = limit
    return rt_goal

    
def wakeupStreak():
    all_dat = month_read.all_data('include date')[0]
    
    changed_occurence = srt.changed_risetime()
    risetime = srt.rise_time_adjustment(all_dat, changed_occurence)
    
    rise_streak = []
    rt_3 = risetime[-30:]
    rt_3.reverse()
    risetime.reverse()
    
    # First, find the average Rise time of last 30 data
    rt_3_avg = np.average(rt_3) # Avg Rise of past 30 days
    

    
    # Set the correct time limit 
    changed_limits = list(changed_occurence.values())
    newest_limit = changed_limits[-1] / 3600
    new_limit = (9 - newest_limit) * -60
        
    for day in range(len(risetime)):
        
        # if my risetime average is below standard(goal) rise time, then
        # set the streak limit as 0
            # If the average is too low, just set the limit to 0 (standard time)
            # so that it won't be keep going down
        if risetime_Goal(np.average(risetime[day+1:day+32])) >= new_limit:
            limit = risetime_Goal(np.average(risetime[day+1:day+32]))
        else:
            limit = new_limit
        
        if risetime[day] > limit: # Set up time standard
            break
        else:
            rise_streak.append(day)
    total_streak = []
    totals = list(np.array(all_dat['Total'])*100)
    tt_3 = totals[-30:]
    totals.reverse()
    tt_3_avg = np.average(tt_3)
    
    
    def total_Goal(avg_tt):
        return avg_tt + 6.5-(avg_tt**2)/1000
    
    for day in range(len(totals)):
        # each total element has to be greater than or equl to the average 
        # of 30 days from that element's point
            # This prevents inaccuracy of the streak when it does not hold 
            # the value it once did just because the standard went up
            
        
        # Set a limit to 75% : values over 75 gets automatically stored in total_streak
        if total_Goal(np.average(totals[day+1:day+32])) > 75:
            if totals[day] < 75:
                break
        else:
            if totals[day] < total_Goal(np.average(totals[day+1:day+32])):
                break
            
        total_streak.append(day)
    
    # Set the streak(%) limit to 75%
    if total_Goal(tt_3_avg) > 75:
        total_visual = 75
    else:
        total_visual = total_Goal(tt_3_avg)
    
    return len(rise_streak), len(total_streak), risetime_Goal(rt_3_avg), total_visual

def find_weekend_indices(datetime_array):
    indices = []
    for i in range(len(datetime_array)):
        if datetime_array[i].weekday() >= 5:
            indices.append(i)
    return indices

def highlight_datetimes(indices, ax, mon):
    i = 0
    while i <= len(indices)-1:
        if indices[i] == 0:
            ax.axvspan(mon.index[indices[i]], mon.index[indices[i]+1], facecolor = 'green',
                       edgecolor='none', alpha = .05 , label = "Weekends")
        else:
            ax.axvspan(mon.index[indices[i]-1], mon.index[indices[i]], facecolor = 'green',
                       edgecolor='none', alpha = .05 , label = "Weekends")
        i += 1


def monthly_eval(mon, update_window):
    
    # count all data for the graph
    all_dat = month_read.all_data('include date')[0]
    all_dat_len = len(all_dat['Date'])
        
    changed_occurence = srt.changed_risetime()
    rt = srt.rise_time_adjustment(mon, changed_occurence)
    
    # rt2: plot 1
    rt2 = np.array(srt.rise_time_adjustment(mon, changed_occurence))
    
    # Divide in order for it to fit into the graph
    divgraph = 3
    rt2 = list(rt2/divgraph)
    fig, axe = plt.subplots(2,1, figsize = (12,9), gridspec_kw={'height_ratios': [2, 1]})
    fig.tight_layout(h_pad = 6)

    # Set up time range
    if min(rt) > 0:
        start_p = 0
    elif min(rt) < 1:
        start_p = min(rt)      
    if max(rt) > 240:
        end_p = max(rt)
    elif max(rt) < 241:
        end_p = 240
    
    rt_bin = np.linspace(start_p,end_p, 8)
    
    
    beg_time = 32400 + start_p*60
    end_time = 32400 + end_p*60
    interval = (end_time-beg_time)/ 6
    interval = interval - (interval%300)
    
    # Set Time values for the Histogram
    Rtime = []
    for i in rt_bin:
        Rtime.append(str(time.strftime('%H:%M',time.gmtime(i*60+32400))))
    
    # figure out each values in rise time hist == t_vals
    c = []
    t_vals = []
    cc = 1

    for i in rt_bin:
        for j in rt:
            try:
                if float(i) <= float(j) <= float(rt_bin[cc]):
                    c.append(j)
            except:
                pass
        cc+=1
        t_vals.append(len(c))
        c = []
    
    # write in the values
    for j in range(len(rt_bin)):
        if t_vals[j] == 0:
            pass
        else:
            axe[1].text(rt_bin[j]+11, t_vals[j]+.5, t_vals[j], color = 'r')
    
    # Set up date for xticklabels
    date = []
    
    try: 
        if '/' in mon['Name'][0] and '/' in mon['Name'][-1]:
            for d in mon['Name']:
                d = d.split('/')
                date.append(d[1][:2].strip(' '))
    except:
        for d in mon['Date']:
            if '-' in d:
                d = d.split('-')
                date.append(d[2][:2])
            else:
                d = d.split('/')
                date.append(d[1][:2].strip(' '))
                
    # Get Weekend indices and highlight Weekeends
    mon['Date'] = pd.to_datetime(mon['Date'])
    weekend_indices = find_weekend_indices(mon['Date'])
    highlight_datetimes(weekend_indices, axe[0], mon)
                    
    # Plot Histogram
    axe[1].hist(rt, rt_bin, color = 'orange', width = 26)
    axe[1].set_ylim((0,max(t_vals)+3))
    axe[1].set_title('Rise Time Histogram', fontsize = 15, fontweight = 'bold')
    axe[1].set_xlabel('Time', fontsize = 13)
    axe[1].set_ylabel('occurence', fontsize = 13)
    axe[1].set_xticks(np.linspace(start_p,end_p,8))
    axe[1].set_xticklabels(Rtime)
    axe[1].text(.75,-.9,'(%d) Last Updated: ' % all_dat_len + datetime.now().strftime('%Y-%m-%d %H:%M')    , color = 'k',fontweight = 'bold',
                            fontsize = 9, alpha = .83, transform= axe[0].transAxes)
    # Add Average wake up time
    avgRT = np.sum(rt)/len(rt)
    avgRT_time = str(time.strftime('%H:%M',time.gmtime(avgRT*60+32400)))
    axe[1].text(avgRT, max(t_vals)+2,'*avg RT: '+avgRT_time+'*',color='red',alpha=.8)
    for i in range(max(t_vals)+2):
        axe[1].text(avgRT, i,'|',color='red',alpha=.5)
        
    # Plot Rise time 
    # set y limits
    ylimits = np.linspace(start_p,end_p,6)
    ylim = []
    for i in ylimits:
        ylim.append(time.strftime('%H:%M',time.gmtime(i*60 + 32400)))
    axe0 = axe[0].twinx()
    axe0.plot(rt2,'g-.', label = 'Rise time (m)+', alpha=.3)
    axe0.set_ylim((min(rt2),max(rt2)+20))
    axe0.set_ylabel('Rise Time', fontsize = 13,alpha=.8)
    axe0.yaxis.set_label_position("right")
    axe0.set_yticks(ylimits/divgraph)
    axe0.set_yticklabels(ylim)
    axe0.tick_params(axis='y', labelcolor='green')
    
    # Meditation
    m = list(mon['Meditation'])
    x_positions = np.arange(0,len(m))
    axe[0].bar(x_positions,m, color ='orange', label = 'Meditation (m)', alpha = .5)
    
    # Personal Reading
    pr = np.array(mon['Reading'])
    x_positions = np.arange(0,len(pr))
    axe[0].bar(x_positions,pr, color = 'red', label = 'Reading (m)', alpha = .5)

    # total
    tt = np.array(list(mon['Total']))
    tt = np.around(tt,3)
    date_x = np.arange(0,len(tt))
    axe[0].plot(tt*100, 'm', lw=2, alpha = .3, label = 'Total (%)')
    axe[0].set_title('Total %', fontsize = 15, fontweight = 'bold')
    axe[0].set_xlabel('Date', fontsize = 13)
    axe[0].set_ylabel('Productivity', fontsize= 13,alpha=.8)
    axe[0].set_xticks(date_x)
    axe[0].set_xticklabels(date)
    axe[0].set_ylim((0,np.max(tt*100)+25))
    axe[0].plot(0,-1,'r.',label = 'Drink') 
    axe[0].plot(0,-1,'w.',lw=2)        
    axe[0].plot(0,0,'g-.', label = 'Rise time', alpha=.3)
    axe[0].tick_params(axis='y', labelcolor='m')
    
    
    # Legends
    handles, labels = axe[0].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    axe[0].legend(by_label.values(), by_label.keys(), ncol=len(by_label.keys()))
    
    # Days I drank
    dk = np.array(list(mon['Drink']))
    for i in range(len(dk)):
        if dk[i] > 0:
            axe[0].plot(date_x[i],tt[i]*100,'r.',lw=3)           
    
    # Personal Reading - Books Finished
    bf = mon['Books finished']
    for i in range(len(bf)):
        if bf[i] == 1.0 and len(bf)> 20:
            axe[0].text(date_x[i],pr[i]-3.5,'Done', color = 'whitesmoke',horizontalalignment='center',fontsize=7.5,alpha=.7)
        elif bf[i] == 1.0 and len(bf) < 21:
            axe[0].text(date_x[i],pr[i]-3.5,'Done', color = 'whitesmoke',horizontalalignment='center',fontsize=9,alpha=.7)
        else:
            pass
        
        
    # Streaks
        # if input month is not a current month, don't apply streak
        # if the streak is 0, don't apply streak
    try:
        Rstreak, Tstreak, avg_3, tt_3 = wakeupStreak() 
        tt_3 = int(tt_3)
        # - Rise time streak
        # - Total streak
        # - avg rise time for the past month
        # - avg total for the past month
        # - Find the exact time for average avg_3
        
        
        
        
        # In order to determine the limit, we need to see the average
        # of date from most recent to -31.
        # Then we use the limit that was used above to set up the streak

        a = list(changed_occurence.values())
        changed_limits = list(changed_occurence.values())
        newest_limit = changed_limits[-1] / 3600
        new_limit = (9 - newest_limit) * -60

        if avg_3 > new_limit:
            limit = avg_3
        else:
            limit = new_limit        
        rt_goal = str(time.strftime('%H:%M',time.gmtime(limit*60 + a[0])))
        
        # Rise streak alignment
        if update_window == True:
            x_ali = .66
        elif len(str(Rstreak)) > 1:
            x_ali = .57
        else:
            x_ali = .58
            
        axe[0].text(x_ali,1.1,'Rise streak(%s): %d'% (rt_goal,Rstreak), color = 'green',fontweight = 'bold',
                        fontsize = 13, alpha = .83, transform= axe[0].transAxes)
        axe[0].text(.8,1.1,'Total streak(%d%%): %d'% (tt_3,Tstreak), color = 'magenta',fontweight = 'bold',
                        fontsize = 13, alpha = .83, transform= axe[0].transAxes)
    except KeyError:
        pass       
    
    # Monthly Average
    monthavg = np.average(mon['Total'])*100
    axe[0].text(0,1.1,'Current Average: %.2f'% monthavg +'%', color = 'k',fontweight = 'bold',
                            fontsize = 13, alpha = .83, transform= axe[0].transAxes)
    
    # Write in minutes for Personal Reading > 100
    c = 0
    for i in mon['Reading']:
        if i > 130:
            axe[0].text(date_x[c], 90, int(i), horizontalalignment = 'center', color = 'white')
        c += 1
    # Write in Percentage 
    for j in range(len(tt)):
        # Special Events
        try:
            events = []
            for i in mon['Events']:
                try:
                    int(i)
                    events.append('')
                except:
                    if ' ' in i:
                        i = i.replace(' ','\n')
                    else:
                        pass
                    events.append(i)
            # Special Events
            axe[0].text(date_x[j], round(tt[j]*100,2)+5.7 ,events[j],horizontalalignment = 'center',color = 'blue' ,fontsize=7.5, alpha=.7)
        except:
            pass
        #if len(tt) > 27:    # Over 27 days could make the graph cramp
        #    if tt[-1] == tt[j]:
        #        axe[0].text(date_x[j], round(tt[j]*100,2)+2, round(tt[j]*100,2), horizontalalignment = 'center' ,color = 'k')
        #    elif np.abs(tt[j+1]-tt[j]) > 0.015:
        #        axe[0].text(date_x[j], round(tt[j]*100,2)+2, round(tt[j]*100,2), horizontalalignment = 'center' ,color = 'k')
        #else:    
        axe[0].text(date_x[j], round(tt[j]*100,2)+2, round(tt[j]*100,2), horizontalalignment = 'center' ,color = 'k')
        fig.subplots_adjust(bottom=0.2) # or whatever
    
    # This size is tailored for window laptop background size
    fig.set_size_inches(18.5, 10.5)
    
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    fig.suptitle('Evaluation: '+datetime.today().strftime('%m/%d') + ' [' + week[datetime.today().weekday()] + ']', fontsize = 16, fontweight = 'bold')
    plt.savefig("C:\\NotionUpdate\progress\jpg files\Monthly Evaluation\month.jpg", format = 'jpg'
            , dpi=1000, bbox_inches = 'tight')

