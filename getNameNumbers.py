#!/usr/bin/env python
# coding: utf-8

# In[23]:


import datetime
from datetime import timedelta
from datetime import date
import month_Days

def wxflow():
    
    # define variables for day, month, year
    today = date.today()
    todayDate = datetime.date.today()
    yesterday = today - timedelta(days = 1)
    todayDay = today.strftime("%d")
    todayDay = int(todayDay)
      
    # Present month
    this_month = (todayDate.strftime("%B"))
    this_month_num = (todayDate.strftime("%m"))
    this_month_num = int(this_month_num)
       
    # Current year
    thisYear = (todayDate.strftime("%Y"))
       
    # previous information for today
    lastDaythisMonth = month_Days.days_in_month(thisYear,this_month_num)
       
    # Yesterday
    yesterdayDay = yesterday.strftime("%d")
    yesterdayDay = int(yesterdayDay)
    date1 = yesterdayDay + 1
    print(date1)
    

    # Previous month
    last_month = todayDate.replace(day=1) - datetime.timedelta(days=1)
    prev_month = (last_month.strftime("%B"))
    prev_month_num = (last_month.strftime("%m"))
    prev_month_num = int(prev_month_num)
    
    
    # Previous year
    prev_year = todayDate.replace(day=1) - datetime.timedelta(days=365)
    prevYear = prev_year.strftime("%Y")
   
    
    # previous information for yesterday
    lastDaylastMonth = month_Days.days_in_month(thisYear,prev_month_num)
    
    
    # Last day of the previous month
    lastDaylastMonth = month_Days.days_in_month(thisYear,prev_month_num)
    

    # Last day of the previous year
    lastDaypreviousYear = month_Days.days_in_month(prevYear,12)
    
    
    # Assign some needed variables
    path_name = '/home/ec2-user/'
    platform = "Tempest"
    xls_suffix = '.xlsx'
    
    if todayDay == 1:
        xls_filename = f'{prev_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}{prev_month}_{thisYear}_{platform}{xls_suffix}'
        return(xls_filename, xls_fullname, path_name, date1, prev_month, thisYear, lastDaylastMonth)
    
    if todayDay == 1 and this_month == 'January':
        xls_filename = f'December_{prevYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}December_{prevYear}_{platform}{xls_suffix}'
        return(xls_filename, xls_fullname, path_name, date1, prev_month, prevYear, lastDayprevYear)
        
    else:
        xls_filename = f'{this_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullfile = f'{path_name}{this_month}_{thisYear}_{platform}{xls_suffix}'
    
        return(xls_filename, xls_fullname, path_name, todayDay, this_month, thisYear, lastDaythisMonth)     
    


# In[8]:


import datetime
from datetime import timedelta
from datetime import date
import month_Days

