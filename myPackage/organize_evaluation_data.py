# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 19:03:49 2022

@author: anddy
"""
import pandas as pd
from datetime import datetime
import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

def get_evaluation_data(projects, data):
    print("Reading Evaluation Database...")
    eval_data = {}
    input_multiple = ['Social','Overall Satisfaction','Tech Consumption','Mentality',
                      'Productivity']
    input_values = ['Meditation (min)','*Phone pickups','Personal Reading','Run (km)',
                    '*Finished','Drink? (over 3 beer)','*Multiple (1~5)','Total To-do List',
                    'Rise time','*Screen time','Books finished']
    for p in projects:
        
        if p in input_multiple:
            eval_data[p] = [len(data['results'][i]['properties'][p]['select']['name'])/2
                            for i in range(len(data['results']))]    
            
        elif p == "Date":
            eval_data[p] = [data['results'][i]['properties'][p]['date']['start']
                            for i in range(len(data['results']))]
            
        elif p == "Created":
            eval_data[p] = [data['results'][i]['properties']['Created']['created_time']
                            for i in range(len(data['results']))]
            
        elif p in input_values:
            eval_data[p] = [data['results'][i]['properties'][p]['number']
                            for i in range(len(data['results']))]
            
        elif p == "Key words":
            temp = []
            for i in range(len(data['results'])):
                path = data['results'][i]['properties']['Key words']['multi_select']
                temp.append([path[row]['name']for row in range(len(path))])
            eval_data[p] = temp
                
        elif p == "Events" or p == "Name":
            temp = []
            for i in range(len(data['results'])):
                try:
                    temp.append(data['results'][i]['properties'][p]['title'][0]['text']['content'])
                except:
                    pass
                if p == "Events":
                    try:
                        temp.append(data['results'][i]['properties'][p]['rich_text'][0]['text']['content'])
                    except:
                        temp.append(0)
            eval_data[p] = temp
            
        else:
            eval_data[p] = [data['results'][i]['properties'][p]['formula']['number']
                            for i in range(len(data['results']))]

    # Reorder columns in the dataset
    eval_data = pd.DataFrame(eval_data, columns=['Name',
                                         '*Finished',
                                         '*Multiple (1~5)',
                                         '*Phone pickups',
                                         '*Screen time',
                                         'Books finished',
                                         'Created',
                                         'Date',
                                         'Drink (%)',
                                         'Drink? (over 3 beer)',
                                         'Events',
                                         'Meditation (%)',
                                         'Meditation (min)',
                                         'Mentality',
                                         'Multiple (%)',
                                         'Multiple EST',
                                         'Overall Satisfaction',
                                         'Personal Reading',
                                         'Pick up (%)',
                                         'Productivity',
                                         'Reading (%)',
                                         'Rise time',
                                         'Rise time (%)',
                                         'Run (%)',
                                         'Run (km)',
                                         'Screen Time (%)',
                                         'Social',
                                         'Tech Consumption',
                                         'Total',
                                         'Total To-do List',
                                         'Work done (%)',
                                         'Key words'])
    eval_data['Created'] = pd.to_datetime(eval_data['Created'])
    eval_data['Date'] = pd.to_datetime(eval_data['Date'])
    eval_data['Created'] = eval_data['Created'].dt.strftime('%m/%d/%Y %H:%M')
    eval_data['Date'] = eval_data['Date'].dt.strftime('%m/%d/%Y')
    print("Completed")
    print()
    return eval_data
