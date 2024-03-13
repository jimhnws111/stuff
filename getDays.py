#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime, timedelta

def getToday():

    presentDay = datetime.now() 
    month_num = presentDay.strftime("%m")
    month = presentDay.strftime("%B")
    date = presentDay.strftime("%-d")
    year = presentDay.strftime("%Y")
    return(month, month_num, date, year)

def getYesterday():

    presentDay = datetime.now() 
    yesterDay = presentDay - timedelta(1)
    yesMonth_num = yesterDay.strftime("%m")
    yesMonth = yesterDay.strftime("%B")
    yesDate = yesterDay.strftime("%-d")
    yesYear = yesterDay.strftime("%Y")
    return(yesMonth, yesMonth_num, yesDate, yesYear)

def getTomorrow():    
    
    presentDay = datetime.now() 
    nextDay = presentDay + timedelta(1)
    nextMonth_num = nextDay.strftime("%m")
    nextMonth = nextDay.strftime("%B")
    nextDate = nextDay.strftime("%-d")
    nextYear = nextDay.strftime("%Y")
    return(nextMonth,nextMonth_num, nextDate, nextYear)

