# Notion Automation

<br>  


## Why Notion Automation? 
Every day, I utilize the Notion platform to schedule my tasks, store meaningful data, and visualize progress for diverse activities(finance, self-evaluations, etc.).
It has indeed been a wonderful experience using Notion, and because of it, I was able to increase my productivity level immensely. 
However, when I was using the platform a few years ago, I have realized that I go through many redundant motions in Notion throughout the day that I could easily automate using Python. 
Thus, I decided to do so by utilizing the Notion API. 
<br>  
Also, before demonstrating a brief explanation of the automation process, understanding my **self-evaluation** project will help grok the purpose of the automation.
For more than 500 days, I have [evaluated and recorded](https://github.com/aLin-96/notion_automation/tree/main/Data) my day-to-day life in the Notion database. 
The general idea is to quantify my daily habits, which are converted to percentages using various mathematical models to approximate the total score of how I lived each day. 
One may think of it as a grading system of my lifestyle.
Then these data are [visualized and updated](https://github.com/aLin-96/notion_automation/blob/main/evaluation_img_example.png) daily to the Notion home page. 
Through this project and daily evaluation, I was able to analyze the strengths and weaknesses of my life and push myself to live a better tomorrow.
<br>  
More information can be found in below links:
- [My Website](https://www.andyleeproject.com/)
- [Statistical Analysis of the lifestyle data using R (IN PROGRESS)](https://alin-96.github.io/selfeval_main.html)

 <br>  
 <br>  
 
## Automation Python Script Sample (No Sound)



https://user-images.githubusercontent.com/84836749/172465933-55117519-cd91-4a19-9719-f668185bc29c.mp4

- Through Notion API, python gathers all information from the Schedule Database. Then it sorts each block by the tags related to today's date to move them into Today column(to-do lists). (ex. given that today is Saturday, 1/1/2022, I can label the block using the **date tag**(1/1/2022), **Weekend** tag, **Everyday** tag, or **Sat** tag. Then python will sort them accordingly)
- Notice "Course: Speaking" block is checked and has 1 hour of estimated duration. Thus, Python will calculate the duration of all the completed blocks (tasks) to compute **Total Work Hours** and **Work Hours Finished** by gathering information from the database.

<br>  
<br>  


## AutoUpdateNotion_API.py [(Python Script)](https://github.com/aLin-96/notion_automation/blob/main/AutoUpdateNotion_API.py)

### 1. Connecting to the Notion API
Recently, Notion has released its API that conveniently allows users to extract data from all databases in Notion. Note that all data are imported to Python as JSON format, which requires data cleaning. 

### 2. Update Today's Schedule
There are approximately 50 weekly tasks in my To-do list database, which are divided into different categories(Programming, Classes, Job search, etc.).
Since it would be tedious and redundant to reschedule these tasks every day, I have successfully written a Python script that schedules it for me.
It goes through every block(task) in the database and organizes today's to-do lists within seconds. 

### 3. Update Duration Database in Notion ([Python Script](https://github.com/aLin-96/notion_automation/blob/main/notion_durationDB.py))
The duration database demonstrates the total expected work hours and how many hours I have completed throughout the day. For each task, there is an Estimated duration tag (ex. Study Statistics - 1hr) that I can assign accordingly. Then these estimations are hourly imported to Python to compute & update the total, completed, and remaining hours using Notion API. The purpose of estimating duration time is to handle and use the given time more efficiently.   

<img align="center" src="https://github.com/aLin-96/notion_automation/blob/main/sample_ImagesVideos/Duration_DB_sample.jpg" width="800" height="200" >

### 4. Read & Organize Evaluation Data ([Python Script](https://github.com/aLin-96/notion_automation/blob/main/myPackage/organize_evaluation_data.py))
The Evaluation data is daily recorded self-evaluations stored in the Notion database. 
It is read & organized for the visualization update.

### 5. Record Data (Excel, MySQL)
Utilizing MySQL will be one of the efficient ways to store and retrieve daily accumulating data. Through mysql.connector module, the Self Evaluation database in the local server can be accessed to send necessary queries for this process. 

### 6. Create Visualization ([Python Script](https://github.com/aLin-96/notion_automation/blob/main/myPackage/NotionprocessMonth.py))
Using the Matplotlib module, the graph is created demonstrating the daily trend of my lifestyle.  

<img align="center" src="https://github.com/aLin-96/notion_automation/blob/main/sample_ImagesVideos/monthly_evaluation_visualization.jpg" width="600" height="450" >
  
  
### 7. Upload & Update evaluation jpg
Using the Notion API, I can directly upload an image from Python. Thus, the created visualization will be updated right away after step 4. 

### 8. Task Schedular
Using the built-in task schedular feature in Windows, I have set up for the Python script to run two times a day. 
The script will run for the first time whenever I log in to my laptop and also at 9:00 pm for the second time.
 



