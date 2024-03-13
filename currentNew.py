#!/usr/bin/env python
# coding: utf-8

# In[138]:


import json
import urllib
import requests
import csv
import re
from datetime import datetime
from dateutil.tz import tzutc, tzlocal
import pytz

token = '877f6425-04a5-4f33-86e7-7123b7ef53d9'
getData = 'https://swd.weatherflow.com/swd/rest/observations/station/95775?token=877f6425-04a5-4f33-86e7-7123b7ef53d9'
r =  requests.get(getData)
y = (r.json())
obs_data = y['obs']
rsqd = obs_data[0]

temp = round((rsqd['air_temperature']) * 1.8 + 32)
dew_point = round((rsqd['dew_point']) * 1.8 + 32)
sea_press = round((rsqd['sea_level_pressure']) * 0.0295301, 2)
press_trend = rsqd['pressure_trend']
wind_spd = round((rsqd['wind_avg']) * 2.23694)
feels_like = round((rsqd['feels_like']) * 1.8 + 32)

if press_trend == "steady":
    press_trend = "S"

if press_trend == "rising":
    press_trend = "R"
    
if press_trend == "falling":
    press_trend = "F"    


wind_card = round(rsqd['wind_direction'])

if wind_card == 0:
    wind_dir = 'N'
if wind_card > 0 and wind_card < 23:
    wind_dir = 'N'
if wind_card > 22 and wind_card < 68: 
    wind_dir = 'NE'
if wind_card > 68 and wind_card < 113:
    wind_dir = 'E'
if wind_card > 112 and wind_card < 158:
    wind_dir = 'SE'  
if wind_card > 157 and wind_card < 203:
    wind_dir = 'S'
if wind_card > 203 and wind_card < 248: 
    wind_dir = 'SW'
if wind_card > 247 and wind_card < 293:
    wind_dir = 'W'
if wind_card > 292 and wind_card < 348:
    wind_dir = 'NW'   
if wind_card > 348 and wind_card < 360:
    wind_dir = 'N' 

wind = f'{wind_dir} {wind_spd}'    
if wind_spd < 1.5:
    wind = 'calm'

    
pcpn_1hr = round((rsqd['precip_accum_last_1hr'] * 0.03937), 2)
rh = rsqd['relative_humidity']
timestamp = rsqd['timestamp']

timezone = pytz.timezone("America/New_York")
dt_object = datetime.fromtimestamp(timestamp)
localT = dt_object.astimezone(timezone)
lastTime = localT.strftime('%I:%M %p')

heat_desc = f'(Feels like {feels_like} degrees)'
if feels_like < 100:
    heat_desc = ''  
    
cold_desc = f'(Feels like {feels_like} degrees)'
if feels_like > 32:
    cold_desc = ''


# In[137]:


temp = str(temp)

with open('/var/www/html/000/currentConditions.html', 'w') as f:
    
    message = f'''
    <DOCTYPE html>
    <html>
    <link rel="stylesheet" type="text/css" href="forecastP.css">
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
    <li>{temp} F</li>
    </div>
    
    <div class="rh">
    <li>{rh}%</li>
    </div>
    
    <div class="winds">
    <li>{wind}</li>
    </div>
    
    <div class="baro">
    <li>{("%.2f" % sea_press)}{press_trend}</li>
    </div>
    
  
    </body>
    </html>'''
    f.write(message)


# In[ ]:





# In[ ]:




