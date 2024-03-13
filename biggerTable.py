#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import urllib
import requests
import csv
import pandas as pd
import numpy as np
import calendar
from PIL import Image
from pretty_html_table import build_table
import sys

#
# Read JSON request into a pandas Dataframe
#

colNames = ['index', 'Rain', 'HiTemp', 'LowTemp', 'Year', 'Month', 'Day']
df = pd.read_json('/var/www/html/000/monthly.txt')
df = df.drop(df.columns[[0]], axis=1)
df['Rain'] = ((df['Rain']).astype(float).fillna(0))

#
# Exit the program if the DataFrame is empty
#

if df.empty:
    print("The dataset is empty")
    Image2 = Image.open('/var/www/html/000/allInOne.png')
    Image2copy = Image2.copy()
    Image1 = Image.open('/var/www/html/000/NoData.png')
    Image1copy = Image1.copy()
    Image2copy.paste(Image1copy, (0, 0))
    Image1copy.save('/var/www/html/000/allInOne.png')     
    
    with open('/var/www/html/000/monthlyTable.html', 'w') as f:
    #with open('/Users/jameshayes/monthlyTable.html', 'w') as f:
        html_table_blue_light = build_table(df, 'blue_light', text_align='center')
        f.write(html_table_blue_light)    
        
    sys.exit()    

#
# Get month name from month number and make some conversions 
#

Date = (df['Day']).astype(int)
month_num  = (df['Month']).astype(int)
month_num = month_num[0]
month_name = calendar.month_name[month_num]
month_abbrev = month_name[0:3]
Year = (df['Year']).astype(int)
year = Year[0]

#
# Calculate the last day of each month
#

lastDay = calendar.monthrange(year,month_num)
lastDay1 = lastDay[1]

High = (df['HiTemp']).round(0).astype(int)
Low = (df['LowTemp']).round(0).astype(int)
Avg = ((High + Low)/2).round(0).astype(int)
HDD = (65 - Avg).round(0).astype(int)
HDD = HDD.where(HDD > 0, 0) 
CDD = (Avg - 65).round(0).astype(int)
CDD = CDD.where(CDD > 0, 0) 
rain = (df['Rain']).astype(float)
totRainfall = rain.sum().round(2)

if year < 1989:
    rain = str(rain)
    rain = "M"
    
month_High_avg = High.mean().round(1) 
month_Low_avg = Low.mean().round(1) 
month_avg = Avg.mean().round(1)
totHDD = HDD.sum()
totCDD = CDD.sum()

df.insert(6, 'Average', Avg)
df.insert(7, 'HDD', HDD)
df.insert(8, 'CDD', CDD)
df.insert(9, 'High', High)
df.insert(10, 'Low', Low)
df.insert(11, 'Rainfall', rain)
df.insert(12, 'Date', Date)

df = df.reindex(columns=['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD','Rainfall'])
df = df.drop(df.columns[[0,1]], index = None, axis=1)
print(len(df))

avgData = np.array([month_High_avg, month_Low_avg, month_avg, totHDD, totCDD, totRainfall])
df2 = pd.DataFrame(avgData)
df3 = df2.transpose()

df3[3] = df3[3].astype(int)
df3[4] = df3[4].astype(int)
print(df3)

df.to_html('/var/www/html/000/monthTest1.html', index = False)