def tempest_ec2():
    
    # define variables for day, month, year
    today = date.today()
    todayDate = datetime.date.today()
    yesterday = today - timedelta(days = 1)
    
    todayDay = today.strftime("%d")
    todayDay = int(todayDay)
    
    # Present month
    this_month = (todayDate.strftime("%B"))
    this_month_num = (todayDate.strftime("%m"))
    this_month_num = int(this_month_num)
        
    # Current year
    thisYear = (todayDate.strftime("%Y"))
        
    # previous information for today
    lastDaythisMonth = month_Days.days_in_month(thisYear,this_month_num)
        
    # Yesterday
    yesterdayDay = yesterday.strftime("%d")
    yesterdayDay = int(yesterdayDay)
    date1 = yesterdayDay + 1
    
    # Previous month
    last_month = todayDate.replace(day=1) - datetime.timedelta(days=1)
    prev_month = (last_month.strftime("%B"))
    prev_month_num = (last_month.strftime("%m"))
    prev_month_num = int(prev_month_num)
        
    # Previous year
    prev_year = todayDate.replace(day=1) - datetime.timedelta(days=365)
    prevYear = prev_year.strftime("%Y")
       
    # previous information for yesterday
    lastDaylastMonth = month_Days.days_in_month(thisYear,prev_month_num)
        
    # Last day of the previous month
    lastDaylastMonth = month_Days.days_in_month(thisYear,prev_month_num)
    
    # Last day of the previous year
    lastDaypreviousYear = month_Days.days_in_month(prevYear,12)
        
    # Assign some needed variables
    path_name = '/home/ec2-user/'
    platform = "Tempest"
    xls_suffix = '.xlsx'
    
    if todayDay == 1:
        xls_filename = f'{prev_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}{prev_month}_{thisYear}_{platform}{xls_suffix}'
        return(xls_filename, xls_fullname, path_name, yesterdayDay, prev_month, thisYear, lastDaylastMonth)
    
    if todayDay == 1 and this_month == 'January':
        xls_filename = f'December_{prevYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}December_{prevYear}_{platform}{xls_suffix}'
        return(xls_filename, xls_fullname, path_name, yesterdayDay, prev_month, prevYear, lastDayprevYear)
        
    else:
        xls_filename = f'{this_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}{this_month}_{thisYear}_{platform}{xls_suffix}'
    
        return(xls_filename, xls_fullname, path_name, todayDay, this_month, thisYear, lastDaythisMonth)   
    


# In[5]:


import datetime
from datetime import timedelta
from datetime import date
import month_Days

def davis():
    
    # Getting today's date and create variables based on it

    # Today
    today = date.today()
    todayDate = datetime.date.today()
    yesterday = today - timedelta(days = 1)

    print("Today is: ", today)
    todayDay = today.strftime("%d")
    todayDay = int(todayDay)
    print("The day of the month is: ", todayDay, "\n")

    # Present month
    this_month = (todayDate.strftime("%B"))
    this_month_num = (todayDate.strftime("%m"))
    this_month_num = int(this_month_num)
    print("This month is :", this_month)
    
    # Current year
    thisYear = (todayDate.strftime("%Y"))
    print("This year is: ", thisYear)
    
    # previous information for today
    lastDaythisMonth = month_Days.days_in_month(thisYear,this_month_num)
    print("Number of days this month: ", lastDaythisMonth, "\n")
    
    # Yesterday
    print("Yesterday was: ", yesterday)
    yesterdayDay = yesterday.strftime("%d")
    yesterdayDay = int(yesterdayDay)
    date1 = yesterdayDay
    print(date1)
    print("The day of the month yesterday was: ", yesterdayDay, "\n")

    # Previous month
    last_month = todayDate.replace(day=1) - datetime.timedelta(days=1)
    prev_month = (last_month.strftime("%B"))
    prev_month_num = (last_month.strftime("%m"))
    prev_month_num = int(prev_month_num)
    print("Last month was: ", prev_month)
    
    # Previous year
    prev_year = todayDate.replace(day=1) - datetime.timedelta(days=365)
    prevYear = prev_year.strftime("%Y")
    print("Last year was: ", prevYear, "\n")
    
    # previous information for yesterday
    lastDaylastMonth = month_Days.days_in_month(thisYear,prev_month_num)
    print("Number of days last month: ", lastDaylastMonth, "\n")
    
    # Last day of the previous month
    lastDaylastMonth = month_Days.days_in_month(thisYear,prev_month_num)
    print("Last day of the previous month: ", lastDaylastMonth)

    # Last day of the previous year
    lastDaypreviousYear = month_Days.days_in_month(prevYear,12)
    print("Last day of the previous year: ", lastDaypreviousYear, "\n")

    # Calculate/assign some needd variables
    path_name = '/home/ec2-user/'
    platform = "Davis"
    xls_suffix = '.xlsx'
    
    if todayDay == 1:
        xls_filename = f'{prev_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}{prev_month}_{thisYear}_{platform}{xls_suffix}'
        print(xls_fullname)
        return(xls_filename, xls_fullname, path_name, date1, prev_month, thisYear, lastDaylastMonth)
    
    if todayDay == 1 and this_month == 'January':
        xls_filename = f'December_{prevYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}December_{prevYear}_{platform}{xls_suffix}'
        return(xls_filename, xls_fullfile, path_name, date1, prev_month, prevYear, lastDayprevYear)
        
    else:
        xls_filename = f'{this_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullfile = f'{path_name}{this_month}_{thisYear}_{platform}{xls_suffix}'
    
        return(xls_filename, xls_fullfile, path_name, todayDay, this_month, thisYear, lastDaythisMonth)   
    
    


