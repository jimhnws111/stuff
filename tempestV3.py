#!/usr/bin/env python
# coding: utf-8

# In[155]:


import logging
import os

#
# Set some logging info
#

def logTempest():
    
    """Set up logging for the script"""

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

    file_handler = logging.FileHandler('/home/ec2-user/tempestComp.log')
    #file_handler = logging.FileHandler('/Users/jameshayes/tempestComp.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)   


# In[156]:


import calcOneDay
import getDays
import daysAndDatesNew
from datetime import datetime, timedelta

def getDateInfo():
    
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


# In[157]:


import datetime
from datetime import datetime
import dataFile
import getNameNumbers
import requests
import getData

#
# Get data from the Tempest database 
#

startEnd = getData.getData()
start, end = startEnd[0], startEnd[1]

def dataFromTempest():
    
    """Create information to retrieve info from the Tempest API"""

    token = '877f6425-04a5-4f33-86e7-7123b7ef53d9'
    protocol = 'https://'
    urlSiteDevice = 'swd.weatherflow.com/swd/rest/observations/device/'
    urlSiteStation = 'swd.weatherflow.com/swd/rest/observations/station/'
    deviceID = '246921'
    stationID = '95775'
    preToken = '&token='
    preStart = '?time_start='
    preEnd = '&time_end='
    start_time = start
    end_time = end
    dayOffset = '&day_offset=1'
    format1 = '&format=csv'

    #
    # Put it together
    # 

    goGetDeviceSummary = (f'{protocol}{urlSiteDevice}{deviceID}{preStart}{start_time}{preEnd}{end_time}{format1}{preToken}{token}')
    r =  requests.get(goGetDeviceSummary)

    path = '/home/ec2-user/'
    #path = '/Users/jameshayes/'
    file_name = 'tempest_temp.csv'
    full_file = f'{path}{file_name}'

    with open(full_file,'w') as fd:
         fd.write(r.text)         


# In[158]:


import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import math

def createF6Tempest():
    
    """Read in data from text file and create needed F6 data"""

    df = pd.read_csv('/home/ec2-user/tempest_temp.csv', index_col=False)
    #df = pd.read_csv('/Users/jameshayes/tempest_temp.csv', index_col=False)

    #
    # Calculate needed F6 data
    #

    max_temp  = (df.sort_values(by='temperature', ascending=False))
    max_T = max_temp.iloc[:1]
    maxT = max_T['temperature'].values[0]
    maxT = round((maxT*1.8) + 32)

    min_temp  = (df.sort_values(by='temperature', ascending=True))
    min_T = min_temp.iloc[:1]
    minT = min_T['temperature'].values[0]
    minT = round((minT*1.8) + 32)

    max_pres = (df.sort_values(by='pressure', ascending=False))
    max_P = max_pres.iloc[:1]
    maxP = max_P['pressure'].values[0]

    min_pres = (df.sort_values(by='pressure', ascending=True))
    min_P = min_pres.iloc[:1]
    minP = min_P['pressure'].values[0]

    cor_rain = (df.sort_values(by='local_daily_precip_final', ascending=False))
    corR_rain = cor_rain.iloc[:1]
    corR = corR_rain['local_daily_precip_final'].values[0]
    corR = round((corR*0.03937), 2)

    tot_rain = df['precip'].sum()
    totR = round((tot_rain*0.03937), 2)

    strike_distance = (df.sort_values(by='strike_distance', ascending=False))
    lightning1 = (df['strike_distance'].between(1,8))
    lightning2 = (df['strike_distance'].between(9,16))

    df.insert(10,'lightning1',lightning1)
    df.insert(11,'lightning2',lightning2)

    #
    # Determine if the strike distance is close enough to count as a thunderstorm
    #

    x = len(df)
    a = 0

    while a < x:
            if (df['lightning1'] == True).any():
                q = "Yes"
            else:
                q = "No"
            if (df['lightning2'] == True).any():   
                r1 = "Yes"
            else:
                r1 = "No"
            a += 1    

    avgTemp = math.ceil((int(maxT + minT)/2))

    hdd = (65 - avgTemp)
    if hdd < 0:
        hdd = 0
    cdd = (avgTemp - 65)
    if cdd < 0:
        cdd = 0      
               
    return (maxT, minT, maxP, minP, corR, totR, q, r1, avgTemp, hdd, cdd)    


# In[159]:


import sqlalchemy
import mysql.connector
import sqlite3
import os
import pandas as pd
      
