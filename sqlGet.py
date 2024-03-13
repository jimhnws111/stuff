#!/usr/bin/env python
# coding: utf-8

# In[3]:


import datetime
from datetime import timedelta
from datetime import date
import month_Days

def sqlGet():
    
    # Getting today's date and create variables based on it

    # Today
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
    
    # Calculate/assign some needd variables
    path_name = '/home/ec2-user/'
    platform = "Tempest"
    xls_suffix = '.xlsx'
    
    if todayDay == 1:
        xls_filename = f'{prev_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}{prev_month}_{thisYear}_{platform}{xls_suffix}'
        print(xls_fullname)
        return(xls_filename, xls_fullname, path_name, date1, prev_month, prev_month_num, thisYear, lastDaylastMonth)
    
    if todayDay == 1 and this_month == 'January':
        xls_filename = f'December_{prevYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}December_{prevYear}_{platform}{xls_suffix}'
        return(xls_filename, xls_fullfile, path_name, date1, prev_month, prev_month_num, prevYear, lastDayprevYear)
        
    else:
        xls_filename = f'{this_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullfile = f'{path_name}{this_month}_{thisYear}_{platform}{xls_suffix}'
    
        return(xls_filename, xls_fullfile, path_name, todayDay, yesterdayDay, this_month, this_month_num, thisYear, lastDaythisMonth)   
    


# In[2]:


sqlGet()


# In[ ]:




