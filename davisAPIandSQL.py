#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import urllib
import requests
import csv
import re
import calcOneDay
import sqlGet

# Calculate the time and date for end of day calculations

xy = calcOneDay.calcOneDay()
start, end = (xy[0], xy[1])
print(start,end)

gD = sqlGet.sqlGet()
nextDay, date, month, month_num, year = gD[3], gD[4], gD[5], gD[6], gD[7]


# In[ ]:


import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json
import dataFile
import pandas as pd
import math
import sqlalchemy
import mysql.connector
import sqlite3
from dateutil.tz import tzutc, tzlocal
import pytz

parameters = {
  "api-key": "vy8jbrjsxlbwgojepq3vfyfqfywyhvbd", 
  "api-secret": "sdqfm6wdfy9w0pqp2vdka38o6b4vcsvc",
  "station-id": 81211, 
  "end-timestamp": end,
  "start-timestamp": start,
  "t": int(time.time())
}

parameters = collections.OrderedDict(sorted(parameters.items()))

for key in parameters:
    print("Parameter name: \"{}\" has value \"{}\"".format(key, parameters[key]))

apiSecret = parameters["api-secret"];
parameters.pop("api-secret", None);

data = ""
for key in parameters:
    data = data + key + str(parameters[key])

print("Data string to hash is: \"{}\"".format(data))
print('\n')

"""
Calculate the HMAC SHA-256 hash that will be used as the API Signature.
"""
apiSignature = hmac.new(
  apiSecret.encode('utf-8'),
  data.encode('utf-8'),
  hashlib.sha256
).hexdigest()

"""
Let's see what the final API Signature looks like.
"""
print("API Signature is: \"{}\"".format(apiSignature))
print('\n')

# Building the URL to get the station

first_part = ('https://api.weatherlink.com/v2/historic/81211?')
api_key = ('api-key=vy8jbrjsxlbwgojepq3vfyfqfywyhvbd')
add_apisig = ('&api-signature=')
add_t = ('&t='+ str(int(time.time())))

start1 = "&start-timestamp=" + start
end1 = "&end-timestamp=" + end

#
URLfinal = (first_part + api_key + add_t + start1 + end1 + add_apisig + apiSignature)
# print(URLfinal)

r =  requests.get(URLfinal)
davisAPI = (r.json())


# In[ ]:


import sqlalchemy
from dateutil.tz import tzutc, tzlocal
import pytz

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

database_username = 'chuckwx'
database_password = 'jfr716!!00'
database_ip       = '3.135.162.69'
database_name     = 'davisInfo'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args={'connect_timeout': 30})
df.to_sql(con=database_connection, name='davisDB', if_exists='append')


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import math

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


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate
import sandbox2

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
recYearNum =  len(result2)
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
#sandbox1.recordRain(result3)
recordRain = result3[0]
recRain = recordRain[1]
recRainYear = int(recordRain[4])


# In[ ]:


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
with open('/var/www/html/000/climoDavisText.txt','w') as outfile1: 
    print(f'Daily almanac for {month} {date}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The high yesterday was {maxT}', file = outfile1)
    print(f'The low yesterday was {minT}', file = outfile1)
    print(f'The average temperature was {avgTemp}', file = outfile1)
    print(f'The rainfall yesterday was {("%.2f" % rain)} inches', file = outfile1)
    if hdd == 0:
        print('')
    else:
            print(f'There were {hdd} heating degree days', file = outfile1)
    if cdd == 0:
        print('')
    else:
        print(f'There were {cdd} cooling degree days', file = outfile1)
            
    print('\n', file = outfile1)
    print(f'Record information for {month} {nextDay}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The record high for today is {recHigh} in {recHighYear}', file = outfile1)
    print(f'The record low for today is {recLow} in {recLowYear}', file = outfile1)
    print(f'The record rainfall for today is {recRain} inches in {recRainYear}', file = outfile1)