def rearrangeDF():
    
    """Rearrange the Pandas DataFrame to match the SQL table"""    
        
    dayInfo = daysAndDatesNew.daysAndDatesNew()
    month, month_num, date, year, yesterday = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3], dayInfo[4]
    yesterday = int(dayInfo[4])
    f6data = createF6Tempest()
    maxT, minT, maxP, minP, corR, totR, q, r1, avgTemp, hdd, cdd = f6data[0], f6data[1], f6data[2], f6data[3], f6data[4], f6data[5], f6data[6], f6data[7], f6data[8], f6data[9], f6data[10]
           
    df2 = pd.DataFrame(columns = ['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10'])
    newRow = pd.DataFrame({'Year': year, 'Month': month_num, 'Date': yesterday, 'High': maxT, 'Low': minT, 'Average': avgTemp, 'HDD': hdd, 'CDD': cdd, 'totR': totR, 'corR': corR, 'Lightning1_5': q, 'Lightning6_10': r1 }, index = [yesterday])
    df2 = pd.concat([newRow, df2]).reset_index(drop = True)      
        
    return(df2)
       
rearrangeDF()

def writeToTable(df2):

    db_user = 'chuckwx'
    db_password = 'jfr716!!00'
    
    database_username = db_user
    database_password = db_password
    database_ip       = '3.135.162.69'
    database_name     = 'tempestf6'
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                   format(database_username, database_password, 
                                                   database_ip, database_name), connect_args={'connect_timeout': 30})
    df2.to_sql(con=database_connection, name='tempestV3', if_exists='append', index = False)

df2 = rearrangeDF()    
writeToTable(df2)


# In[160]:


import pymysql as dbapi
import pandas as pd
from pretty_html_table import build_table
import os
import daysAndDatesNew

dayInfo = daysAndDatesNew.daysAndDatesNew()
month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])

db_user = 'chuckwx'
db_password = 'jfr716!!00'
#db_user = os.environ.get('dbUser')
#db_password = os.environ.get('dbPass')

def makeHTMLTables():
    
    """Pop data out of the SQL table, read it into a Pandas DataFrame, and 
    create an HTML table for display"""
    
    
    QUERY2 = """SELECT * FROM tempestV3 
             WHERE Month = %s""" % (month_num)

    #
    # use environmental variables for the SQL query
    #


    database_username = db_user
    database_password = db_password

    db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'tempestf6')
    html_path = '/var/www/html/000/'
    #html_path = '/Users/jameshayes/Sites/'

    cur = db.cursor()
    cur.execute(QUERY2)
    dateResult = cur.fetchall()

    colNames = (['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10']) 
    df3 = pd.DataFrame(dateResult, columns = colNames) 
    df3 = df3.drop(df3.columns[[0, 1]], axis = 1)
    df3 = df3.reindex(columns=['Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10'])
    df3.to_html(f'{html_path}tempest_Throttle.html', index = False) 

    html_table_green_light = build_table(df3, 'green_light', text_align='center', font_size='32px')

    with open(f'{html_path}tempestLocalV3.html', 'w') as f:
              f.write(html_table_green_light)   
            
makeHTMLTables()         


# In[161]:


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
#db_user = os.environ.get('dbUser')
#db_password = os.environ.get('dbPass')

month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])

def getTableData():
    
    """Retrieve normal and record data from various mySQL tables for the almanac"""

    QUERY = """SELECT * FROM avgHiLo 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)

    database_username = db_user
    database_password = db_password

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
    recYearNum = len(result2)
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
    
getTableData()   


# In[162]:


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

#
# Convert df2 to something easier to use with text
#

zsw = rearrangeDF()
maxT = zsw['High'].astype(int)    
maxT = int(maxT)
minT = zsw['Low'].astype(int) 
minT = int(minT)
avgTemp = zsw['Average'].astype(int) 
avgTemp = int(avgTemp)
hdd = zsw['HDD'].astype(int)
hdd = int(hdd)
cdd = zsw['CDD'].astype(int)
cdd = int(cdd)
totR = zsw['totR'].astype(float)
totR = float(totR)
corR = zsw['corR'].astype(float)
corR = float(corR)
lightning1 = zsw['Lightning1_5'].astype(str)
#lightning1 = str(lightning1)
lightning2 = zsw['Lightning6_10'].astype(str)
#lightning2 = str(lightning2)

#
# Retrieve normal and record data that has been checked for 
# multiple values 
#

nmlData = sandbox2.sandbox2()
nmlHi = nmlData[3]
nmlLo = nmlData[4]

highData = sandbox1.recordHigh()
lowData = sandbox1.recordLow()
rainData = sandbox1.recordRain()

highPhrase = highData[2]
lowPhrase = lowData[2]
rainPhrase = rainData[2]

filePath = '/var/www/html/000/climoTempest112.txt'
#filePath = '/Users/jameshayes/Sites/climoTempestText112.txt'

def almanac_Tempest():

    """Set and and write the daily almanac"""


    with open(f'{filePath}','w') as outfile1: 
        print(f'Daily almanac for {month} {yesterday}, {year}', file = outfile1)
        print('\n', file = outfile1)
        print(f'The high yesterday was {maxT} degrees', file = outfile1)
        print(f'The low yesterday was {minT} degrees', file = outfile1)
        print(f'The average temperature was {avgTemp} degrees', file = outfile1)
        print(f'The rainfall yesterday was {("%.2f" % corR)} inches', file = outfile1)
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
            
almanac_Tempest()            


# In[ ]:




