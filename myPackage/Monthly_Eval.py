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
    sys.path.append('/Volumes/Programming/Personal/progress')
    save_path = r"/Volumes/Programming/Spring 2022/DANL 310/my_website/aLin-96.github.io/monthly_eval_images/%s"
else:
    sys.path.append(r'D:\Personal\progress')
    save_path = r"D:\Spring 2022\DANL 310\my_website\aLin-96.github.io\monthly_eval_images\%s"
    save_path_1 = r"D:\Personal\progress\jpg files\Monthly Evaluation\%s"
from myPackage import Read_Data as pRd
import std_risetime as srt
import time
from datetime import datetime
month_read = pRd.read_data()


def find_weekend_indices(datetime_array):
    indices = []
    for i in range(len(datetime_array)):
        if datetime_array[i].weekday() >= 5:
            if len(datetime_array) == i+1:
                pass
            else:
                indices.append(i+1)
    return indices

def highlight_datetimes(indices, ax, mon):
    i = 0
    while i <= len(indices)-1:
        ax.axvspan(mon.index[indices[i]-1], mon.index[indices[i]], facecolor = 'green',
                   edgecolor='none', alpha = .1, label = "Weekends")
        i += 1

def monthly_eval(mon):
    
    # Reverse month dataframe
    mon = mon.reindex(index=mon.index[::-1])

    
    # count all data for the graph
    all_dat_len = month_read.all_data('include date')[0]
    all_dat_len = len(all_dat_len['Name'])
        
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
    if '/' in mon['Name'][0] and '/' in mon['Name'][-1]:
        for d in mon['Name']:
            d = d.split('/')
            date.append(d[1][:2].strip(' '))
    else:
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
    axe[0].set_xlabel('Date', fontsize = 13)
    axe[0].set_ylabel('Productivity', fontsize= 13,alpha=.8)
    axe[0].set_xticks(date_x)
    axe[0].set_xticklabels(date)
    axe[0].set_ylim((0,np.max(tt*100)+30))
    axe[0].plot(0,-1,'r.',label = 'Drink') 
    axe[0].plot(0,-1,'w.',lw=2)        
    axe[0].plot(0,0,'g-.', label = 'Rise time', alpha=.3)
    axe[0].tick_params(axis='y', labelcolor='m')
    
    # Legends
    handles, labels = axe[0].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    axe[0].legend(by_label.values(), by_label.keys())

    
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
        
    # Get the Month's Screen Time AVG
    screen_time_avg = np.average(mon['Screen time'])
    stAVG_hour = round(screen_time_avg // 60)
    stAVG_min = round(screen_time_avg  % 60)
    screen_time_avg = str(stAVG_hour) + "hr " + str(stAVG_min) + "min"
    
    # Get the Month's Meditation AVG
    meditation_avg = np.average(mon['Meditation'])
    
    # Get the Month's Reading AVG
    reading_avg = np.average(mon['Reading'])
    
    # Monthly Average
    monthavg = np.average(mon['Total'])*100
    axe[0].text(-.03,1.1,'Month Average: %.2f'% monthavg +'%', color = 'k',fontweight = 'bold',
                            fontsize = 13, alpha = .83, transform= axe[0].transAxes)
    
    # Other Average Values (Screen time, Meditation, Reading)
    axe[0].text(.25,1.1,'Screen_time AVG: %s'% (screen_time_avg), color = 'skyblue',fontweight = 'bold',
                    fontsize = 13, alpha = .83, transform= axe[0].transAxes)
    axe[0].text(.56,1.1,'Meditation AVG: %.1fmin'% (meditation_avg), color = 'orange',fontweight = 'bold',
                    fontsize = 13, alpha = .83, transform= axe[0].transAxes)
    axe[0].text(.82,1.1,'Reading AVG: %.1fmin'% (reading_avg), color = 'red',fontweight = 'bold',
                    fontsize = 13, alpha = .6, transform= axe[0].transAxes)
    
    
    
    
    
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
        
    # Get current month & date in string format
    month_date = mon['Date'][0].strftime('%Y/%m/%d').split('/')
    month_obj = datetime.strptime(month_date[1].strip('0'), "%m")
    year_obj = datetime.strptime(month_date[0].strip('0'), "%Y")
    
    month_name = month_obj.strftime("%b")
    year_name = year_obj.strftime("%Y")
    date_title = month_name + ' ' + year_name
    
        
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle('Evaluation: ' + date_title, fontsize = 16, fontweight = 'bold')
    plt.savefig("C:\\NotionUpdate\progress\jpg files\Monthly Evaluation\month.jpg", format = 'jpg'
            , dpi=800, bbox_inches = 'tight')
    
    # If D drive is plugged in, save it in D drive as well
    
    try:
        plt.savefig(save_path % (date_title.replace(" ","") + '.jpg'), format = 'jpg'
                , dpi=800, bbox_inches = 'tight')
        plt.savefig(save_path_1 % (date_title.replace(" ","") + '.jpg'), format = 'jpg'
                , dpi=800, bbox_inches = 'tight')
    except:
        pass

