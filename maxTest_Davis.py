#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
import pprint
import dataFile

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
print(URLfinal)

r =  requests.get(URLfinal)
path_name = '/home/ec2-user/'
dump_file = 'davisDataDumpTest.csv'
data_file = f'{path_name}{dump_file}'

with open(data_file, "w") as fd:   
     json.dump(r.json(), fd)


# In[ ]:


import time
from datetime import datetime
import requests
import json
import dataFile

with open(data_file) as fr:
    davisAPI = json.load(fr) 
    
a = davisAPI['sensors']    
b = a[1]
c = (b['data'])

cLen = len(c)

with open(data_file, 'w') as outfile: 
    i = 0
    while i < cLen:
        d = c[i]
        hi_temp = (d['temp_hi'])
        lo_temp = (d['temp_lo'])
        rainfall = (d['rainfall_in'])
        dew_hi = (d['dew_point_hi'])
        dew_lo = (d['dew_point_lo'])
        temp_hi_at = (d['temp_hi_at'])
        temp_lo_at = (d['temp_lo_at'])
        print(f'{hi_temp},{temp_hi_at},{lo_temp}, {temp_lo_at},{rainfall},{dew_hi},{dew_lo}',file = outfile)
        i += 1
        


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

df = pd.read_csv(data_file, index_col=False,names=['temp_hi', 'temp_hi_at', 'temp_lo', 'temp_lo_at', 'rainfall', 'dew_hi', 'dew_lo'])

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

maxT1 = df['temp_hi'].max()
maxT1 = round((maxT1 * 1.8) + 32)
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
print(maxT, max_T_time)
print(minT, min_T_time)

dew_max = (df.sort_values(by='dew_hi', ascending=False))
dew_max1 = dew_max.iloc[:1]
dewMax = dew_max1['dew_hi'].values[0]
dewMaxT = round(dewMax)

dew_min = (df.sort_values(by='dew_lo', ascending=True))
dew_min1 = dew_min.iloc[:1]
dewMin = dew_min1['dew_lo'].values[0]
dewMinT = round(dewMin)

rain = df['rainfall'].sum()

timezone = pytz.timezone("America/New_York")
dt_object = datetime.fromtimestamp(max_T_time)
localT = dt_object.astimezone(timezone)
hiTime = localT.strftime('%I:%M %p')  

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


# In[ ]:


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

climo_data = [["Month", "Day", "Year", "High", "Low", "Avg", "HDD", "CDD", "Rain"],
             [month, date, year, maxT, minT, avgTemp, hdd, cdd, rain]]

#with open('/var/www/html/000/climoDavis.html', 'w') as f:
#    f.write(tabulate(climo_data, headers = 'firstrow', tablefmt = 'html'))
    

record_data = [["Month", "Day", "Year", "Record High", "Year", "Record Low", "Year", "Record Rainfall", "Year"],
             [month, nextDay, year, recHigh, recHighYear, recLow, recLowYear, recRain, recRainYear]]

#with open('/var/www/html/000/day_records_Davis.html', 'w') as f:
#    f.write(tabulate(record_data, headers = 'firstrow', tablefmt = 'html'))
  
   
#with open('/var/www/html/000/climo1.html','w') as outfile1: 
#    print(f'This is the daily almanac for {month} {date}, {year}', file = outfile1)
#    print('\n', file = outfile1)
#    print(f'The high today was {maxT} at {hiTime}', file = outfile1)
#    print(f'The low today was {minT} at {loTime}', file = outfile1)
#   print(f'The average temperature was {avgTemp}', file = outfile1)
#    print(f'The rainfall today was {corR} inches', file = outfile1)
#    print(f'There were {hdd} heating degree days today', file = outfile1)
#    print(f'There were {cdd} cooling degree days today', file = outfile1)

with open('/var/www/html/000/climoRecordsDavis.txt','w') as outfile1: 
    print(f'Daily almanac for {month} {date}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The high today was {maxT} at {hiTime}', file = outfile1)
    print(f'The low today was {minT} at {loTime}', file = outfile1)
    print(f'The average temperature was {avgTemp}', file = outfile1)
    print(f'The rainfall today was {rain} inches', file = outfile1)
    print(f'There were {hdd} heating degree days today', file = outfile1)
    print(f'There were {cdd} cooling degree days today', file = outfile1)
    print('\n', file = outfile1)
    print(f'Record information for {month} {nextDay}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The record high for today is {recHigh} in {recHighYear}', file = outfile1)
    print(f'The record low for today is {recLow} in {recLowYear}', file = outfile1)
    print(f'The record rainfall for today is {recRain} inches in {recRainYear}', file = outfile1)

