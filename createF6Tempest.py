#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import math

def createF6Tempest():
    
    """Read in data from text file and create needed F6 data"""

    df = pd.read_csv('/home/ec2-user/tempest_temp.csv', index_col=False)
    #df = pd.read_csv('/Users/jameshayes/tempest_temp.csv', index_col=False)

    #
    # Calculate needed F6 data
    #

    max_temp  = (df.sort_values(by='temperature', ascending=False))
    max_T = max_temp.iloc[:1]
    maxT = max_T['temperature'].values[0]
    maxT = round((maxT*1.8) + 32)

    min_temp  = (df.sort_values(by='temperature', ascending=True))
    min_T = min_temp.iloc[:1]
    minT = min_T['temperature'].values[0]
    minT = round((minT*1.8) + 32)

    max_pres = (df.sort_values(by='pressure', ascending=False))
    max_P = max_pres.iloc[:1]
    maxP = max_P['pressure'].values[0]

    min_pres = (df.sort_values(by='pressure', ascending=True))
    min_P = min_pres.iloc[:1]
    minP = min_P['pressure'].values[0]

    cor_rain = (df.sort_values(by='local_daily_precip_final', ascending=False))
    corR_rain = cor_rain.iloc[:1]
    corR = corR_rain['local_daily_precip_final'].values[0]
    corR = round((corR*0.03937), 2)

    tot_rain = df['precip'].sum()
    totR = round((tot_rain*0.03937), 2)

    strike_distance = (df.sort_values(by='strike_distance', ascending=False))
    lightning1 = (df['strike_distance'].between(1,8))
    lightning2 = (df['strike_distance'].between(9,16))

    df.insert(10,'lightning1',lightning1)
    df.insert(11,'lightning2',lightning2)

    #
    # Determine if the strike distance is close enough to count as a thunderstorm
    #

    x = len(df)
    a = 0

    while a < x:
            if (df['lightning1'] == True).any():
                q = "Yes"
            else:
                q = "No"
            if (df['lightning2'] == True).any():   
                r1 = "Yes"
            else:
                r1 = "No"
            a += 1    

    avgTemp = math.ceil((int(maxT + minT)/2))

    hdd = (65 - avgTemp)
    if hdd < 0:
        hdd = 0
    cdd = (avgTemp - 65)
    if cdd < 0:
        cdd = 0     
        
    return (maxT, minT, maxP, minP, corR, totR, q, r1, avgTemp, hdd, cdd)

