#!/usr/bin/env python
# coding: utf-8

# In[152]:


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


# In[153]:


from datetime import datetime, timedelta
import daysAndDatesNew
import checkDST
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from dateutil.tz import tzutc, tzlocal
import pytz

def timesAndDates():
    
    """Calculate the time and date for end of day calculations
    First determine whether we are in DST or not"""   

    dayInfo = daysAndDatesNew.daysAndDatesNew()
    month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
    yesterday = int(dayInfo[4])
    nextDay = int(dayInfo[5])
    month_num = int(month_num)
    date = int(date)
                               
    return(month, month_num, date, year, yesterday, nextDay) 


# In[157]:


import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json
import dataFile
import getData
import checkDST

#
# Start the module
#

def dataFromDavis1():
    
    startEnd = getStartEnd.getStartEnd()
    start, end = startEnd[0], startEnd[1]
 
    print(start, end)    
    
    
    parameters = {
      "api-key": "vy8jbrjsxlbwgojepq3vfyfqfywyhvbd", 
      "api-secret": "sdqfm6wdfy9w0pqp2vdka38o6b4vcsvc",
      "station-id": 81211, 
      "end-timestamp": end,
      "start-timestamp": start,
      "t": int(time.time())
    }

    parameters = collections.OrderedDict(sorted(parameters.items()))

   #for key in parameters:
   #     print("Parameter name: \"{}\" has value \"{}\"".format(key, parameters[key]))

    apiSecret = parameters["api-secret"];
    parameters.pop("api-secret", None);

    data = ""
    for key in parameters:
        data = data + key + str(parameters[key])

    #logger.info('Data string to hash is: \"{}\"'.format(data))   


    apiSignature = hmac.new(
      apiSecret.encode('utf-8'),
      data.encode('utf-8'),
      hashlib.sha256
    ).hexdigest()


    #logger.info('API Signature is: \"{}\"'.format(apiSignature))

    # Building the URL to get the station

    first_part = ('https://api.weatherlink.com/v2/historic/81211?')
    api_key = ('api-key=vy8jbrjsxlbwgojepq3vfyfqfywyhvbd')
    add_apisig = ('&api-signature=')
    add_t = ('&t='+ str(int(time.time())))

    start1 = "&start-timestamp=" + start
    end1 = "&end-timestamp=" + end

    URLfinal = (first_part + api_key + add_t + start1 + end1 + add_apisig + apiSignature)

    r =  requests.get(URLfinal)
    davisAPI = (r.json())
    
    return(davisAPI)


# In[159]:


import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import sqlalchemy
from dateutil.tz import tzutc, tzlocal
import pytz
import os
import dataFromDavis1
import math

#
# Create some F6 data from the API data and write to a Pandas dataFrame 
#

def getAndStore():
    
    davisAPI = dataFromDavis1.dataFromDavis1()
    print(davisAPI)
    a = davisAPI['sensors']    
    b = a[1]
    c = (b['data'])

    df = pd.DataFrame(c) 
    df.rename(columns = {'ts':'timestamp'}, inplace = True)
   
    timezone = pytz.timezone("America/New_York")
    df['timeGroup'] = pd.to_datetime(df['timestamp'], unit='s')
    df['timeGroup'] = df['timeGroup'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    df['localTime'] = df['timeGroup'].dt.strftime('%I:%M %p')

    df = df.loc[:,['timestamp', 'temp_hi', 'temp_hi_at','temp_lo', 'temp_lo_at', 'rainfall_in', 'dew_point_hi', 'dew_point_lo',  'rain_rate_hi_in', 'rain_rate_hi_at', 'timeGroup', 'localTime']]   
    
    print(df)
    
    
    return(df)

#
# Calculate more variables from the dataFrame
#

import pandas as pd
from pandas import DataFrame, Series
import math

def createF6(df):
    
    max_temp  = (df.sort_values(by='temp_hi', ascending=False))
    max_T = max_temp.iloc[:1]
    max_T_time = int(max_T['temp_hi_at'])
    maxT = max_T['temp_hi'].values[0]
    maxT = round(maxT)

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


# In[160]:


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

filePath = '/var/www/html/000/climoDavis999.txt'
#filePath = '/Users/jameshayes/Sites/climoDavis999.txt'

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




