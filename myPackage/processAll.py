# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 21:51:46 2021

@author: anddy
"""

import numpy as np
from matplotlib import pyplot as plt

def All_cor_plots(test_dict):
    # Create Names
    names = []
    for i in test_dict.keys():
        i = i.strip('Cor TEST : *')
        if 'creen time &' in i:
            i = 'S' + i
        elif 'tal &' in i or 'List &' in i:
            i = 'To' + i
        i = i.strip(' ').split('&')
        if i[0] in names:
            pass
        else:
            names.append(i[0])
    dif_cor = {}
    for i in names:
        temp_l = []
        for k,v in test_dict.items():
            temp = {}
            if i+'&' in k:
                k = k.split(' & ')
                if v[0] == 0:
                    temp[k[-1]] = float(v[0])
                else:
                    temp[k[-1]] = -float(v[0])
                temp_l.append(temp)
        dif_cor[i] = temp_l
    x = list(np.arange(1,len(names)))
    passline = [-0.05]*(len(names)-1)
    fig, axe = plt.subplots(4,3, figsize = (11,12))
    fig.tight_layout(w_pad=2, h_pad=12)
    colors = ['k','y','m','g','b','orange', 'c','m', 'y', 'k', 'g']
    titles = list(dif_cor.keys())

    c = 0
    for i in range(4):
        for j in range(3):
            t = 0
            for k,v in dif_cor.items():
                values = []
                names = []
                for l in v:
                    a = list(l.values())
                    b = list(l.keys())
                    names.append(b[0])
                    values.append(float(a[0]))
                if t == c:
                    break
                t += 1
            if c == len(names)+1:
                break
            axe[i,j].plot(x,values, colors[c])
            nc = 0
            for k in values:
                if abs(k) < 0.05:
                    names[nc] = names[nc] + ' >'
                nc +=1
            axe[i,j].set_xticks(x)
            axe[i,j].set_xticklabels(names, rotation=90, )
            axe[i,j].set_title(titles[c], fontsize = 15)
            axe[i,j].plot(x,passline, 'r', lw=.8, label = '0.05')
            axe[i,j].set_ylim((-1,.5))
            axe[i,j].legend()
                
            c += 1
    try:
        plt.savefig('/Volumes/Programming/Personal/progress/jpg files/Overall/All Correlation.jpg', format = 'jpg'
                    , dpi=1000, bbox_inches = 'tight')
    except ImportError:
        plt.savefig('D:\Personal\progress\jpg files\Overall\Alll Correlation.jpg', format = 'jpg'
                    , dpi=1000, bbox_inches = 'tight')