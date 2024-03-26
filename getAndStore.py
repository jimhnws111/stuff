#!/usr/bin/env python
# coding: utf-8

# In[56]:


import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import sqlalchemy
from dateutil.tz import tzutc, tzlocal
import pytz
import os
import dataFromDavis
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import math

#
# Create some F6 data from the API data and write to a Pandas dataFrame 
#

def getAndStore():
    
    davisAPI = dataFromDavis.dataFromDavis()
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
    
    return(df)


#
# Calculate more variables from the dataFrame
#

import pandas as pd
from pandas import DataFrame, Series
import math

def createF6(df):
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
        
 
    return(maxT, minT, dewMaxT, dewMinT, rain, avgTemp, hdd, cdd)
    


# In[57]:


df = getAndStore()
createF6(df)


# In[ ]:




