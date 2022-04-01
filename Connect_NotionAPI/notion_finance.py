<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 23:20:25 2021

@author: anddy
"""

import numpy as np
from matplotlib import pyplot as plt
import os, sys
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from notion.client import NotionClient
from datetime import date
import pandas as pd
from datetime import datetime
sys.path.append('C:\\NotionUpdate\\progress')
from secret import secret





class Update_Notion_Finance():
    def __init__(self):
        pass    
        
    def crypto_graph(self, df):
        
        tot_days = -20
        initial_inv = 6000
        andy_share = .25
        trey_share = .25
        che_share = .5
        
        fig, axe = plt.subplots(2,1, figsize = (12,9), gridspec_kw={'height_ratios': [2, 1]})
        fig.tight_layout(h_pad = 6)

        bot_profit = df['bot_profit']
        
        # Total amount of bot profit from cancelled bots
        cancelled_bp = df['cancelled bot profit'][bot_profit.index[-1]]

        
        bot_profit_sep = []
        for i in range(len(bot_profit)):
            if i==0:
                bot_profit_sep.append(bot_profit[i])
            else:
                if bot_profit[i] - bot_profit[i-1] < 0:
                    bot_profit_sep.append(0)
                else:
                    bot_profit_sep.append(bot_profit[i] - bot_profit[i-1])
        
        # change date formats
        date = df['Date']
        date_x = []
        for d in date:
            d = d.split('/')
            date_x.append(int(d[1]))
        
        xticks = np.arange(0,-tot_days)
        
        balance_tot = df['balance total']
        
        # 1st plot: Line graph
        balance_tot_short = list(balance_tot.iloc[tot_days:]) 
            # Change it to list since it has dataframe index
            # Only print the last 20 days for clean graph purposes
        
        axe[0].plot(balance_tot_short, 'g-', label = 'Balance Total')
        axe[0].set_title('Total Balance\n', fontsize = 18, fontweight = 'bold')
        axe[0].set_xlabel('Date', fontsize = 13, fontweight = 'bold')
        axe[0].set_ylabel('Balance', fontsize= 13, fontweight = 'bold')
        axe[0].set_xticks(xticks)
        axe[0].set_xticklabels(date_x[tot_days:])
        axe[0].tick_params(axis='y', labelcolor='green')
        axe[0].plot([initial_inv]*len(balance_tot_short), 'r--', label = 'Initial Investment', alpha = .5)
        
        # 1st plot: bar graph
        axe2 = axe[0].twinx()        
        x_positions = np.arange(0,-tot_days)
        axe2.bar(x_positions, bot_profit_sep[tot_days:], color = 'blue', label = 'Bot Profit', lw=2, alpha = .2)
        axe2.tick_params(axis='y', labelcolor='black')
        

        if max(bot_profit) < 100:
            ylimit = 100
        else:
            ylimit = max(bot_profit)+ max(bot_profit)/10
        axe2.set_ylim(0,ylimit)
        axe2.tick_params(axis='y', labelcolor='blue')
        
        # daily bot profit text
        ind = len(date_x) + tot_days # new starting point for the text 
        
        for i in range(len(date_x[tot_days:])):
            
            if bot_profit_sep[ind+i] == 0 and df['bot status'][bot_profit.index[ind+i]] != "Range":
                axe2.text(x_positions[i], bot_profit_sep[ind+i]+1, 'bot\nchange\n', color = 'blue',
                      horizontalalignment='center' ,fontsize = 11, alpha=.9)
            else:
                axe2.text(x_positions[i], bot_profit_sep[ind+i]+1, '$' + str(int(bot_profit_sep[ind+i])), color = 'blue',
                      horizontalalignment='center' ,fontsize = 11, alpha=.9)
        
        # 1st plot: Line graph (Bot profit)
        bot_profit_short = list(bot_profit[tot_days:])
            # Change it to list since it has dataframe index
            # Only print the last 20 days for clean graph purposes
        
        axe2.plot(bot_profit_short, 'b-', label = 'Bot Profit', alpha = .45)
        axe2.text(len(xticks)-.8, bot_profit[bot_profit.index[-1]], '$'+str(int(bot_profit[bot_profit.index[-1]])), color = 'blue', fontsize = 11, fontweight = 'bold', alpha=.9)
        
        # Text
        last_balance = balance_tot[balance_tot.index[-1]]
        axe[0].text(.82,1.09,'Tot Balance: $%d'% (balance_tot[balance_tot.index[-1]]), color = 'green',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[0].transAxes)
        axe[0].text(.6628,1.02,'B.P. Current/ Cancelled: \$%d/ \$%d'% (bot_profit[bot_profit.index[-1]], cancelled_bp), color = 'blue',fontweight = 'bold',
                    fontsize = 14, alpha = .3, transform= axe[0].transAxes)
            # .6628 for 3 digits
        
        # get average profit
            # If there was a bot change, need to take the value out to calculate average
        if 0 in bot_profit_sep:
            count_zero = []
            for i in bot_profit_sep:
                if i == 0:
                    count_zero.append(0)
            avg_profit = np.sum(bot_profit_sep)/(len(bot_profit_sep)-len(count_zero))
        else:
            avg_profit = np.average(bot_profit_sep)
        axe[0].text(-.03,1.05, 'Daily Bot Profit Avg: $%.1f (%d days total)'%(avg_profit,len(bot_profit_sep)), color = 'red',fontweight = 'bold',
                    fontsize = 14, alpha = .6, transform= axe[0].transAxes)

        
        # Profit for each person
        current_tot = balance_tot[balance_tot.index[-1]]
        andy = (bot_profit[bot_profit.index[-1]] + cancelled_bp) * .25
        andy_tot = round(current_tot * andy_share - initial_inv * andy_share,2)
        trey = (bot_profit[bot_profit.index[-1]] + cancelled_bp) * .25
        trey_tot = round(current_tot * trey_share - initial_inv * trey_share,2)
        che = (bot_profit[bot_profit.index[-1]] + cancelled_bp) * .5
        che_tot = round(current_tot * che_share - initial_inv * che_share,2)
        
        bot_profit_person = [0, andy,0,trey,0, che]
        tot_profit_person = [andy_tot,0, trey_tot, 0,che_tot, 0]
        names = [ 'Total P/L\n(including bot+)','Bot Profit', 'Total P/L\n(including bot+)', 'Bot Profit','Total P/L\n(including bot+)', 'Bot Profit']

        # 2nd plot: bar graph
        x_positions_person = np.arange(0, len(bot_profit_person))
        c = ['darkorange', 'darkorange','tan','tan','mediumorchid','mediumorchid']
        axe[1].bar(x_positions_person, bot_profit_person, color = c, lw = .5, label = 'Total Bot Profit', alpha = .3)
        axe[1].bar(x_positions_person, tot_profit_person, color = c, lw = .5, label = 'Total Earnings', alpha = .5)
        axe[1].set_xlabel('Investors', fontsize = 13, fontweight = 'bold')
        axe[1].set_ylabel('B.P. (Cancelled + Current)', fontsize= 13, fontweight = 'bold')
        axe[1].set_xticks(x_positions_person)
        axe[1].set_xticklabels(names)

        '''
             When we add another bot, use align = 'edge' feature 
        '''
        
        # 2nd plot: Text (1)
        axe[1].text(0,1.05,'TOTAL:', color = 'k',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[1].transAxes)
        axe[1].text(.11,1.05,'Andy: %.1f$'% (balance_tot[balance_tot.index[-1]]*.25), color = 'darkorange',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[1].transAxes)
        axe[1].text(.42,1.05,'Trey: %.1f$'% (balance_tot[balance_tot.index[-1]]*.25), color = 'tan',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[1].transAxes)
        axe[1].text(.76,1.05,'Chanae: %.1f$'% (balance_tot[balance_tot.index[-1]]*.5), color = 'mediumorchid',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[1].transAxes)
        axe[1].text(.7,-.9,'Last Updated: '+ datetime.now().strftime('%Y-%m-%d %H:%M')    , color = 'k',fontweight = 'bold',
                            fontsize = 14, alpha = .83, transform= axe[0].transAxes)
        
        # 2nd Plot: Text (2)        
        c = 0
        spacing = .08
        for i in range(6):
            
            if i%2 == 0:
                axe[1].text(spacing,.05,'$'+str(tot_profit_person[i]), color = 'red', fontweight = 'bold',
                            fontsize = 11   , transform= axe[1].transAxes)
            else:
                axe[1].text(spacing,.05,'$'+str(bot_profit_person[i]), color = 'red',
                            fontsize = 11   , transform= axe[1].transAxes)
            spacing += .158
            
            
        fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=axe[0].transAxes)
        
        plt.savefig(r"C:\NotionUpdate\progress\Connect_NotionAPI\jpg files\crypto_update.jpg", format = 'jpg'
        , dpi=1000, bbox_inches = 'tight')

    
        
        
        
    def NotionAutoUpdate(self, driver):
                
        # go to Crypto Page
        driver.get("https://app.bitsgap.com/bot")
        driver.maximize_window()
        # Set the Crypto Page tab 1        
        
        time.sleep(3)

        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-form"]/div[1]/div')))                         
        bits_id = driver.find_element_by_xpath('//*[@id="lemail"]')
        bits_id.click()
        bits_id.send_keys(secret.bitsgap_login("username"))
        
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-form"]/div[2]/div')))
        bits_pw = driver.find_element_by_xpath('//*[@id="lpassword"]')
        bits_pw.click()
        bits_pw.send_keys(secret.bitsgap_login("pwd"))
        
        ActionChains(driver).send_keys(Keys.ENTER)
        driver.find_element_by_xpath('//*[@id="login-form"]/button').click()
        
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/button/svg')))
            exit_button = driver.find_element_by_xpath('/html/body/div[2]/div[3]/button/svg')
            exit_button.click()
        except:
            pass
        
        # Balance
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/div/div/div[2]')))
            balance = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/div/div/div[2]')
            balance.click()
        
            time.sleep(3)
            # Balance Status -> A box on the right side                      
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div')))
            balance_status = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div')
            
        except:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[1]/div/div/div/div[2]')))
            balance = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[1]/div/div/div/div[2]')
            balance.click()
        
            time.sleep(3)
            # Balance Status -> A box on the right side                      
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div')))
            balance_status = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div')
            
        
        
        

        
        allbots = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]')
        sum_value = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[3]/div').text
        
        available_bal_exchanges = {}
        available_tot = 0
        c = 1
        while True:
            try:
                # click on every bot that I own      
                if c == 1:
                    pass
                else:
                    driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[%d]/div[2]'%c).click()
                
            except:                           
                # if there is no more bot to click on, break
                available_bal_exchanges['Total'] = available_tot
                break
            time.sleep(2)
            # sbot details: exchange name
            exchange_name = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div').text
            
            # get exchange balance
            exchange_bal = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div').text
            available_bal = exchange_bal.split('\n')[-1]
            available_bal = int(available_bal.strip('USD').replace(" ",""))
            
            if exchange_name in available_bal_exchanges.keys():
                pass
            else:
                # available_tot is for the sum of all avaialbe balance in different exchanges
                available_tot += available_bal
            
            available_bal_exchanges.setdefault(exchange_name, []).append(available_bal)
            c += 1           
            
            # To prevent a redundant available balance, we need if statement
            
        
        
        
        
        # Sum Value
        sv = sum_value.replace(' ','').strip('$')
        
        # Balance Total
        
        
        # Balance status
        bs = balance_status.text.replace('—','0')
        bs = bs.split('\n')
        
        bots = {}
        today = date.today()
        today = today.strftime("%#m/%#d/%Y")
        bots['Date'] = today.strip('0')
        coins = []
        c = 0
        for i in range(len(bs)):
            if i % 5 == 0:
                if i != 0:
                    c+=1
                coins.append(bs[i])
                bots.setdefault(coins[c], [])
            else: 
                if bots[coins[c]] == []:
                    # check if there's any value in cions[c], if not, add (only one value)
                    
                    bots[coins[c]] = float(bs[i].strip('USD ').replace(' ',''))
                else:
                    pass
        
        
        allbots = allbots.text
        allbots = allbots.split('\n')
        change = allbots[2]

        
        bot_status_1 = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[8]/div/div[1]/div').text
        bot_status_2 = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div[8]/div/div[1]/div').text
        
        
        # Get the previous bot profits
        driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div/div[3]').click()
        time.sleep(2)
        
        cancelled_bot_profit = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div/div/span[1]').text
        cancelled_bp = int(cancelled_bot_profit.strip('$ ').replace(' ',''))
        
        # Read the csv file (cryptojournal.csv)
        os.chdir('C:\\NotionUpdate\\progress\\Connect_NotionAPI')
        df = pd.read_csv('crypto_journal_set1.csv')
        
        # Drop any added unnecessary columns
        if 'Unnamed: 0' in df.keys():
            df = df.drop('Unnamed: 0', 1)

        
        # Run until the page loads (when cancelled_bp is not zero)
        c = 0 # If it runs over 5 times, the closed bot has been hidden
        while True:
            if c > 4 and cancelled_bp == 0:
                cancelled_bp = np.max(df['cancelled bot profit'])
                break
                
            elif cancelled_bp == 0:
                time.sleep(1)   
                cancelled_bot_profit = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div/div/span[1]').text
                cancelled_bp = int(cancelled_bot_profit.strip('$ ').replace(' ',''))
                
            else:
                break
            c += 1
        
        # Move to the exchange page
        driver.get('https://app.bitsgap.com/my-exchanges')
        time.sleep(3)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[1]/div/div[2]/span[2]')))
        coinbase_pro = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[1]/div/div[2]/span[2]').text
        kucoin = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[2]/div/div[2]/span[2]').text
        
        if 'N/A' == coinbase_pro:
            driver.sendKeys(Keys.F5)
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[1]/div/div[2]/span[2]')))
            coinbase_pro = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[1]/div/div[2]/span[2]').text
            kucoin = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[2]/div/div[2]/span[2]').text
            
        coinbase_pro = int(coinbase_pro.strip('$ USD').replace(' ',''))
        kucoin = int(kucoin.strip('$ USD').replace(' ',''))
        
        print('coinbase_pro: ', coinbase_pro)
        print('kucoin: ', kucoin)
        print()
        print('Total: ', coinbase_pro + kucoin)
        print()
        print()
        
        
        if bot_status_1 == 'Range' and bot_status_2 == 'Range':
            bots['bot status'] = 'Range'
        else:
            bots['bot status'] = 'Active'
            
        bots['balance total (available)'] = available_bal_exchanges['Total']
        bots['cancelled bot profit'] = cancelled_bp
        bots['sum value'] = int(sv)
        bots['balance total'] = coinbase_pro + kucoin
        bots['change'] = round(float(change.strip('%()+-')),1)
        bots['bot_profit'] = round(float(allbots[4].strip(' $').replace(' ','')),1)
        bots['bot profit %'] = round(float(allbots[5].strip('%()+-')),1)
        
        


        # Add a row 
        if len(df[df['Date']==today.strip('0')]) < 1:
            pass
            
        else:
            df.drop(df.tail(1).index,inplace=True) # drop last n rows
            
        # concatenate the row into existing df            
        df = pd.concat([df,pd.DataFrame(bots, index = [0])], axis=0, ignore_index=True)    
        # save it to my file
        df.to_csv(r'C:\NotionUpdate\progress\Connect_NotionAPI\crypto_journal_set1.csv', index = False)
        
        driver.quit()
        
        
        return df
    
    
                
        
    def uploadFinanceJPG(self):
        print("Uploading Total_Balance.jpg  ..... ")
        token_v2 = secret.notion_API("token_v2")
        client = NotionClient(token_v2=token_v2)
        time.sleep(1)
        # connect page
        url = 'https://www.notion.so/andyhomepage/Crypto-b0ab576de9834c09867844f3bfe54239'
        page = client.get_block(url)
        
        time.sleep(1)
        
        newchild = page.children.add_new('image')
        time.sleep(1)
        newchild.upload_file(r"C:\NotionUpdate\progress\Connect_NotionAPI\jpg files\crypto_update.jpg")
        newchild.move_to(page.children[1],"before")
        page.children[0].remove()



driver = webdriver.Chrome('C:\\NotionUpdate\\progress\\chromedriver.exe')
Update = Update_Notion_Finance()
df = Update.NotionAutoUpdate(driver)
Update.crypto_graph(df)
Update.uploadFinanceJPG()









=======
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 23:20:25 2021

@author: anddy
"""

