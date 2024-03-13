#!/usr/bin/env python
# coding: utf-8

# In[13]:


import calcOneDay
import getNameNumbers
import sqlGet
import requests

#
# Calculate the time and date for end of day calculations
#

xy = calcOneDay.calcOneDay()
start, end = (xy[0], xy[1])

#
# figure out the date today
#

gD = sqlGet.sqlGet()
nextDay, date, month, month_num, year = gD[3], gD[4], gD[5], gD[6], gD[7]


# In[12]:


import datetime
from datetime import datetime
import dataFile
import getNameNumbers

#
# Get data from the Tempest database for the new station
#

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
#print(goGetDeviceSummary)
r =  requests.get(goGetDeviceSummary)
path = '/home/ec2-user/'
file_name = 'tempest_test.csv'
full_file = f'{path}{file_name}'

with open(full_file,'w') as fd:
     fd.write(r.text)


# In[ ]:


import pandas as pd
import dataFile
import getNameNumbers
import sqlalchemy
import mysql.connector
import sqlite3
import datetime
from datetime import datetime
from dateutil.tz import tzutc, tzlocal
import pytz
import math

#
# Read in the CSV file for processing in pandas
#

path = '/home/ec2-user/'
file_name = 'tempest_test.csv'
full_file = f'{path}{file_name}'
df = pd.read_csv(full_file, index_col=False)

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

maxT1 = df['temperature'].max()
maxT1 = round((maxT1 * 1.8) + 32)
max_temp  = (df.sort_values(by='temperature', ascending=False))
max_T = max_temp.iloc[:1]
max_T_time = int(max_T['timestamp'])
print(type(max_T_time))
maxT = max_T['temperature'].values[0]
maxT = round((maxT*1.8) + 32)

timezone = pytz.timezone("America/New_York")
dt_object = datetime.fromtimestamp(max_T_time)
localT = dt_object.astimezone(timezone)
hiTime = localT.strftime('%I:%M %p')  

minT1 = df['temperature'].min()
minT1 = round((minT1 * 1.8) + 32)
min_temp  = (df.sort_values(by='temperature', ascending=True))
min_T = min_temp.iloc[:1]
min_T_time = int(min_T['timestamp'])
minT = min_T['temperature'].values[0]
minT = round((minT*1.8) + 32)

dt_object1 = datetime.fromtimestamp(min_T_time)
localT1 = dt_object1.astimezone(timezone)
loTime = localT1.strftime('%I:%M %p')  

avgTemp = math.ceil(((maxT + minT)/2))

# 
# Calculate heating/cooling degree days
#

hdd = (65 - avgTemp)
if hdd < 0:
    hdd = 0
cdd = (avgTemp - 65)
if cdd < 0:
    cdd = 0

cor_rain = (df.sort_values(by='local_daily_precip_final', ascending=False))
corR_rain = cor_rain.iloc[:1]
corR = corR_rain['local_daily_precip_final'].values[0]
corR = round((corR*0.03937), 2)
corR = "{:.2f}".format(corR)

tot_rain = df['precip'].sum()
totR = round((tot_rain*0.03937), 2)

strike_distance = (df.sort_values(by='strike_distance', ascending=False))
lightning1 = (df['strike_distance'].between(1,8))
lightning2 = (df['strike_distance'].between(9,16))

df.insert(10,'lightning1',lightning1)
df.insert(11,'lightning2',lightning2)

#Determine if the strike distance is close enough to count as a thunderstorm
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


# In[1]:


import pandas as pd
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate

#
# Get normal highs and lows
#

QUERY = """SELECT * FROM avgHiLo 
           WHERE Month = %s 
           AND Day = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

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
           AND Day = %s""" % (month_num, nextDay)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

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
           AND Day = %s""" % (month_num, nextDay)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY2)
result2 = cur.fetchall()
recordLow = result2[0]
recLow = int(recordLow[1])
recLowYear = int(recordLow[4])

#
# Get the record rainfall for the date
#

QUERY3 = """SELECT * FROM recRain 
           WHERE Month = %s 
           AND Day = %s""" % (month_num, nextDay)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY3)
result3 = cur.fetchall()
recordRain = result3[0]
recRain = recordRain[1]
recRainYear = int(recordRain[4])

#
# Data setup for tabulate
# 

'''
climo_data = [["Month", "Day", "Year", "High", "Low", "Avg", "HDD", "CDD", "Rain"],
             [month, date, year, maxT, minT, avgTemp, hdd, cdd, corR]]

with open('/var/www/html/000/climo.html', 'w') as f:
    f.write(tabulate(climo_data, headers = 'firstrow', tablefmt = 'html'))
    

record_data = [["Month", "Day", "Year", "Record High", "Year", "Record Low", "Year", "Record Rainfall", "Year"],
             [month, nextDay, year, recHigh, recHighYear, recLow, recLowYear, recRain, recRainYear]]

with open('/var/www/html/000/day_records.html', 'w') as f:
    f.write(tabulate(record_data, headers = 'firstrow', tablefmt = 'html'))
  
with open('/var/www/html/000/climo1.html','w') as outfile1: 
    print(f'This is the daily almanac for {month} {date}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The high today was {maxT} at {hiTime}', file = outfile1)
    print(f'The low today was {minT} at {loTime}', file = outfile1)
    print(f'The average temperature was {avgTemp}', file = outfile1)
    print(f'The rainfall today was {corR} inches', file = outfile1)
    print(f'There were {hdd} heating degree days today', file = outfile1)
    print(f'There were {cdd} cooling degree days today', file = outfile1)

'''
with open('/var/www/html/000/climo.txt','w') as outfile1: 
    print(f'Daily almanac for {month} {date}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The high today was {maxT} at {hiTime}', file = outfile1)
    print(f'The low today was {minT} at {loTime}', file = outfile1)
    print(f'The average temperature was {avgTemp}', file = outfile1)
    print(f'The rainfall today was {corR} inches', file = outfile1)
    print(f'There were {hdd} heating degree days today', file = outfile1)
    print(f'There were {cdd} cooling degree days today', file = outfile1)
    print('\n', file = outfile1)
    print(f'Record information for {month} {nextDay}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The record high for today is {recHigh} in {recHighYear}', file = outfile1)
    print(f'The record low for today is {recLow} in {recLowYear}', file = outfile1)
    print(f'The record rainfall for today is {recRain} inches in {recRainYear}', file = outfile1)

