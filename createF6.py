#!/usr/bin/env python
# coding: utf-8

# In[94]:


import pandas as pd
import math

def createF6(df):
    
    """Create FG data from the newly created and passed dataframe"""
    
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

