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


# In[1]:


import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json
import pprint
import dataFile
import pandas as pd
import math
import sqlalchemy
import mysql.connector
import sqlite3

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

a = davisAPI['sensors']    
b = a[1]
c = (b['data'])
cLen = len(c)

df = pd.DataFrame(c) 
df = df.loc[:,['temp_hi', 'temp_hi_at','temp_lo', 'temp_lo_at', 'rainfall_in', 'dew_point_hi', 'dew_point_lo',  'rain_rate_hi_in', 'rain_rate_hi_at']]
print(df) 

database_username = 'chuckwx'
database_password = 'jfr716!!00'
database_ip       = '3.135.162.69'
database_name     = 'trweather'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args={'connect_timeout': 30})
df.to_sql(con=database_connection, name='davisData', if_exists='replace')

               
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
avgTemp = math.ceil(((maxT + minT)/2))

hdd = (65 - avgTemp)
if hdd < 0:
    hdd = 0
cdd = (avgTemp - 65)
if cdd < 0:
    cdd = 0  


# In[ ]:




