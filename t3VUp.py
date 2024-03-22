#!/usr/bin/env python
# coding: utf-8

# In[16]:


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
    file_handler = logging.FileHandler('/home/ec2-user/davisPMUpdate.log')
    #file_handler = logging.FileHandler('/Users/jameshayes/Sites/dV3Up.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)  


# In[17]:


import calcOneDay
import getDays
import daysAndDatesNew
from datetime import datetime, timedelta
import datetime
import dataFile
import getNameNumbers
import requests
import getData
from dataFromTempest import dataFromTempest

def getUpDateInfo():
    
    """Calculating some date/time information to retrieve and process data"""

    xy = calcOneDay.calcOneDay()
    start, end = (xy[0], xy[1])
    dayInfo = daysAndDatesNew.daysAndDatesNew()
    #logger.info('Start time: {}'.format(start)) 
    #logger.info('End time: {}'.format(end))
    
    month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
    #logger.info('Month, MonthNumber, Date, Year: {} {} {} {}'.format(month, month_num, date, year))

    yesterday = int(dayInfo[4])
    nextDay = int(dayInfo[5])
    
    return(start, end, month, month_num, date, year)

getUpDateInfo()


# In[18]:


import datetime
from datetime import datetime
import dataFile
import getNameNumbers
import requests
import getData
from dataFromTempest import dataFromTempest

#
# Get the start and end times, depending on product
#

def reckonTime():
    
    """Make sure the proper version of dataFromTempest
    is executed at the proper time"""

    now = datetime.now()
    x = now.strftime("%Y-%m-%d")
    print("This script started at:", now)

    t1 = ' 20:00'
    t2 = ' 21:00'
    time1 = x + t1
    time2 = x + t2
    val1 = datetime.strptime(time1, "%Y-%m-%d %H:%M")
    val2 = datetime.strptime(time2, "%Y-%m-%d %H:%M")

    if val1 < now < val2:
        end = int(datetime.timestamp(now))
        start = (end - 55800)
        start = str(start)
        end = str(end)    
        
    else:
        startEnd = getData.getData()
        start, end = startEnd[0], startEnd[1]   
        
reckonTime()    
dataFromTempest()
createF6Tempest()


# In[25]:


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

sdf = createF6Tempest()
maxT, minT, maxP, minP, corR, totR, q, r1, avgTemp, hdd, cdd = sdf[0], sdf[1], sdf[2], sdf[3], sdf[4], sdf[5], \
                                                               sdf[6], sdf[7], sdf[8], sdf[9], sdf[10],
nmlData = sandbox2.sandbox2()
nmlHi = nmlData[3]
nmlLo = nmlData[4]

highData = sandbox1.recordHigh()
lowData = sandbox1.recordLow()
rainData = sandbox1.recordRain()

highPhrase = highData[2]
lowPhrase = lowData[2]
rainPhrase = rainData[2]

filePath = '/var/www/html/000/climoDavisTest111.txt'
#filePath = '/Users/jameshayes/Sites/climoDavis998.txt'

def almanacUpT():
    
    """Set and and write the daily almanac"""

    with open(f'{filePath}','w') as outfile1: 
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
            
almanacUpT()            


# In[ ]:




