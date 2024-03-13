#!/usr/bin/env python
# coding: utf-8

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
    
latestRain = df.tail(60)
hourlyRate = latestRain['precip'].sum()
print("%.2f" % hourlyRate)

