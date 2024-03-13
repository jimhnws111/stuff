#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import calcOneDay
import sqlGet
import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json
import dataFile

def davisGet():
    
    xy = calcOneDay.calcOneDay()
    start, end = (xy[0], xy[1])
    print(start,end)

    gD = sqlGet.sqlGet()
    nextDay, date, month, month_num, year = gD[3], gD[4], gD[5], gD[6], gD[7]
        
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
    return(davisAPI)


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
from dateutil.tz import tzutc, tzlocal
import pytz

def davisFrame():
    
    davisAPI = davisGet()
    path2 = '/var/www/html/000/'

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
    print(df)
    
    t = df['temp_hi']
    y = t.to_numpy()
    date = df['localTime']
    x = date.to_numpy()
    print(x)

    '''
    plt.figure(figsize= (10,6))
    plt.yticks(fontsize = 12)
    plt.ylabel('Temperature (F)', fontsize=12, fontweight ='bold')
    
    plt.xticks(fontsize = 8, rotation = 45, fontweight = 'bold')     
    plt.locator_params(axis = 'x', tight = True, nbins = 24)
    plt.ylabel('Temperature (F)', fontsize=12, fontweight ='bold')
    plt.title('Hourly Temperatures - last 24 hours', fontsize = 12, fontweight = 'bold')
    plt.plot(x, y, marker = "*", color = "red", linewidth = 4, label = "Temperature")
    plt.grid(True)
    plt.autoscale(enable = True, axis = 'both', tight = True)

    plt.savefig(f'{path2}testDavisImg')
    '''


# In[ ]:


davisGet()
davisFrame()

