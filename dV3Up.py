#!/usr/bin/env python
# coding: utf-8

# In[50]:


import calcOneDay
import getDays
from datetime import datetime, timedelta
import calcTimeNow
import daysAndDates
import logging
import checkDST

def logdV3():
    
    """Set up logging for this script"""
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    #file_handler = logging.FileHandler('/home/ec2-user/davisPMUpdate.log')
    file_handler = logging.FileHandler('/Users/jameshayes/Sites/dV3Up.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)  


# In[63]:


import calcOneDay
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


# In[61]:


import pandas as pd
from pandas import DataFrame, Series
import math
from tableWrite import tableWrite
import daysAndDatesNew

def createF6(df):
    
    """Create FG data from the newly created and passed dataframe"""
    
    max_temp  = (df.sort_values(by='temp_hi', ascending=False))
    max_T = max_temp.iloc[:1]
    max_T_time = int(max_T['temp_hi_at'])
    maxT = max_T['temp_hi'].values[0]
    maxT = round(maxT)
    print(maxT)

    min_temp  = (df.sort_values(by='temp_lo', ascending=True))
    min_T = min_temp.iloc[:1]
    min_T_time = int(min_T['temp_lo_at'])
    minT = min_T['temp_lo'].values[0]
    minT = round(minT)

    dew_max = (df.sort_values(by='dew_point_hi', ascending=False))
    dew_max1 = dew_max.iloc[:1]
    dewMax = dew_max1['dew_point_hi'].values[0]
    dewMaxT = round(dewMax)

    dew_min = (df.sort_values(by='dew_point_lo', ascending=True))
    dew_min1 = dew_min.iloc[:1]
    dewMin = dew_min1['dew_point_lo'].values[0]
    dewMinT = round(dewMin)

    rain = df['rainfall_in'].sum()
    avgTemp = math.ceil((int(maxT + minT)/2))

    hdd = (65 - avgTemp)
    if hdd < 0:
        hdd = 0
    cdd = (avgTemp - 65)
    if cdd < 0:
        cdd = 0          
 
    return(maxT, minT, dewMaxT, dewMinT, rain, avgTemp, hdd, cdd)
    
df = getAndStore()
createF6(df)


# In[56]:


import sandbox1
import sandbox2
import daysAndDatesNew
import createF6

#
# Import data for use in the alamanc
#

dayInfo = daysAndDatesNew.daysAndDatesNew()
month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])

sdf = createF6.createF6(df)
print(sdf)
maxT, minT, dewMaxT, throttle, rain, avgTemp, hdd, cdd = sdf[0], sdf[1], sdf[2], sdf[3], sdf[4], sdf[5], sdf[6], sdf[7]

nmlData = sandbox2.sandbox2()
nmlHi = nmlData[3]
nmlLo = nmlData[4]

highData = sandbox1.recordHigh()
lowData = sandbox1.recordLow()
rainData = sandbox1.recordRain()

highPhrase = highData[2]
lowPhrase = lowData[2]
rainPhrase = rainData[2]

#filePath = '/var/www/html/000/climoDavisTest111.txt'
filePath = '/Users/jameshayes/Sites/climoDavis999.txt'

def almanac():
    
    """Set and and write the daily almanac"""

    with open(f'{filePath}','w') as outfile1: 
    #with open('/var/www/html/000/climoDavisText.txt','w') as outfile1: 
        print(f'Daily almanac for {month} {date}, {year}', file = outfile1)
        print('\n', file = outfile1)
        print(f'The high so far today is {maxT} degrees', file = outfile1)
        print(f'The low so far today is {minT} degrees', file = outfile1)
        print(f'The average temperature is {avgTemp} degrees', file = outfile1)
        print(f'The rainfall so far today is {("%.2f" % rain)} inches', file = outfile1)
        if hdd == 0:
            print('')
        else:
            print(f'There were {hdd} heating degree days', file = outfile1)
        if cdd == 0:
            print('')
        else:
            print(f'There were {cdd} cooling degree days', file = outfile1)
            
        print('\n', file = outfile1)        
    
    
        if date == 1:
            print(f'Normal and Record information for {nextMonth} {nextDay}, {year}', file = outfile1)
            print('\n', file = outfile1)
            print(f'The normal high for today is {nmlHi} degrees', file = outfile1)
            print(f'The normal low for today is {nmlLo} degrees' , file = outfile1)
            print('\n', file = outfile1)
            print(highPhrase, file = outfile1)
            print(lowPhrase, file = outfile1)
            print(rainPhrase, file = outfile1)  
        
        else:
            print(f'Normal and Record information for {month} {date}, {year}', file = outfile1)
            print('\n', file = outfile1)
            print(f'The normal high for today is {nmlHi} degrees', file = outfile1)
            print(f'The normal low for today is {nmlLo} degrees' , file = outfile1)
            print('\n', file = outfile1)
            print(highPhrase, file = outfile1)
            print(lowPhrase, file = outfile1)
            print(rainPhrase, file = outfile1)  
            
almanac()            
        


# In[ ]:





# In[ ]:




