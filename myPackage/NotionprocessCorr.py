# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:38:22 2021

@author: anddy
"""


from scipy.stats import pearsonr
import numpy as np
import sys
sys.path.append('D:\Personal\progress\myPackage')
from matplotlib import pyplot as plt


#%%
def correlation_test(x,y,name1,name2):
    # Example of the Pearson's Correlation test
    A = ''
    stat, p = pearsonr(x,y)
    A += '\nCor TEST : %s & %s' % (name1, name2)
    A += '\nstat=%.3f, p=%.5f' % (stat, p)
    if p > 0.05:
        A += '\nProbably independent'
    elif p > 0.3:
        A += '\nIndependent'
    elif p < 0.001:
        A += '\nDependent'
    else:
        A += '\nProbably dependent'
    return A

#%%
def getTotal(x):
    all_dat = {}
    for i in x[-1].keys():
        for j in x:
            if i not in j:
                pass
            else:
                all_dat.setdefault(i, [])
                all_dat[i] += j[i]
    return all_dat

'''
Correlations of -1 or +1 imply an exact linear relationship.
    Positive correlations imply that as x increases, so does y. Negative
    correlations imply that as x increases, y decreases.
'''

#%%
def combine_dataframes(x):
    all_dat = {}
    for i in x[-1].keys():
        for j in x:
            if i not in j:
                pass
            elif 'Drink' in j[i]: # Error in Drink variable so pass 
                pass
                
            else:
                all_dat.setdefault(i, [])
                # Since j comes as a dataframe format, need to change into a list format
                all_dat[i] += list(j[i]) 
    return all_dat

#%%
'''
                                [Correlation Test Setup]
'''

def DeleteUnnecessaryVar(data,purpose):
    if 'include date' in purpose:
        deleteKeys = ['Finished','Meditation %','Multiple %',
                  'Rise time %','Screen time %','Pick up %',
                  'Drink %', 'Reading %', 'Books finished',
                  'Run %', 'Events','Screen Time %','Multiple EST']
    elif 'RSTUDIO' == purpose:
        deleteKeys = ['Meditation %','Multiple %',
                  'Rise time %','Screen time %','Pick up %',
                  'Drink %', 'Reading %', 'Books finished',
                  'Run %', 'Events','Screen Time %','Multiple EST']
    else:
        # Omit Date, since it only will be needed for monthly dependency
        deleteKeys = ['Date','Finished','Meditation %','Multiple %',
                  'Rise time %','Screen time %','Pick up %',
                  'Drink %', 'Reading %', 'Books finished',
                  'Run %', 'Events','Screen Time %', 'Multiple EST']

    for item in deleteKeys:
        try:
            del data[item]
        except:
            pass
    return data

def CorSetUp(months_key, purpose):
    all_dat = combine_dataframes(months_key)
    
    # If the size don't match, make the difference 0
    for i in all_dat.keys():
        if len(all_dat[i]) != len(all_dat['Name']):
            all_dat[i] = [0]*(len(all_dat['Name'])-len(all_dat[i]))+all_dat[i]
    
    
    # Delete unimportant, redundant factor 
    
    all_dat = DeleteUnnecessaryVar(all_dat, purpose)
    return all_dat

#%%
'''
                                [Pearson's Test]
'''
def PearsonTest(all_dat):
    names = list(all_dat.keys())
    values = list(all_dat.values())
    test_results = []
    r = 0
    c = 0
    del all_dat['Drink? (over 3 beer)'][-1]
    all_dat['Drink? (over 3 beer)'].insert(0,0)
    for i in values:
        for j in values:
            if np.all(i == j):
                pass
            elif type(i[0]) == type('s') or type(j[0]) == type('s'):
                pass
            elif len(i) != len(j):
                if len(i) > len(j):
                    n = len(i)-len(j)
                    i = i[n:]
                    test_results.append(correlation_test(i,j,names[c], names[r] ))
                elif len(i) < len(j):
                    n = len(j)-len(i)
                    j = j[n:]
                    test_results.append(correlation_test(i, j,names[c], names[r] ))
                else:
                    test_results.append(correlation_test(i, j,names[c], names[r] ))
            else:
                test_results.append(correlation_test(i, j,names[c], names[r] ))
        
            r += 1
        c +=1
        r = 0

    tests = ''
    for i in test_results:
        i = i.split('\n')
        tests += i[0]+'\n'+i[1]+'\n'+i[2] +'\n'
    
    test_order = []
    c = 1
    # Arange all the correlation values in order
    for k in test_results:
        test = k.split('\n')
        del test[0], test[-1]
        values = test[-1].split(',')
        p_val = values[1].split('=')
        stat = values[0].split('=')
        test_order.append(test[0])
        test_order.append([p_val[-1], stat[-1]])
    
    test_dict = {}
    c = 1
    for i in test_order:
        if 'Cor' in i:
            test_dict[i] = test_order[c]
            c += 2
        
    dep_cor = {}
    for k,v in test_dict.items():
        if float(v[0]) < 0.05 and 'total' not in k:
            dep_cor[k] = v
    output = [dep_cor, test_dict]
    return output


#%%
'''
                                [Plot ALL Correlations]
'''
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
    colors = ['k','y','m','g','b','orange', 'c','m', 'y', 'k', 'g','b']
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
            try: 
                axe[i,j].plot(x,values, colors[c])
            except IndexError:
                pass
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
    except FileNotFoundError:
        plt.savefig('D:\Personal\progress\jpg files\Overall\Alll Correlation.jpg', format = 'jpg'
                , dpi=1000, bbox_inches = 'tight')


#%%
'''
                    [Plot Evaluation by Days (Dependent variables)]
'''

# Tests for correlation in data of monthly scope
def dep_cor_M(M):
    months = []
    DeleteUnnecessaryVar(M,'include date')
    names = list(M.keys())
    values = list(M.values())
    results = []
    r = 0
    c = 0
    if 'Date' in M.keys():
        month = int(M['Date'][0][0:2].strip('/'))
    else:
        month = int(M['Name'][0][0:2].strip('/'))
    if len(str(month)) < 2:
        months.append('0'+str(month))
    else:
        months.append(month)
    for i in values:
        for j in values:                
            if np.all(i == j):
                pass
            elif type(i[0]) == type('s') or type(j[0]) == type('s'):
                pass
            elif np.all(np.array(i)==0) or np.all(np.array(j)==0):
                pass
            elif len(i) != len(j):
                if len(i) > len(j):
                    n = len(i)-len(j)
                    i = i[n:]
                    results.append(correlation_test(i,j,names[c], names[r] ))
                elif len(i) < len(j):
                    n = len(j)-len(i)
                    j = j[n:]
                    results.append(correlation_test(i, j,names[c], names[r] ))
                else:
                    results.append(correlation_test(i, j,names[c], names[r] ))
            else:
                results.append(correlation_test(i, j,names[c], names[r] ))
        
            r += 1
        c +=1
        r = 0
    dep_M = {}
    for i in results:
        i = i.split('\n')
        del i[0]
        del i[2]
        value =  i[1].split(',')
        if float(value[1].strip(' p=')) < 0.05:
            dep_M[i[0]] = [float(value[1].strip(' p=')),float(value[0].strip('stat='))]
    return dep_M


def DEP_m(x,month):
    # Find how many graphs you want
    rows = []
    for i in dep_cor_M(month):
        i = i.split(' & ')
        com1 = i[0].strip('Cor TEST :')
        com2 = i[1]
        if x.strip('Cor TEST :') == com1:
            rows.append(' ')
    length = len(month[x])
    x_positions = np.arange(0,length)
    if len(rows) == 0:
        print('No Correlation')
        return None
    fig, axe = plt.subplots(len(rows),1,figsize=(15,8), sharex=True)
    main = np.average(month[x])
    if main > 200:
        main = np.array(month[x])/300    
    elif 50 < main < 200:
        main = np.array(month[x])/100
    elif 8 < main < 49:
        main = np.array(month[x])/10
    elif 1 < main < 8:
        main = np.array(month[x])/3
    else:
        main = np.array(month[x])*6
    c = 0

    for i in dep_cor_M(month):
        i_v = i
        i = i.split(' & ')
        com1 = i[0].strip('Cor TEST :')
        com2 = i[1]
        if x.strip('Cor TEST :') == com1:
            title = com2
            range_fac = np.max(month[title])
            if range_fac > 200:
                factor = np.array(month[title])/300   
            elif 50 < range_fac < 200:
                factor = np.array(month[title])/100
            elif 8 < range_fac < 49:
                factor = np.array(month[title])/15  
            elif 1 < range_fac < 8:
                factor = np.array(month[title])/3
            else:
                factor = np.array(month[title])*2
            if len(x_positions) != len(factor):
                x_positions = np.arange(0,len(factor))
            if len(rows) == 1:
                axe.plot(x_positions, factor,'m', lw=2)
                axe.set_xlabel(i[-1]+'\nP-value = %s, Stat = %s'%(dep_cor_M(month)[i_v][0],dep_cor_M(month)[i_v][1]), fontweight = 'bold', color = 'm')
            else:
                axe[c].plot(x_positions, factor,'m', lw=2)
                axe[c].set_xlabel(i[-1]+'\nP-value = %s, Stat = %s'%(dep_cor_M(month)[i_v][0],dep_cor_M(month)[i_v][1]), fontweight = 'bold', color = 'm')
                        
            for i in range(len(x_positions)):
                if len(rows) == 1:
                    axe.text(x_positions[i], factor[i]+.15, round(factor[i],2), horizontalalignment = 'center', color = 'm')
                elif len(rows) < 4:
                    axe[c].text(x_positions[i], factor[i]+.15, round(factor[i],2), horizontalalignment = 'center', color = 'm')
                else:
                    axe[c].text(x_positions[i], factor[i]+.5, round(factor[i],2), horizontalalignment = 'center', color = 'm')
            if len(rows) == 1:
                axe.bar(x_positions, main, color = 'orange', alpha = .5, label = x, width = .5)
            else:
                if c == 0:
                    axe[c].bar(x_positions, main, color = 'orange', alpha = .5, label = x, width = .5)
                else:
                    axe[c].bar(x_positions, main, color = 'orange', alpha = .5, width = .5)
            c += 1
    fig.tight_layout(w_pad = 3)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.legend()
    if 'Date' in month:
        mon = int(month['Date'][0][0:2].strip('/'))
    else:
        mon = int(month['Name'][0][0:2].strip('/'))
    fig.suptitle(x+'\nMonth: %s'%(mon), fontsize = 15, fontweight='bold')
    try: 
        plt.savefig('/Volumes/Programming/Personal/progress/jpg files/Overall/Specific Correlation.jpg', format = 'jpg'
                , dpi=1000, bbox_inches = 'tight')
    except FileNotFoundError:
        plt.savefig('D:\Personal\progress\jpg files\Overall\Specific Correlation.jpg', format = 'jpg'
                , dpi=1000, bbox_inches = 'tight')
        
        
#%%
'''
                [Correlation between 2 specific months]
'''

def correlation_change(M):
    m_tests = []
    months = []
    for m in M:
        m = DeleteUnnecessaryVar(m, 'include date')
        names = list(m.keys())
        values = list(m.values())
        results = []
        r = 0
        c = 0
        if 'Date' in m:
            month = int(m['Date'][0][0:2].strip('/'))
        else:
            month = int(m['Name'][0][0:2].strip('/'))
        if len(str(month)) < 2:
            months.append('0'+str(month))
        else:
            months.append(month)
        for i in values:
            for j in values:
                if np.all(i == j):
                    pass
                elif type(i[0]) == type('s') or type(j[0]) == type('s'):
                    pass
                elif np.all(np.array(i)==0) or np.all(np.array(j)==0):
                    pass
                elif len(i) != len(j):
                    if len(i) > len(j):
                        n = len(i)-len(j)
                        i = i[n:]
                        results.append(correlation_test(i,j,names[c], names[r] ))
                    elif len(i) < len(j):
                        n = len(j)-len(i)
                        j = j[n:]
                        results.append(correlation_test(i, j,names[c], names[r] ))
                    else:
                        results.append(correlation_test(i, j,names[c], names[r] ))
                else:
                    results.append(correlation_test(i, j,names[c], names[r] ))
            
                r += 1
            c +=1
            r = 0
        m_tests.append(results)
    
    test1 = m_tests[0]
    test2 = m_tests[1]
    red = []
    major_change = []
    for one in test1:
        one = one.split('\n')
        del one[0]
        values1 = one[1].split(', ')
        stat1 = float(values1[0].strip('stat='))
        pval1 = float(values1[1].strip('p='))
        for two in test2:
            two = two.split('\n')
            del two[0]
            values2 = two[1].split(', ')
            stat2 = float(values2[0].strip('stat='))
            pval2 = float(values2[1].strip('p='))
            stat_d = stat2-stat1
            pval_d = pval2-pval1
            if one[0] == two[0] and one[-1] != two[-1] and pval_d not in red:
                if pval_d > .5:
                    major_change.append([one[0],pval1,pval2,round(pval_d,5),stat1,stat2,round(stat_d,5)])
                elif pval_d < -.5:
                    major_change.append([one[0],pval1,pval2,round(pval_d,5),stat1,stat2,round(stat_d,5)])
                red.append(pval_d)
    
    
    a = ''
    a += 'Month: %d\n'% month
    for i in range(len(major_change)):
        a += ('''
        -------------------------------------------------
        %s
              %s : p-value = %f, stat = %f
              %s : p-vaule = %f, stat = %f
        
        Difference
              p-value: %f
              stat   : %f
              '''
            % (major_change[i][0], months[0], major_change[i][1], 
               major_change[i][4], months[1], major_change[i][2],
               major_change[i][5], major_change[i][3], major_change[i][-1]))
    return major_change, a, months


#%%
'''
                [Correlation between Overall & Specific Month]
'''
def correlation_change_overall(M):
    # Delete M[1] from M[0] since we are comparing those two 
    try:                    
        M[0].remove(M[1])
    except ValueError:
        pass
    M[0] = getTotal(M[0])
    m_tests = []
    months = []
    for m in M:
        m = DeleteUnnecessaryVar(m, 'include date')
        names = list(m.keys())
        values = list(m.values())
        results = []
        r = 0
        c = 0
        if len(m['Name']) > 50:
            months.append('All')
        else:
            if 'Date' in m:
                month = int(m['Date'][0][0:2].strip('/'))
            else:
                month = int(m['Name'][0][0:2].strip('/'))
            if len(str(month)) < 2:
                months.append('0'+str(month))
            else:
                months.append(month)
        for i in values:
            for j in values:
                if np.all(i == j):
                    pass
                elif type(i[0]) == type('s') or type(j[0]) == type('s'):
                    pass
                elif np.all(np.array(i)==0) or np.all(np.array(j)==0):
                    pass
                elif len(i) != len(j):
                    if len(i) > len(j):
                        n = len(i)-len(j)
                        i = i[n:]
                        results.append(correlation_test(i,j,names[c], names[r] ))
                    elif len(i) < len(j):
                        n = len(j)-len(i)
                        j = j[n:]
                        results.append(correlation_test(i, j,names[c], names[r] ))
                    else:
                        results.append(correlation_test(i, j,names[c], names[r] ))
                else:
                    results.append(correlation_test(i, j,names[c], names[r] ))
            
                r += 1
            c +=1
            r = 0
        m_tests.append(results)
    
    test1 = m_tests[0]
    test2 = m_tests[1]
    red = []
    major_change = []
    for one in test1:
        one = one.split('\n')
        del one[0]
        values1 = one[1].split(', ')
        stat1 = float(values1[0].strip('stat='))
        pval1 = float(values1[1].strip('p='))
        for two in test2:
            two = two.split('\n')
            del two[0]
            values2 = two[1].split(', ')
            stat2 = float(values2[0].strip('stat='))
            pval2 = float(values2[1].strip('p='))
            stat_d = stat2-stat1
            pval_d = pval2-pval1
            if one[0] == two[0] and one[-1] != two[-1] and pval_d not in red:
                if pval_d > .5:
                    major_change.append([one[0],pval1,pval2,round(pval_d,5),stat1,stat2,round(stat_d,5)])
                elif pval_d < -.5:
                    major_change.append([one[0],pval1,pval2,round(pval_d,5),stat1,stat2,round(stat_d,5)])
                red.append(pval_d)
    
    
    a = ''
    a += 'Month: %d\n'% month
    all_names = []
    for i in range(len(major_change)):
        name = major_change[i][0].replace('Cor TEST : ','')
        name = name.split(' & ')
        
        # Omit redundancy
        if [name[0],name[1]] in all_names or [name[1],name[0]] in all_names:
            pass
            del major_change[i]
        else:
            a += ('''
            -------------------------------------------------
            %s
                  %s : p-value = %f, stat = %f
                  %s  : p-vaule = %f, stat = %f
            
            Difference
                  p-value: %f
                  stat   : %f
                  '''
                % (major_change[i][0], months[0], major_change[i][1], 
                   major_change[i][4], months[1], major_change[i][2],
                   major_change[i][5], major_change[i][3], major_change[i][-1]))
        all_names.append(name)
        
    return major_change, a, months





















