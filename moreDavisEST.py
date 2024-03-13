#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import datetime
from datetime import datetime
from dateutil.tz import tzutc, tzlocal
import pytz

#path_name = '/Users/jameshayes/'
path_name = '/home/ec2-user/'
file_name = 'testout.csv'
full_file = (path_name + file_name)

df = pd.read_csv(full_file, index_col=False,names=['temp_hi', 'temp_lo', 'rainfall','time'])

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

max_temp  = (df.sort_values(by='temp_hi', ascending=False))
max_T = max_temp.iloc[:1]
maxT = max_T['temp_hi'].values[0]
maxT = round(maxT)

min_temp  = (df.sort_values(by='temp_lo', ascending=True))
min_T = min_temp.iloc[:1]
minT = min_T['temp_lo'].values[0]
minT = round(minT)
minT = str(minT)
minT = minT.strip()

currentT = df['temp_hi'].iloc[-1]
currentT = round(currentT)
print(currentT)

totR = df['rainfall'].sum()
totR = float(round(totR,2))
latestRain = df.tail(60)
hourlyRate = latestRain['rainfall'].sum()

timezone = pytz.timezone("America/New_York")
recentT = (df['time'].iloc[-1])
datetime_obj = datetime.strptime(recentT, '%Y-%m-%d %H:%M:%S')
localT = datetime_obj.astimezone(timezone)
lastTime = localT.strftime('%I:%M %p')
print(localT, lastTime)

print(f'{maxT},{minT},{currentT},{("%.2f" % totR)},{("%.2f" % hourlyRate)}')


# In[ ]:




