#!/usr/bin/env python
# coding: utf-8

# In[2]:


import calcOneDay
import getDays
from datetime import datetime, timedelta
import calcTimeNow
import daysAndDates
import logging
import os

#
# Set up some logging
#

'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('/home/ec2-user/davisComplete99.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
'''

# Calculate the time and date for end of day calculations

xy = calcOneDay.calcOneDay()
start, end = (xy[0], xy[1])
dayInfo = daysAndDates.daysAndDates()

month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])
print(month, month_num, date, year)


# In[7]:


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
    print("Parameter name: \"{}\" has value \"{}\"".format(key, parameters[key]))

apiSecret = parameters["api-secret"];
parameters.pop("api-secret", None);

data = ""
for key in parameters:
    data = data + key + str(parameters[key])

#logger.info('Data string to hash is: \"{}\"'.format(data))   

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


# In[13]:


import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import sqlalchemy
from dateutil.tz import tzutc, tzlocal
import pytz
import os

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

#
# use environmental variables for the SQL query
#

db_user = os.environ.get('dbUser')
db_password = os.environ.get('dbPass')

database_username = db_user
database_password = db_password
database_ip       = '3.135.162.69'
database_name     = 'davisInfo'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args={'connect_timeout': 30})
df.to_sql(con=database_connection, name='davisTestB', if_exists='append')


# In[22]:


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


import sqlalchemy
import mysql.connector
import sqlite3
import os

df2 = pd.DataFrame(columns = ['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
newRow = pd.DataFrame({'Year': year, 'Month': month_num, 'Date': yesterday, 'High': maxT, 'Low': minT, 'Average': avgTemp, 'HDD': hdd, 'CDD': cdd, 'Rainfall' : rain, 'Max_Dew_Point': dewMaxT }, index = [yesterday])
df2 = pd.concat([newRow, df2]).reset_index(drop = True)

#
# use environmental variables for the SQL query
#

db_user = os.environ.get('dbUser')
db_password = os.environ.get('dbPass')

database_username = db_user
database_password = db_password
database_ip       = '3.135.162.69'
database_name     = 'davisf6'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args={'connect_timeout': 30})
df2.to_sql(con=database_connection, name='davisUpdate', if_exists='append', index = False)


# In[17]:


#
# Get the data from the mySQL table for yesterday
#

import pandas as pd
import pymysql as dbapi
from pretty_html_table import build_table
import os

#
# use environmental variables for the SQL query
#

db_user = os.environ.get('dbUser')
db_password = os.environ.get('dbPass')

QUERY2 = """SELECT * FROM davisUpdate 
         WHERE Month = %s""" % (month_num)


html_path = '/var/www/html/000/'
db = dbapi.connect(host='3.135.162.69', user=db_user, passwd=db_password, database = 'davisf6', port = 3306)

cur = db.cursor()
cur.execute(QUERY2)
dateResult = cur.fetchall()

colNames = (['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point']) 
pd.options.display.float_format = '{:,.2f}'.format
df3 = pd.DataFrame(dateResult, columns = colNames) 
df3 = df3.drop(df3.columns[[0, 1]], axis = 1)
df3 = df3.reindex(columns=['Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
df3.to_html(f'{html_path}throttled.html', index = False)     

html_table_blue_light = build_table(df3, 'blue_light', text_align='center', font_size='32px')

with open(f'{html_path}davisLocal.html', 'w') as f:
          f.write(html_table_blue_light)   


# In[1]:


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


# In[1]:


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

nmlData = sandbox2.sandbox2()
nmlHi = nmlData[3]
nmlLo = nmlData[4]

highData = sandbox1.recordHigh()
lowData = sandbox1.recordLow()
rainData = sandbox1.recordRain()

highPhrase = highData[2]
lowPhrase = lowData[2]
rainPhrase = rainData[2]

with open('/var/www/html/000/climoDavisText.txt','w') as outfile1: 
    print(f'Daily almanac for {month} {yesterday}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The high yesterday was {maxT} degrees', file = outfile1)
    print(f'The low yesterday was {minT} degrees', file = outfile1)
    print(f'The average temperature was {avgTemp} degrees', file = outfile1)
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
    
    print(f'Normal and Record information for {month} {date}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The normal high for today is {nmlHi} degrees', file = outfile1)
    print(f'The normal low for today is {nmlLo} degrees' , file = outfile1)
    print('\n', file = outfile1)
    print(highPhrase, file = outfile1)
    print(lowPhrase, file = outfile1)
    print(rainPhrase, file = outfile1)  


# In[ ]:




