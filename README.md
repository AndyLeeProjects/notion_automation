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
 
## Automation Python Script  

https://user-images.githubusercontent.com/84836749/172453935-355dff09-d834-4038-a430-207adfeffeb0.mp4


<br>  
<br>  


## AutoUpdateNotion_API.py [(See file)](https://github.com/aLin-96/notion_automation/blob/main/AutoUpdateNotion_API.py)

### 1. Connecting to the Notion API
Recently, Notion has released its API that conveniently allows users to extract data from all databases in Notion. Note that all data are imported to Python as JSON format, which requires data cleaning. 

### 2. Update Today's Schedule
There are approximately 50 weekly tasks in my To-do list database, which are divided into different categories(Programming, Classes, Job search, etc.).
Since it would be tedious and redundant to reschedule these tasks every day, I have successfully written a Python script that schedules it for me.
It goes through every block(task) in the database and organizes today's to-do lists within seconds. 

### 3. Update Duration Database in Notion
The duration database demonstrates the total expected work hours and how many hours I have completed throughout the day. For each task, there is an Estimated duration tag (ex. Study Statistics - 1hr) that I can assign accordingly. Then these estimations are hourly imported to Python to compute & update the total, completed, and remaining hours using Notion API. The purpose of estimating duration time is to handle and use the given time more efficiently.   

<img align="center" src="https://github.com/aLin-96/notion_automation/blob/main/sample_images/Duration_DB_sample.jpg" width="800" height="200" >

### 4. Read & [Organize](https://github.com/aLin-96/notion_automation/blob/main/myPackage/organize_evaluation_data.py) Evaluation Data 
The Evaluation data is daily recorded self-evaluations stored in the Notion database. 
It is read & organized for the visualization update.

### 5. [Create Visualization](https://github.com/aLin-96/notion_automation/blob/main/myPackage/NotionprocessMonth.py)
Using the Matplotlib module, the graph is created demonstrating the daily trend of my lifestyle.  

<img align="center" src="https://github.com/aLin-96/notion_automation/blob/main/sample_images/monthly_evaluation_visualization.jpg" width="600" height="450" >
  
  
### 6. Upload & Update evaluation jpg
Using the Notion API, I can directly upload an image from Python. Thus, the created visualization will be updated right away after step 4. 

### 7. Task Schedular
Using the built-in task schedular feature in Windows, I have set up for the Python script to run two times a day. 
The script will run for the first time whenever I log in to my laptop and also at 9:00 pm for the second time.