import numpy as np
from matplotlib import pyplot as plt
import os, sys
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from notion.client import NotionClient
from datetime import date
import pandas as pd
from datetime import datetime
sys.path.append('C:\\NotionUpdate\\progress')
from secret import secret





class Update_Notion_Finance():
    def __init__(self):
        pass    
        
    def crypto_graph(self, df):
        
        tot_days = -20
        initial_inv = 6000
        andy_share = .25
        trey_share = .25
        che_share = .5
        
        fig, axe = plt.subplots(2,1, figsize = (12,9), gridspec_kw={'height_ratios': [2, 1]})
        fig.tight_layout(h_pad = 6)

        bot_profit = df['bot_profit']
        
        # Total amount of bot profit from cancelled bots
        cancelled_bp = df['cancelled bot profit'][bot_profit.index[-1]]

        
        bot_profit_sep = []
        for i in range(len(bot_profit)):
            if i==0:
                bot_profit_sep.append(bot_profit[i])
            else:
                if bot_profit[i] - bot_profit[i-1] < 0:
                    bot_profit_sep.append(0)
                else:
                    bot_profit_sep.append(bot_profit[i] - bot_profit[i-1])
        
        # change date formats
        date = df['Date']
        date_x = []
        for d in date:
            d = d.split('/')
            date_x.append(int(d[1]))
        
        xticks = np.arange(0,-tot_days)
        
        balance_tot = df['balance total']
        
        # 1st plot: Line graph
        balance_tot_short = list(balance_tot.iloc[tot_days:]) 
            # Change it to list since it has dataframe index
            # Only print the last 20 days for clean graph purposes
        
        axe[0].plot(balance_tot_short, 'g-', label = 'Balance Total')
        axe[0].set_title('Total Balance\n', fontsize = 18, fontweight = 'bold')
        axe[0].set_xlabel('Date', fontsize = 13, fontweight = 'bold')
        axe[0].set_ylabel('Balance', fontsize= 13, fontweight = 'bold')
        axe[0].set_xticks(xticks)
        axe[0].set_xticklabels(date_x[tot_days:])
        axe[0].tick_params(axis='y', labelcolor='green')
        axe[0].plot([initial_inv]*len(balance_tot_short), 'r--', label = 'Initial Investment', alpha = .5)
        
        # 1st plot: bar graph
        axe2 = axe[0].twinx()        
        x_positions = np.arange(0,-tot_days)
        axe2.bar(x_positions, bot_profit_sep[tot_days:], color = 'blue', label = 'Bot Profit', lw=2, alpha = .2)
        axe2.tick_params(axis='y', labelcolor='black')
        

        if max(bot_profit) < 100:
            ylimit = 100
        else:
            ylimit = max(bot_profit)+ max(bot_profit)/10
        axe2.set_ylim(0,ylimit)
        axe2.tick_params(axis='y', labelcolor='blue')
        
        # daily bot profit text
        ind = len(date_x) + tot_days # new starting point for the text 
        
        for i in range(len(date_x[tot_days:])):
            
            if bot_profit_sep[ind+i] == 0 and df['bot status'][bot_profit.index[ind+i]] != "Range":
                axe2.text(x_positions[i], bot_profit_sep[ind+i]+1, 'bot\nchange\n', color = 'blue',
                      horizontalalignment='center' ,fontsize = 11, alpha=.9)
            else:
                axe2.text(x_positions[i], bot_profit_sep[ind+i]+1, '$' + str(int(bot_profit_sep[ind+i])), color = 'blue',
                      horizontalalignment='center' ,fontsize = 11, alpha=.9)
        
        # 1st plot: Line graph (Bot profit)
        bot_profit_short = list(bot_profit[tot_days:])
            # Change it to list since it has dataframe index
            # Only print the last 20 days for clean graph purposes
        
        axe2.plot(bot_profit_short, 'b-', label = 'Bot Profit', alpha = .45)
        axe2.text(len(xticks)-.8, bot_profit[bot_profit.index[-1]], '$'+str(int(bot_profit[bot_profit.index[-1]])), color = 'blue', fontsize = 11, fontweight = 'bold', alpha=.9)
        
        # Text
        last_balance = balance_tot[balance_tot.index[-1]]
        axe[0].text(.82,1.09,'Tot Balance: $%d'% (balance_tot[balance_tot.index[-1]]), color = 'green',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[0].transAxes)
        axe[0].text(.6628,1.02,'B.P. Current/ Cancelled: \$%d/ \$%d'% (bot_profit[bot_profit.index[-1]], cancelled_bp), color = 'blue',fontweight = 'bold',
                    fontsize = 14, alpha = .3, transform= axe[0].transAxes)
            # .6628 for 3 digits
        
        # get average profit
            # If there was a bot change, need to take the value out to calculate average
        if 0 in bot_profit_sep:
            count_zero = []
            for i in bot_profit_sep:
                if i == 0:
                    count_zero.append(0)
            avg_profit = np.sum(bot_profit_sep)/(len(bot_profit_sep)-len(count_zero))
        else:
            avg_profit = np.average(bot_profit_sep)
        axe[0].text(-.03,1.05, 'Daily Bot Profit Avg: $%.1f (%d days total)'%(avg_profit,len(bot_profit_sep)), color = 'red',fontweight = 'bold',
                    fontsize = 14, alpha = .6, transform= axe[0].transAxes)

        
        # Profit for each person
        current_tot = balance_tot[balance_tot.index[-1]]
        andy = (bot_profit[bot_profit.index[-1]] + cancelled_bp) * .25
        andy_tot = round(current_tot * andy_share - initial_inv * andy_share,2)
        trey = (bot_profit[bot_profit.index[-1]] + cancelled_bp) * .25
        trey_tot = round(current_tot * trey_share - initial_inv * trey_share,2)
        che = (bot_profit[bot_profit.index[-1]] + cancelled_bp) * .5
        che_tot = round(current_tot * che_share - initial_inv * che_share,2)
        
        bot_profit_person = [0, andy,0,trey,0, che]
        tot_profit_person = [andy_tot,0, trey_tot, 0,che_tot, 0]
        names = [ 'Total P/L\n(including bot+)','Bot Profit', 'Total P/L\n(including bot+)', 'Bot Profit','Total P/L\n(including bot+)', 'Bot Profit']

        # 2nd plot: bar graph
        x_positions_person = np.arange(0, len(bot_profit_person))
        c = ['darkorange', 'darkorange','tan','tan','mediumorchid','mediumorchid']
        axe[1].bar(x_positions_person, bot_profit_person, color = c, lw = .5, label = 'Total Bot Profit', alpha = .3)
        axe[1].bar(x_positions_person, tot_profit_person, color = c, lw = .5, label = 'Total Earnings', alpha = .5)
        axe[1].set_xlabel('Investors', fontsize = 13, fontweight = 'bold')
        axe[1].set_ylabel('B.P. (Cancelled + Current)', fontsize= 13, fontweight = 'bold')
        axe[1].set_xticks(x_positions_person)
        axe[1].set_xticklabels(names)

        '''
             When we add another bot, use align = 'edge' feature 
        '''
        
        # 2nd plot: Text (1)
        axe[1].text(0,1.05,'TOTAL:', color = 'k',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[1].transAxes)
        axe[1].text(.11,1.05,'Andy: %.1f$'% (balance_tot[balance_tot.index[-1]]*.25), color = 'darkorange',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[1].transAxes)
        axe[1].text(.42,1.05,'Trey: %.1f$'% (balance_tot[balance_tot.index[-1]]*.25), color = 'tan',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[1].transAxes)
        axe[1].text(.76,1.05,'Chanae: %.1f$'% (balance_tot[balance_tot.index[-1]]*.5), color = 'mediumorchid',fontweight = 'bold',
                    fontsize = 14, alpha = .83, transform= axe[1].transAxes)
        axe[1].text(.7,-.9,'Last Updated: '+ datetime.now().strftime('%Y-%m-%d %H:%M')    , color = 'k',fontweight = 'bold',
                            fontsize = 14, alpha = .83, transform= axe[0].transAxes)
        
        # 2nd Plot: Text (2)        
        c = 0
        spacing = .08
        for i in range(6):
            
            if i%2 == 0:
                axe[1].text(spacing,.05,'$'+str(tot_profit_person[i]), color = 'red', fontweight = 'bold',
                            fontsize = 11   , transform= axe[1].transAxes)
            else:
                axe[1].text(spacing,.05,'$'+str(bot_profit_person[i]), color = 'red',
                            fontsize = 11   , transform= axe[1].transAxes)
            spacing += .158
            
            
        fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=axe[0].transAxes)
        
        plt.savefig(r"C:\NotionUpdate\progress\Connect_NotionAPI\jpg files\crypto_update.jpg", format = 'jpg'
        , dpi=1000, bbox_inches = 'tight')

    
        
        
        
    def NotionAutoUpdate(self, driver):
                
        # go to Crypto Page
        driver.get("https://app.bitsgap.com/bot")
        driver.maximize_window()
        # Set the Crypto Page tab 1        
        
        time.sleep(3)

        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-form"]/div[1]/div')))                         
        bits_id = driver.find_element_by_xpath('//*[@id="lemail"]')
        bits_id.click()
        bits_id.send_keys(secret.bitsgap_login("username"))
        
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-form"]/div[2]/div')))
        bits_pw = driver.find_element_by_xpath('//*[@id="lpassword"]')
        bits_pw.click()
        bits_pw.send_keys(secret.bitsgap_login("pwd"))
        
        ActionChains(driver).send_keys(Keys.ENTER)
        driver.find_element_by_xpath('//*[@id="login-form"]/button').click()
        
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/button/svg')))
            exit_button = driver.find_element_by_xpath('/html/body/div[2]/div[3]/button/svg')
            exit_button.click()
        except:
            pass
        
        # Balance
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/div/div/div[2]')))
            balance = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div[1]/div/div/div/div[2]')
            balance.click()
        
            time.sleep(3)
            # Balance Status -> A box on the right side                      
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div')))
            balance_status = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div')
            
        except:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[1]/div/div/div/div[2]')))
            balance = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[1]/div/div/div/div[2]')
            balance.click()
        
            time.sleep(3)
            # Balance Status -> A box on the right side                      
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div')))
            balance_status = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div')
            
        
        
        

        
        allbots = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]')
        sum_value = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[3]/div').text
        
        available_bal_exchanges = {}
        available_tot = 0
        c = 1
        while True:
            try:
                # click on every bot that I own      
                if c == 1:
                    pass
                else:
                    driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[%d]/div[2]'%c).click()
                
            except:                           
                # if there is no more bot to click on, break
                available_bal_exchanges['Total'] = available_tot
                break
            time.sleep(2)
            # sbot details: exchange name
            exchange_name = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div').text
            
            # get exchange balance
            exchange_bal = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div').text
            available_bal = exchange_bal.split('\n')[-1]
            available_bal = int(available_bal.strip('USD').replace(" ",""))
            
            if exchange_name in available_bal_exchanges.keys():
                pass
            else:
                # available_tot is for the sum of all avaialbe balance in different exchanges
                available_tot += available_bal
            
            available_bal_exchanges.setdefault(exchange_name, []).append(available_bal)
            c += 1           
            
            # To prevent a redundant available balance, we need if statement
            
        
        
        
        
        # Sum Value
        sv = sum_value.replace(' ','').strip('$')
        
        # Balance Total
        
        
        # Balance status
        bs = balance_status.text.replace('—','0')
        bs = bs.split('\n')
        
        bots = {}
        today = date.today()
        today = today.strftime("%#m/%#d/%Y")
        bots['Date'] = today.strip('0')
        coins = []
        c = 0
        for i in range(len(bs)):
            if i % 5 == 0:
                if i != 0:
                    c+=1
                coins.append(bs[i])
                bots.setdefault(coins[c], [])
            else: 
                if bots[coins[c]] == []:
                    # check if there's any value in cions[c], if not, add (only one value)
                    
                    bots[coins[c]] = float(bs[i].strip('USD ').replace(' ',''))
                else:
                    pass
        
        
        allbots = allbots.text
        allbots = allbots.split('\n')
        change = allbots[2]

        
        bot_status_1 = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[8]/div/div[1]/div').text
        bot_status_2 = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div[8]/div/div[1]/div').text
        
        
        # Get the previous bot profits
        driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div/div[3]').click()
        time.sleep(2)
        
        cancelled_bot_profit = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div/div/span[1]').text
        cancelled_bp = int(cancelled_bot_profit.strip('$ ').replace(' ',''))
        
        # Read the csv file (cryptojournal.csv)
        os.chdir('C:\\NotionUpdate\\progress\\Connect_NotionAPI')
        df = pd.read_csv('crypto_journal_set1.csv')
        
        # Drop any added unnecessary columns
        if 'Unnamed: 0' in df.keys():
            df = df.drop('Unnamed: 0', 1)

        
        # Run until the page loads (when cancelled_bp is not zero)
        c = 0 # If it runs over 5 times, the closed bot has been hidden
        while True:
            if c > 4 and cancelled_bp == 0:
                cancelled_bp = np.max(df['cancelled bot profit'])
                break
                
            elif cancelled_bp == 0:
                time.sleep(1)   
                cancelled_bot_profit = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div/div/span[1]').text
                cancelled_bp = int(cancelled_bot_profit.strip('$ ').replace(' ',''))
                
            else:
                break
            c += 1
        
        # Move to the exchange page
        driver.get('https://app.bitsgap.com/my-exchanges')
        time.sleep(3)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[1]/div/div[2]/span[2]')))
        coinbase_pro = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[1]/div/div[2]/span[2]').text
        kucoin = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[2]/div/div[2]/span[2]').text
        
        if 'N/A' == coinbase_pro:
            driver.sendKeys(Keys.F5)
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[1]/div/div[2]/span[2]')))
            coinbase_pro = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[1]/div/div[2]/span[2]').text
            kucoin = driver.find_element_by_xpath('//*[@id="root"]/main/div/div/div/div/div/div[2]/div/ul/li[2]/div/div[2]/span[2]').text
            
        coinbase_pro = int(coinbase_pro.strip('$ USD').replace(' ',''))
        kucoin = int(kucoin.strip('$ USD').replace(' ',''))
        
        print('coinbase_pro: ', coinbase_pro)
        print('kucoin: ', kucoin)
        print()
        print('Total: ', coinbase_pro + kucoin)
        print()
        print()
        
        
        if bot_status_1 == 'Range' and bot_status_2 == 'Range':
            bots['bot status'] = 'Range'
        else:
            bots['bot status'] = 'Active'
            
        bots['balance total (available)'] = available_bal_exchanges['Total']
        bots['cancelled bot profit'] = cancelled_bp
        bots['sum value'] = int(sv)
        bots['balance total'] = coinbase_pro + kucoin
        bots['change'] = round(float(change.strip('%()+-')),1)
        bots['bot_profit'] = round(float(allbots[4].strip(' $').replace(' ','')),1)
        bots['bot profit %'] = round(float(allbots[5].strip('%()+-')),1)
        
        


        # Add a row 
        if len(df[df['Date']==today.strip('0')]) < 1:
            pass
            
        else:
            df.drop(df.tail(1).index,inplace=True) # drop last n rows
            
        # concatenate the row into existing df            
        df = pd.concat([df,pd.DataFrame(bots, index = [0])], axis=0, ignore_index=True)    
        # save it to my file
        df.to_csv(r'C:\NotionUpdate\progress\Connect_NotionAPI\crypto_journal_set1.csv', index = False)
        
        driver.quit()
        
        
        return df
    
    
                
        
    def uploadFinanceJPG(self):
        print("Uploading Total_Balance.jpg  ..... ")
        token_v2 = secret.notion_API("token_v2")
        client = NotionClient(token_v2=token_v2)
        time.sleep(1)
        # connect page
        url = 'https://www.notion.so/andyhomepage/Crypto-b0ab576de9834c09867844f3bfe54239'
        page = client.get_block(url)
        
        time.sleep(1)
        
        newchild = page.children.add_new('image')
        time.sleep(1)
        newchild.upload_file(r"C:\NotionUpdate\progress\Connect_NotionAPI\jpg files\crypto_update.jpg")
        newchild.move_to(page.children[1],"before")
        page.children[0].remove()



driver = webdriver.Chrome('C:\\NotionUpdate\\progress\\chromedriver.exe')
Update = Update_Notion_Finance()
df = Update.NotionAutoUpdate(driver)
Update.crypto_graph(df)
Update.uploadFinanceJPG()









>>>>>>> 572dc86 (update)