# In[ ]:


import datetime
from datetime import timedelta
from datetime import date
import month_Days

def sqlWrite():
    
    # Getting today's date and create variables based on it

    # Today
    today = date.today()
    todayDate = datetime.date.today()
    yesterday = today - timedelta(days = 1)

    print("Today is: ", today)
    todayDay = today.strftime("%d")
    todayDay = int(todayDay)
    print("The day of the month is: ", todayDay, "\n")

    # Present month
    this_month = (todayDate.strftime("%B"))
    this_month_num = (todayDate.strftime("%m"))
    this_month_num = int(this_month_num)
    print("This month is :", this_month)
    
    # Current year
    thisYear = (todayDate.strftime("%Y"))
    print("This year is: ", thisYear)
    
    # previous information for today
    lastDaythisMonth = month_Days.days_in_month(thisYear,this_month_num)
    print("Number of days this month: ", lastDaythisMonth, "\n")
    
    # Yesterday
    print("Yesterday was: ", yesterday)
    yesterdayDay = yesterday.strftime("%d")
    yesterdayDay = int(yesterdayDay)
    print("The day of the month yesterday was: ", yesterdayDay, "\n")

    # Previous month
    last_month = todayDate.replace(day=1) - datetime.timedelta(days=1)
    prev_month = (last_month.strftime("%B"))
    prev_month_num = (last_month.strftime("%m"))
    prev_month_num = int(prev_month_num)
    print("Last month was: ", prev_month)
    
    # Previous year
    prev_year = todayDate.replace(day=1) - datetime.timedelta(days=365)
    prevYear = prev_year.strftime("%Y")
    print("Last year was: ", prevYear, "\n")
    
    # previous information for yesterday
    lastDaylastMonth = month_Days.days_in_month(thisYear,prev_month_num)
    print("Number of days last month: ", lastDaylastMonth, "\n")
    
    # Last day of the previous month
    lastDaylastMonth = month_Days.days_in_month(thisYear,prev_month_num)
    print("Last day of the previous month: ", lastDaylastMonth)

    # Last day of the previous year
    lastDaypreviousYear = month_Days.days_in_month(prevYear,12)
    print("Last day of the previous year: ", lastDaypreviousYear, "\n")

    # Calculate/assign some needd variables
    path_name = '/home/ec2-user/'
    platform = "Tempest"
    xls_suffix = '.xlsx'
    
    if todayDay == 1:
        xls_filename = f'{prev_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}{prev_month}_{thisYear}_{platform}{xls_suffix}'
        print(xls_fullname)
        return(xls_filename, xls_fullname, path_name, yesterdayDay, prev_month_num, thisYear, lastDaylastMonth)
    
    if todayDay == 1 and this_month == 'January':
        xls_filename = f'December_{prevYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}December_{prevYear}_{platform}{xls_suffix}'
        return(xls_filename, xls_fullfile, path_name, date1, prev_month, prevYear, lastDayprevYear)
        
    else:
        xls_filename = f'{this_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullfile = f'{path_name}{this_month}_{thisYear}_{platform}{xls_suffix}'
    
        return(xls_filename, xls_fullfile, path_name, todayDay, yesterdayDay, this_month_num, thisYear, lastDaythisMonth)   
    


# In[ ]:




