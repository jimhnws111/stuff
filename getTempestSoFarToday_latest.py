#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import urllib
import requests
import csv
import re
import calcTimeStamp
import UTC2local

# Calculate the time and date for calucaltions so far

xy = UTC2local.UTC2local()
start, end = (xy[0], xy[1])
start = str(start)
end = str(end)


# In[ ]:


import datetime
from datetime import datetime
import dataFile

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
print(goGetDeviceSummary)
r =  requests.get(goGetDeviceSummary)
full_file = '/home/ec2-user/latestTempest1m.csv'

with open(full_file,'w') as fd:
     fd.write(r.text)


# In[ ]:


import pandas as pd
import dataFile
import datetime
from datetime import datetime
from dateutil.tz import tzutc, tzlocal
import pytz

#
# Read in the CSV file for processing in pandas
#

full_file = '/home/ec2-user/latestTempest1m.csv'

df = pd.read_csv(full_file, index_col=False)

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

max_temp  = (df.sort_values(by='temperature', ascending=False))
max_T = max_temp.iloc[:1]
maxT = max_T['temperature'].values[0]
maxT = round((maxT*1.8) + 32)

min_temp  = (df.sort_values(by='temperature', ascending=True))
min_T = min_temp.iloc[:1]
minT = min_T['temperature'].values[0]
minT = round((minT*1.8) + 32)

tot_rain = df['precip'].sum()
totR = round((tot_rain*0.03937), 2)
nc_Rain = df['local_daily_precip_final'].iloc[-1]
ncR = round((nc_Rain*0.03937), 2)
latestRain = df.tail(60)
hourlyRate = latestRain['precip'].sum()
hourlyRate = round((hourlyRate*0.03937), 2)
print(hourlyRate)

storm = (df['strike_distance'].iloc[-1])
if storm > 0 and storm < 8:
    status = "Yes"
else:
    status = "No"

timezone = pytz.timezone("America/New_York")
recentT = (df['timestamp'].iloc[-1])
dt_object = datetime.fromtimestamp(recentT)
localT = dt_object.astimezone(timezone)
lastTime = localT.strftime('%I:%M %p')
    

# write the data to a csv file with an html suffix

with open('/home/ec2-user/HiLoRain_tempest.csv', 'w') as outfile:
    print(f'{maxT},{minT},{("%.2f" % totR)},{("%.2f" % hourlyRate)},{("%.2f" % ncR)},{status},{lastTime}',file = outfile)

