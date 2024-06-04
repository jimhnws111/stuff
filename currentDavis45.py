#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime
import time
from datetime import datetime, timedelta
import collections
import hashlib
import hmac
import requests
import json
from dateutil.tz import tzutc, tzlocal
import pytz
import os
#import sqlalchemy
#import mysql.connector
#import sqlite3
import os


# In[ ]:


parameters = {
  "api-key": "vy8jbrjsxlbwgojepq3vfyfqfywyhvbd", 
  "api-secret": "sdqfm6wdfy9w0pqp2vdka38o6b4vcsvc",
  "station-id": 81211, 
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

first_part = ('https://api.weatherlink.com/v2/current/81211?')
api_key = ('api-key=vy8jbrjsxlbwgojepq3vfyfqfywyhvbd')
add_apisig = ('&api-signature=')
add_t = ('&t='+ str(int(time.time())))
print(add_t)

URLfinal = (first_part + api_key + add_t + add_apisig + apiSignature)
print(URLfinal)

r =  requests.get(URLfinal)

#data_dir_file = '/Users/jameshayes/davis1.json' 
data_dir_file = '/var/www/html/000/davis1.json' 
with open(data_dir_file, "w") as fd:   
    json.dump(r.json(), fd)


# In[ ]:


import pandas as pd

#ata_dir_file = '/Users/jameshayes/davis1.json' 
data_dir_file = '/var/www/html/000/davis1.json' 
with open(data_dir_file, "r") as fr:
    davisAPI = json.load(fr) 

#
# Converting dictionaries to lists and vice versa
#

a = davisAPI['sensors']   
b = a[1]
pres = a[3]
pres_data = (pres['data'])
med_baro = pres_data[0]
final_baro = (med_baro['bar_sea_level'])
final_baro = ("%.2f" % final_baro)
baro_trend = (med_baro['bar_trend'])
c = (b['data'])
d = c[0]


#with open('/Users/jameshayes/davisTable.csv', 'w') as outfile: 
with open('/home/ec2-user/davisTable.csv', 'w') as outfile: 

    temp = (d['temp'])
    temp = round(temp)
    dew_point = (d['dew_point'])
    rainfall = (d['rainfall_daily_in'])
    hum = (d['hum'])
    hum = round(hum)
    wind_direct = (d['wind_dir_scalar_avg_last_1_min'])
    wind_speed = (d['wind_speed_last'])
    rain_rate = (d['rain_rate_hi_in'])
    htindx = int(d['thw_index'])
    time = (d['ts'])
    date_time = datetime.fromtimestamp(time)
    print(f'{temp},{hum},{wind_direct},{wind_speed},{rainfall},{rain_rate},{htindx},{final_baro},{baro_trend},{time}', 
          file = outfile)      
    
df = pd.DataFrame(c) 

timezone = pytz.timezone("America/New_York")
recentT = (df['ts'].iloc[-1])
dt_object = datetime.fromtimestamp(recentT)
localT = dt_object.astimezone(timezone)
lastTime = localT.strftime('%I:%M %p')  
time24 = localT.strftime('%-H')  
time24 = int(time24)
localSet = localT.strftime(('%Y-%m-%d %H:%M'))
    
with open('/home/ec2-user/davisTableTest.csv', 'a') as outfile1: 

    temp = (d['temp'])
    temp = round(temp)
    dew_point = (d['dew_point'])
    dew_point = round(dew_point)
    rainfall = (d['rainfall_daily_in'])
    hum = (d['hum'])
    hum = round(hum)
    wind_direct = (d['wind_dir_scalar_avg_last_1_min'])
    wind_speed = (d['wind_speed_last'])
    rain_rate = (d['rain_rate_hi_in'])
    htindx = int(d['thw_index'])
    time = (d['ts'])
    date_time = datetime.fromtimestamp(time)
    print(f'{temp},{dew_point},{hum},{wind_direct},{wind_speed},{rainfall},{rain_rate},{htindx},{final_baro},{baro_trend},{localSet}', 
          file = outfile1)      


# In[ ]:


wind_direct = int(wind_direct)
wind_speed = int(wind_speed)

if wind_direct == 0:
    wind_dir = 'N'
if wind_direct > 0 and wind_direct < 23:
    wind_dir = 'N'
if wind_direct > 22 and wind_direct < 68: 
    wind_dir = 'NE'
if wind_direct > 68 and wind_direct < 113:
    wind_dir = 'E'
if wind_direct > 112 and wind_direct < 158:
    wind_dir = 'SE'  
if wind_direct > 157 and wind_direct < 203:
    wind_dir = 'S'
if wind_direct > 203 and wind_direct < 248: 
    wind_dir = 'SW'
if wind_direct > 247 and wind_direct < 293:
    wind_dir = 'W'
if wind_direct > 292 and wind_direct < 348:
    wind_dir = 'NW'   
if wind_direct > 348 and wind_direct <= 360:
    wind_dir = 'N' 

wind = f'{wind_dir} {wind_speed}'    
if wind_speed < 1.5:
    wind = 'Calm'   


# In[ ]:


from datetime import datetime
from dateutil.tz import tzutc, tzlocal
import pytz

#
# Stringify some numbers
#

temp = str(temp)
hum = str(hum)
rainfall = float(rainfall)
final_baro = float(final_baro)
rain_rate = float(rain_rate)

baro_trend = float(baro_trend)
dp = int(dew_point)

#
# Codify the barometric pressure trend
#

if baro_trend > 0.02:
    print(baro_trend)
    baro_letter = "R"
    print(baro_letter)

elif baro_trend < -0.02:
    print(baro_trend)
    baro_letter = "F"
    print(baro_letter)
    
else:
    print(baro_trend)
    baro_letter = "S"
    print(baro_letter)        

#
# Time info
#

timezone = pytz.timezone("America/New_York")
dt_object = datetime.fromtimestamp(time)
localT = dt_object.astimezone(timezone)
lastTime = localT.strftime('%I:%M %p')

import pandas as pd
import csv

colNames = ['Hi', 'Lo','Rain', 'hRain', 'text1', 'text2', 'eTime']
df = pd.read_csv('/home/ec2-user/HiLoRain.csv', names = colNames)

hiTemp = df['Hi'].astype(int)
loTemp = df['Lo'].astype(int)
hiTemp =int(hiTemp)
loTemp =int(loTemp)

if rain_rate == 0.0:
    
    rain_rate = ""
    with open('/var/www/html/000/currentDavisV45.html', 'w') as f:
    #with open('/Users/jameshayes/currentDavis.html', 'w') as f:

        message = f'''
        <DOCTYPE html>
        <html>
        <link rel="stylesheet" media="screen and (min-width: 900px)" href="forecastP.css" />
        <link rel="stylesheet" media="screen and (max-width: 600px) " href="forecastSmaller.css" />
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="60";>
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Latest Conditions</title>

        </head>
        <body>

        <div class="timed"
        <li> In Toms River, NJ at {lastTime}</li><br><br>
        </div>

        <div class="temps">
        <li>{temp}&deg;</li>
        </div>

        <div class="hiTemp">
        <li>{hiTemp}&deg;</li>
        </div>

        <div class="loTemp">
        <li>{loTemp}&deg;</li>
        </div>

        <div class="rh">
        <li>{hum}%</li>
        </div>

        <div class="dp">
        <li>{dp}&deg;</li>
        </div>       
               
        <div class="winds">
        <li>{wind}</li>
        </div>

        <div class="baro">
        <li>{("%.2f" % final_baro)}{baro_letter}</li>
        </div>

        <div class="hrain">
        <li>{rain_rate}</li>
        </div>

        <div class="totR">
        <li>{("%.2f" % rainfall)}"</li>
        </div>

        </body>
        </html>'''
        f.write(message)

else:
        with open('/var/www/html/000/currentDavisV45.html', 'w') as f:
        #with open('/Users/jameshayes/currentDavis.html', 'w') as f:

            message = f'''
            <DOCTYPE html>
            <html>
            <link rel="stylesheet" media="screen and (min-width: 900px)" href="forecastP.css" />
            <link rel="stylesheet" media="screen and (max-width: 600px) " href="forecastSmaller.css" />
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="refresh" content="60";>
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Latest Conditions</title>

            </head>
            <body>

            <div class="timed"
            <li> In Toms River, NJ at {lastTime}</li><br><br>
            </div>

            <div class="temps">
            <li>{temp}&deg;</li>
            </div>

            <div class="hiTemp">
            <li>{hiTemp}&deg;</li>
            </div>

            <div class="loTemp">
            <li>{loTemp}&deg;</li>
            </div>

            <div class="rh">
            <li>{hum}%</li>
            </div>

            <div class="dp">
            <li>{dp}&deg;</li>
            </div>
            
            <div class="winds">
            <li>{wind}</li>
            </div>

            <div class="baro">
            <li>{("%.2f" % final_baro)}{baro_letter}</li>
            </div>

            <div class="hrain">
            <li>{rain_rate}"</li>
            </div>

            <div class="totR">
            <li>{("%.2f" % rainfall)}"</li>
            </div>

            </body>
            </html>'''
            f.write(message)


# In[4]:


import pandas as pd
import csv
import sqlalchemy
import mysql.connector
import sqlite3
import os

colNames1 = ['temp', 'dew_point','hum', 'wind_dir', 'wind_speed', 'rainfall','rain_rate', 'htindx', 'final_baro', 'baro_trend', 'dtg']
df1 = pd.read_csv('/home/ec2-user/davisTableTest.csv', names = colNames1)

time = (d['ts'])
timezone = pytz.timezone("America/New_York")
dt_object = datetime.fromtimestamp(time)
localT = dt_object.astimezone(timezone)
lastTime = localT.strftime('%I:%M %p')

df2 = pd.DataFrame(columns = ['timeStamp','temp', 'dew_point','hum', 'wind_dir', 'wind_speed', 'rainfall','rain_rate', 'htindx', 'final_baro', 'baro_trend', 'lastTime'])
newRow = pd.DataFrame({'timeStamp': time, 'temp': temp, 'dew_point': dew_point, 'hum': hum, 'wind_dir': wind_dir, 'wind_speed': wind_speed, 'rainfall': rainfall, 'rain_rate': rain_rate, 'htindx': htindx, 'final_baro': final_baro, 'baro_trend': baro_trend, 'lastTime': lastTime}, index = [0])
df2 = pd.concat([newRow, df2[:]]).reset_index(drop = True)
print("This is the most recent rain_rate", rain_rate)


#
# use environmental variables for the SQL query
#

db_user = os.environ.get('dbUser')
db_password = os.environ.get('dbPass')

database_username = db_user
database_password = db_password
database_ip       = '3.135.162.69'
database_name     = 'trweather'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
df2.to_sql(con=database_connection, name='davisMinute', if_exists='append', index = False) 


# In[ ]:




