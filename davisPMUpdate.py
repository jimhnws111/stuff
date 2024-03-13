#!/usr/bin/env python
# coding: utf-8

# In[12]:


import calcOneDay
import getDays
from datetime import datetime, timedelta
import calcTimeNow
import daysAndDates
import logging
import checkDST

'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('/home/ec2-user/davisPMUpdate.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
'''

# Calculate the time and date for end of day calculations
#
# First determine whether we are in DST or not
#

# Check DST setting
isDST = checkDST.checkDST()

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

dayInfo = daysAndDates.daysAndDates()
month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])
month_num = int(month_num)
date = int(date)


# In[2]:


import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json
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
    logging.debug("Parameter name: \"{}\" has value \"{}\"".format(key, parameters[key]))

apiSecret = parameters["api-secret"];
parameters.pop("api-secret", None);

data = ""
for key in parameters:
    data = data + key + str(parameters[key])

logging.debug("Data string to hash is: \"{}\"".format(data))
logging.debug('\n')

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
logging.debug("API Signature is: \"{}\"".format(apiSignature))
logging.debug('\n')

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


# In[3]:


import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
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


# In[4]:


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


# In[5]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate
import os

#
# Get normal highs and lows
#

#
# use environmental variables for the SQL query
#

db_user = os.environ.get('dbUser')
db_password = os.environ.get('dbPass')

QUERY = """SELECT * FROM avgHiLo 
           WHERE Month = %s 
           AND Day = %s""" % (month_num, date)

print(QUERY)


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


# In[7]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate
import sandbox1
import sandbox2

'''
climo_data = [["Month", "Day", "Year", "High", "Low", "Avg", "HDD", "CDD", "Rain"],
             [month, date, year, maxT, minT, avgTemp, hdd, cdd, corR]]

with open('/var/www/html/000/climo.html', 'w') as f:
    f.write(tabulate(climo_data, headers = 'firstrow', tablefmt = 'html'))
    

record_data = [["Month", "Day", "Year", "Record High", "Year", "Record Low", "Year", "Record Rainfall", "Year"],
             [month, nextDay, year, recHigh, recHighYear, recLow, recLowYear, recRain, recRainYear]]
            


with open('/var/www/html/000/day_records.html', 'w') as f:
    f.write(tabulate(record_data, headers = 'firstrow', tablefmt = 'html'))'

with open('/var/www/html/000/climoTest1.html','w') as outfile1: 
    print(f'This is the daily almanac for {month} {date}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The high today was {maxT} at {hiTime}', file = outfile1)
    print(f'The low today was {minT} at {loTime}', file = outfile1)
    print(f'The average temperature was {avgTemp}', file = outfile1)
    print(f'The rainfall today was {corR} inches', file = outfile1)
    print(f'There were {hdd} heating degree days today', file = outfile1)
    print(f'There were {cdd} cooling degree days today', file = outfile1)
'''

nmlData = sandbox2.sandbox2()
logging.debug(f'This is the value of nmlData: {nmlData}')
nmlHi = nmlData[3]
nmlLo = nmlData[4]

highData = sandbox1.recordHigh()
logging.debug("THIS IS THE HIGH DATA: ", highData)
lowData = sandbox1.recordLow()
logging.debug("THIS IS THE LOW DATA: ", lowData)
rainData = sandbox1.recordRain()
logging.debug("THIS IS THE RAIN DATA: ", rainData)

highPhrase = highData[2]
lowPhrase = lowData[2]
rainPhrase = rainData[2]

if date == 1:
    date = 1

print(date)

with open('/var/www/html/000/climoDavisText.txt','w') as outfile1: 
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
    
    print(f'Normal and Record information for {month} {date}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The normal high for today is {nmlHi} degrees', file = outfile1)
    print(f'The normal low for today is {nmlLo} degrees' , file = outfile1)
    print('\n', file = outfile1)
    print(highPhrase, file = outfile1)
    print(lowPhrase, file = outfile1)
    print(rainPhrase, file = outfile1)  


# In[ ]:





# In[ ]:




