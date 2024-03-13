#!/usr/bin/env python
# coding: utf-8

# In[37]:


from datetime import datetime, timedelta
import calcOneDay
import getDays

def daysAndDates():

    # Calculate the time and date for end of day calculations

    xy = calcOneDay.calcOneDay()
    start, end = (xy[0], xy[1])

    todayInfo = getDays.getToday()
    day = int(todayInfo[2])
    yesterdayInfo = getDays.getYesterday()
    tomorrowInfo = getDays.getTomorrow()
        
    if day == 1:
        month, month_num, date, year = yesterdayInfo[0], yesterdayInfo[1], yesterdayInfo[2], yesterdayInfo[3]
    else:
        month, month_num, date, year = todayInfo[0], todayInfo[1], todayInfo[2], todayInfo[3]        
      
    yesterday = int(yesterdayInfo[2])
    nextDay = int(tomorrowInfo[2])
        
    return(month, month_num, date, year, yesterday, nextDay)


# In[38]:


daysAndDates()


# In[ ]:




