#!/usr/bin/env python
# coding: utf-8

# In[201]:


# import datetime

import datetime
#from datetime import datetime
from datetime import timedelta
from datetime import date
import time
import month_Days
from dateutil.tz import tzutc, tzlocal
import pytz

def tempest_ec2():   
 
    utc_datetime = datetime.datetime.now(tzutc())
    local_timezone = pytz.timezone('America/New_York')
    timeInNewYork = datetime.datetime.now(local_timezone)
    local_t = timeInNewYork.astimezone(local_timezone)  
           
    # define variables for day, month, year
    today = local_t.strftime("%Y-%m-%d")
    today1 = datetime.datetime.strptime(today,"%Y-%m-%d")
    todayDate = local_t.strftime("%-d")
    yesterday = local_t - timedelta(days = 1)
    yDay = yesterday.strftime("%x")

    print("Today is: ", today)
    todayDay = local_t.strftime("%d")
    print("The day of the month is: ", todayDay, "\n")

    # Present month
    this_month = (local_t.strftime("%B"))
    this_month_num = (local_t.strftime("%m"))
    this_month_num = int(this_month_num)
    print("This month is :", this_month)
    
    # Current year
    thisYear = (local_t.strftime("%Y"))
    print("This year is: ", thisYear)
    
    # previous information for today
    lastDaythisMonth = month_Days.days_in_month(thisYear,this_month_num)
    print("Number of days this month: ", lastDaythisMonth, "\n")
    
    # Yesterday
    print("Yesterday was: ", yDay)
    yesterdayDay = yesterday.strftime("%d")
    yesterdayDay = int(yesterdayDay)
    print("The day of the month yesterday was: ", yesterdayDay, "\n")

    # Previous month
    last_month = today1.replace(day=1) - datetime.timedelta(days=1)
    prev_month = (last_month.strftime("%B"))
    prev_month_num = (last_month.strftime("%m"))
    prev_month_num = int(prev_month_num)
    print("Last month was: ", prev_month)
    
    # Previous year
    prev_year = today1.replace(day=1) - datetime.timedelta(days=365)
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
    
    # Assign some needed variables
    path_name = '/home/ec2-user/'
    platform = "Tempest"
    xls_suffix = '.xlsx'
    
    if todayDay == 1:
        xls_filename = f'{prev_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}{prev_month}_{thisYear}_{platform}{xls_suffix}'
        return(xls_filename, xls_fullfile, path_name, yesterdayDay, prev_month, thisYear, lastDaylastMonth)
    
    if todayDay == 1 and this_month == 'January':
        xls_filename = f'December_{prevYear}_{platform}{xls_suffix}'
        xls_fullname = f'{path_name}December_{prevYear}_{platform}{xls_suffix}'
        return(xls_filename, xls_fullfile, path_name, yesterdayDay, prev_month, prevYear, lastDayprevYear)
        
    else:
        xls_filename = f'{this_month}_{thisYear}_{platform}{xls_suffix}'
        xls_fullfile = f'{path_name}{this_month}_{thisYear}_{platform}{xls_suffix}'
    
        return(xls_filename, xls_fullfile, path_name, todayDay, this_month, thisYear, lastDaythisMonth)   
    


# In[200]:


tempest_ec2()


# In[ ]:




