#!/usr/bin/env python
# coding: utf-8

# In[17]:


import calcOneDay
import getDays
from datetime import datetime, timedelta
import daysAndDatesNew

# Calculate the time and date for end of day calculations

def getData1():

    xy = calcOneDay.calcOneDay()
    start, end = (xy[0], xy[1])
    dayInfo = daysAndDatesNew.daysAndDatesNew()

    month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
    yesterday = int(dayInfo[4])
    nextDay = int(dayInfo[5])
        
    return(start, end, month, month_num, date, year)


# In[18]:


getData1()


# In[ ]:




