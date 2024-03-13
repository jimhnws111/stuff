#!/usr/bin/env python
# coding: utf-8

# In[95]:


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

wind_card = round(rsqd['wind_direction'])
if wind_card == 0:
    wind_dir = 'north'
if wind_card > 0 and wind_card < 23:
    wind_dir = 'north'
if wind_card > 22 and wind_card < 68: 
    wind_dir = 'northeast'
if wind_card > 68 and wind_card < 113:
    wind_dir = 'east'
if wind_card > 112 and wind_card < 158:
    wind_dir = 'southeast'  
if wind_card > 157 and wind_card < 203:
    wind_dir = 'south'
if wind_card > 203 and wind_card < 248: 
    wind_dir = 'southwest'
if wind_card > 247 and wind_card < 293:
    wind_dir = 'west'
if wind_card > 292 and wind_card < 348:
    wind_dir = 'northwest'   
if wind_card > 348 and wind_card < 361:
    wind_dir = 'north' 

wind = f'{wind_dir} at {wind_spd} miles per hour'    
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

with open('/var/www/html/000/text975.txt','w') as fd:
    print(f'In Toms River, NJ at {lastTime}','\n', file = fd)
    print(f'The temperature was {temp} degrees {heat_desc}', file = fd)
    print(f'The relative humidity was {rh}%', file = fd)
    print(f'The wind was {wind}', file = fd)
    print(f'The barometric pressure was {sea_press:.2f} inches and {press_trend}', file = fd)   


# In[ ]:




