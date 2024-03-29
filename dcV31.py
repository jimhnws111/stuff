#!/usr/bin/env python
# coding: utf-8

# In[100]:


import logging
import os

#
# Set up some logging
#

def logIt():
    """ Setting up logging for the script"""

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler('/home/ec2-user/davisCompleteTest.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


# In[17]:


import calcOneDay
import getDays
from datetime import datetime, timedelta
import daysAndDatesNew

# Calculate the time and date for end of day calculations

def getData1():
    
    """calculating some date/time information to retrieve and process data"""
    

    xy = calcOneDay.calcOneDay()
    start, end = (xy[0], xy[1])
    dayInfo = daysAndDatesNew.daysAndDatesNew()

    month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
    yesterday = int(dayInfo[4])
    nextDay = int(dayInfo[5])
        
    return(start, end, month, month_num, date, year)


# In[18]:


import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json
import dataFile
import getData

#
# Get the data from the Davis API
#

startEnd = getData.getData()
start, end = startEnd[0], startEnd[1]

def dataFromDavis():
    """Create information to retrieve info from the Davis API"""
    
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


# In[80]:


import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import sqlalchemy
from dateutil.tz import tzutc, tzlocal
import pytz
import os
import dataFromDavis
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import math
import daysAndDatesNew

#
# Create some F6 data from the API data and write to a Pandas dataFrame 
#

def getAndStore():
    
    """Unpack the API dicionary and add a couple of elements to the dataframe"""
    
    davisAPI = dataFromDavis.dataFromDavis()
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
    
    return(df)

#
# Calculate more variables from the dataFrame
#

import pandas as pd
from pandas import DataFrame, Series
import math

def createF6(df):
    
    """Create FG data from the newly created and passed dataframe"""
    
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

def arrangeAndWrite():
    
    """Rearrange the dataframe to make a bit more sense and add a couple of elements"""
    
    dayInfo = daysAndDatesNew.daysAndDatesNew()
    month, month_num, date, year, yesterday = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3], dayInfo[4]
    yesterday = int(dayInfo[4])
    f6data = createF6(df)
    maxT, minT, dewMaxT, dewMinT, rain, avgTemp, hdd, cdd = f6data[0], f6data[1], f6data[2], f6data[3], f6data[4], f6data[5], f6data[6], f6data[7] 
 
    df2 = pd.DataFrame(columns = ['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
    newRow = pd.DataFrame({'Year': year, 'Month': month_num, 'Date': yesterday, 'High': maxT, 'Low': minT, 'Average': avgTemp, 'HDD': hdd, 'CDD': cdd, 'Rainfall' : rain, 'Max_Dew_Point': dewMaxT }, index = [yesterday])
    df2 = pd.concat([newRow, df2]).reset_index(drop = True)    
        
    return(df2)
    
arrangeAndWrite()  

def tableWrite(df2):
    
    """Write the Pandas DataFrame info to a mySQL table"""
  
    #db_user = os.environ.get('dbUser')
    #db_password = os.environ.get('dbPass')

    db_user = 'chuckwx'
    db_password = 'jfr716!!00'

    database_username = 'chuckwx'
    database_password = 'jfr716!!00'
    database_ip       = '3.135.162.69'
    database_name     = 'davisf6'
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(database_username, database_password, 
                                                          database_ip, database_name), connect_args={'connect_timeout': 30})
    df2.to_sql(con=database_connection, name='davisUpdate', if_exists='append', index = False)

df2 = arrangeAndWrite()    
tableWrite(df2)


# In[73]:


import pandas as pd
import pymysql as dbapi
from pretty_html_table import build_table
import os
import daysAndDatesNew

#
# use environmental variables for the SQL query
#

db_user = 'chuckwx'
db_password = 'jfr716!!00'
dayInfo = daysAndDatesNew.daysAndDatesNew()

month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])

def createHTMLTables():
    
    """Creare two HTML tables for the F6 data to be viewed"""

    #db_user = os.environ.get('dbUser')
    #db_password = os.environ.get('dbPass')

    QUERY2 = """SELECT * FROM davisV3 
             WHERE Month = %s""" % (month_num)


    html_path = '/var/www/html/000/'
    #html_path = '/Users/jameshayes/Sites/'
    db = dbapi.connect(host='3.135.162.69', user=db_user, passwd=db_password, database = 'davisf6', port = 3306)

    cur = db.cursor()
    cur.execute(QUERY2)
    dateResult = cur.fetchall()
    
    colNames = (['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point']) 
    pd.options.display.float_format = '{:,.2f}'.format
    df3 = pd.DataFrame(dateResult, columns = colNames) 
    df3 = df3.drop(df3.columns[[0, 1]], axis = 1)
    df3 = df3.reindex(columns=['Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
    df3.to_html(f'{html_path}throttledTest.html', index = False)     

    html_table_blue_light = build_table(df3, 'blue_light', text_align='center', font_size='32px')

    with open(f'{html_path}davisLocal.html', 'w') as f:
              f.write(html_table_blue_light)  
            
createHTMLTables()           


# In[74]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate
import os

db_user = 'chuckwx'
db_password = 'jfr716!!00'
month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])

def gatherData():  
    
    """Retrieve normal and record data from various mySQL tables for the almanac"""

    QUERY = """SELECT * FROM avgHiLo 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)


    db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

    cur = db.cursor()
    cur.execute(QUERY)
    result = cur.fetchall()

    dataset = result[0]
    nmlHi = int(dataset[3])
    nmlLo = int(dataset[4])

    #
    # Get the record high for the date
    #

    QUERY1 = """SELECT * FROM recHigh 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)


    db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

    cur = db.cursor()
    cur.execute(QUERY1)
    result1 = cur.fetchall()
    recordHigh = result1[0]
    recHigh = int(recordHigh[1])
    recHighYear = int(recordHigh[4])

    #
    # Get the record low for the date
    #

    QUERY2 = """SELECT * FROM recLow 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)


    db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

    cur = db.cursor()
    cur.execute(QUERY2)
    result2 = cur.fetchall()
    recYearNum =  len(result2)
    recordLow = result2[0]
    recLow = int(recordLow[1])
    recLowYear = int(recordLow[4])

    #
    # Get the record rainfall for the date
    #

    QUERY3 = """SELECT * FROM recRain 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)


    db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

    cur = db.cursor()
    cur.execute(QUERY3)
    result3 = cur.fetchall()

    recordRain = result3[0]
    recRain = recordRain[1]
    recRainYear = int(recordRain[4])
    
gatherData()   


# In[103]:


import pymysql as dbapi
import sys
import csv
import sandbox1
import sandbox2
import daysAndDatesNew

#
# Import data for use in the alamanc
#

month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])

sdf = createF6(df)
maxT, minT, dewMaxT, throttle, rainfall, avgTemp, hdd, cdd = sdf[0], sdf[1], sdf[2], sdf[3], sdf[4], sdf[5], sdf[6], sdf[7]

nmlData = sandbox2.sandbox2()
nmlHi = nmlData[3]
nmlLo = nmlData[4]

highData = sandbox1.recordHigh()
lowData = sandbox1.recordLow()
rainData = sandbox1.recordRain()

highPhrase = highData[2]
lowPhrase = lowData[2]
rainPhrase = rainData[2]

filePath = '/var/www/html/000/climoDavisText.txt'
#filePath = '/Users/jameshayes/Sites/climoDavisText111.txt'

def almanac():
    
    """Set and and write the daily almanac"""

    with open(f'{filePath}','w') as outfile1: 
        print(f'Daily almanac for {month} {yesterday}, {year}', file = outfile1)
        print('\n', file = outfile1)
        print(f'The high yesterday was {maxT} degrees', file = outfile1)
        print(f'The low yesterday was {minT} degrees', file = outfile1)
        print(f'The average temperature was {avgTemp} degrees', file = outfile1)
        print(f'The rainfall yesterday was {("%.2f" % rainfall)} inches', file = outfile1)
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




