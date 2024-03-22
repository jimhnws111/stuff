#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import getDays
from datetime import datetime, timedelta
import calcTimeNow
import daysAndDatesNew
import checkDST
from dataFromDavis import dataFromDavis
from getAndStore import getAndStore
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from dateutil.tz import tzutc, tzlocal
import pytz

def timesAndDates():
    
    """Calculate the time and date for end of day calculations
    First determine whether we are in DST or not"""

    # Check DST setting
    isDST = checkDST.checkDST()
    print(isDST)

    if isDST == 1:
        now = datetime.now()
        end = int(datetime.timestamp(now))
        start = (end - 55800)
        start = str(start)
        end = str(end)
        
    else:
        now = datetime.now()
        end = int(datetime.timestamp(now))
        start = (end - 59400)
        start = str(start)
        end = str(end)    

    dayInfo = daysAndDatesNew.daysAndDatesNew()
    month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
    yesterday = int(dayInfo[4])
    nextDay = int(dayInfo[5])
    month_num = int(month_num)
    date = int(date)
        
    return(start, end, month, month_num, date, year, yesterday, nextDay)  

timesAndDates()
dataFromDavis()
getAndStore()

