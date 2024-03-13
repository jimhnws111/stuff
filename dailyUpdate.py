#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import urllib
import requests
import csv


# In[1]:


import pandas as pd
import calendar
from PIL import Image
from pretty_html_table import build_table
import sys
import shutil

#
# Read JSON request into a pandas Dataframe
#

colNames = ['index', 'Rain', 'HiTemp', 'LowTemp', 'Year', 'Month', 'Day']
df = pd.read_json('/var/www/html/000/daily.txt')

#
# Exit the program if the DataFrame is empty
#

'''
if df.empty:
    print("The dataset is empty")
    file1 = ('/var/www/html/000/NoData.html')
    file2 = ('/var/www/html/000/dailyTest.html')
    shutil.copyfile(file1, file2)
    
    sys.exit()   
    
#
# Calculating some needed variables for later
#
''' 
 
df = df.drop(df.columns[[0,7]], axis=1)

Date = (df['Day']).astype(int)
month_num  = (df['Month']).astype(int)
month_num = month_num[0]
month_name = calendar.month_name[month_num]
month_abbrev = month_name[0:3]
Year = (df['Year']).astype(int)
year = Year[0]
date = Date[0]


# In[ ]:


import math
import numpy as np

lastDay = calendar.monthrange(year,month_num)
lastDay1 = lastDay[1]

High = (df['HiTemp']).round(0).astype(int)
Low = (df['LowTemp']).round(0).astype(int)
Avg = ((High + Low)/2).astype(int).apply(np.ceil)
HDD = (65 - Avg).round(0).astype(int)
HDD = HDD.where(HDD > 0, 0) 
CDD = (Avg - 65).round(0).astype(int)
CDD = CDD.where(CDD > 0, 0) 
Rainfall = (df['Rain']).astype(float).fillna(0)
totRainfall = Rainfall.sum().round(2)

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
df.insert(11, 'Rainfall', Rainfall)
df.insert(12, 'Date', Date)

df = df.reindex(columns=['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD','Rainfall'])
df = df.drop(df.columns[[0,1,2]], index = None, axis=1)


# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate
import getDays
import logging

print("this is the date", date)

#
# Get the record high for the date
#

QUERY1 = """SELECT * FROM recHigh 
         WHERE Month = %s 
         AND Day = %s""" % (month_num, date)

db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY1)
result1 = cur.fetchall()
recordHigh = result1[0]
recHigh = int(recordHigh[1])
recHighYear = int(recordHigh[4])

QUERY2 = """SELECT * FROM recLow 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY2)
result2 = cur.fetchall()
recYearNum =  len(result2)
recordLow = result2[0]
recLow = int(recordLow[1])
recLowYear = int(recordLow[4])

QUERY3 = """SELECT * FROM minOfMax 
         WHERE Month = %s 
         AND Day = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY3)
result3 = cur.fetchall()
recYearNum =  len(result3)
minOfMax = result3[0]
minHigh = int(minOfMax[1])
recminHighYear = int(minOfMax[4])

QUERY4 = """SELECT * FROM maxOfMin 
         WHERE Month = %s 
         AND Day = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY4)
result4 = cur.fetchall()
recYearNum =  len(result4)
maxOfMin = result4[0]
maxLow = int(maxOfMin[1])
recmaxLowYear = int(maxOfMin[4])

#
# Get the record rainfall for the date
#
    
QUERY5 = """SELECT * FROM recRain 
         WHERE Month = %s 
         AND Day = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY5)
result5 = cur.fetchall()
recYearNum =  len(result5)
recordRain = result5[0]
recRain = float(recordRain[1])
recRainYear = int(recordRain[4])

#
# Get the average high for the date
#

QUERY6 = """SELECT * FROM dailyAvgTemps
         WHERE Month = %s 
         AND Date = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY6)
result6 = cur.fetchall()

avgData = result6[0]
avgHigh = avgData[3]
avgLow = avgData[4]
avgTemp = avgData[5]

nmlHDD = (65 - avgTemp)
if nmlHDD < 0:
    nmlHDD = 0
nmlCDD = (avgTemp - 65)
if nmlCDD < 0:
    nmlCDD = 0  

#
# Get the average rainfall for the date
#

QUERY7 = """SELECT * FROM dailyAvgRain
         WHERE Month = %s 
         AND Date = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY7)
result7 = cur.fetchall()

#
# Get the high average for the date
#

QUERY8 = """SELECT * FROM dailyHiAvg 
         WHERE Month = %s 
         AND Date = %s""" % (month_num, date)

db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY8)
result8 = cur.fetchall()
dailyHiAvg = result8[0]
recYearNum =  len(result8)
hiAvg = int(dailyHiAvg[3])
hiAvgYear = int(dailyHiAvg[4])
print(hiAvg, hiAvgYear)

#
# Get the low average for the date
#

QUERY9 = """SELECT * FROM dailyLoAvg
               WHERE Month = %s 
               AND Date = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY9)
result9 = cur.fetchall()
recYearNum =  len(result9)
dailyLoAvg = result9[0]
loAvg = int(dailyLoAvg[3])
loAvgYear = int(dailyLoAvg[4])

#
# Get the high HDD for the date
#

QUERY10 = """SELECT * FROM dailyHDDMax 
         WHERE Month = %s 
         AND Date = %s""" % (month_num, date)

db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY10)
result10 = cur.fetchall()
dailyHDDMax = result10[0]
recYearNum =  len(result10)
HDDMax = int(dailyHDDMax[4])
HDDMaxYear = int(dailyHDDMax[3])

#
# Get the low HDD for the date
#

QUERY11 = """SELECT * FROM dailyHDDMin
               WHERE Month = %s 
               AND Date = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY11)
result11 = cur.fetchall()
recYearNum =  len(result11)
dailyHDDMin = result11[0]
HDDMin = int(dailyHDDMin[4])
HDDMinYear = int(dailyHDDMin[3])

#
# Get the high CDD for the date
#

QUERY12 = """SELECT * FROM dailyCDDMax 
         WHERE Month = %s 
         AND Date = %s""" % (month_num, date)

db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY12)
result12 = cur.fetchall()
dailyCDDMax = result12[0]
recYearNum =  len(result12)
CDDMax = int(dailyCDDMax[4])
CDDMaxYear = int(dailyCDDMax[3])

#
# Get the low HDD for the date
#

QUERY13 = """SELECT * FROM dailyCDDMin
               WHERE Month = %s 
               AND Date = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'trweather')

cur = db.cursor()
cur.execute(QUERY13)
result13 = cur.fetchall()
recYearNum =  len(result13)
dailyCDDMin = result13[0]
CDDMin = int(dailyCDDMin[4])
CDDMinYear = int(dailyCDDMin[3])

#
# Calculate phrasing for the web page
#

avgRainfall = result7[0]
avgRain = avgRainfall[3]
lowestRainfall = "0.00 in 1988"


# In[3]:


#
# Write out the web page 
#

high = int(df['High'])
low = int(df['Low'])
avg = int(df['Average'])
hdd = int(df['HDD'])
cdd = int(df['CDD'])
rain = float(df['Rainfall'])

if year < 1989:
    rain = str(rain)
    rain = "M"
else:
    rain = float(df['Rainfall'])
    rain = format(rain, ".2f") 

with open('/var/www/html/000/dailyTest.html', 'w') as f:
    
    message = f'''
    <DOCTYPE html>
    <html>
    <link rel="stylesheet" type="text/css" href="dailyHTML.css" />
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Almanac for Toms River, NJ</title>
    
    </head>
    <body>
    <div class="dailyTable">
    
    <p> Daily Almanac for Toms River, NJ<br>
        {month_name} {date}, {year}<br>    
    </p><br>
    
    <table border="2">
        <tr>
            <th>Daily Data</th>
            <th>Observed</th>   
            <th>Normal</th>
            <th>Record Highest</th>
            <th>Record Lowest</th>  
        
        </tr>
        <tr>
            <td>Max Temp</td><td>{high}</td><td>{avgHigh}</td><td>{recHigh} in {recHighYear}</td><td>{minHigh} in {recminHighYear}</td>
        </tr>
        <tr>
            <td>Min Temp</td><td>{low}</td><td>{avgLow}</td><td>{maxLow} in {recmaxLowYear}</td><td>{recLow} in {recLowYear}</td>
        </tr>
        <tr>
            <td>Avg Temp</td><td>{avg}</td><td>{avgTemp}</td><td>{hiAvg} in {hiAvgYear}</td><td>{loAvg} in {loAvgYear}</td>
        </tr>
        <tr>
            <td>HDD</td><td>{hdd}</td><td>{nmlHDD}</td><td>{HDDMax} in {HDDMaxYear}</td><td>{HDDMin} in {HDDMinYear}</td>
        </tr>
        <tr>
            <td>CDD</td><td>{cdd}</td><td>{nmlCDD}</td><td>{CDDMax} in {CDDMaxYear}</td><td>{CDDMin} in {CDDMinYear}</td>
        </tr>
        <tr>
            <td>Rain</td><td>{rain}</td><td>{avgRain:.2f}</td><td>{recRain:.2f} in {recRainYear}</td><td>{lowestRainfall}</td>
        </tr>       
            
        
    </table>   
    </div>
   
    </body>
    </html>'''
   
    f.write(message)


# In[ ]:


with open('/var/www/html/000/dailyTest1.html', 'w') as f:
    
    message = f'''
    <DOCTYPE html>
    <html>
    <link rel="stylesheet" type="text/css" href="dailyHTML1.css" />
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Almanac for Toms River, NJ</title>
    
    </head>
    <body>
    <div class="dailyTable">
    
    <p> Daily Almanac for Toms River, NJ<br>
        {month_name} {date}, {year}<br>    
    </p><br>
    
    <table border="2">
        <tr>
            <th>Daily Data</th>
            <th>Observed</th>   
            <th>Normal</th>
            <th>Record Highest</th>
            <th>Record Lowest</th>  
        
        </tr>
        <tr>
            <td>Max Temperature</td><td>{high}</td><td>{avgHigh}</td><td>{recHigh} in {recHighYear}</td><td>{minHigh} in {recminHighYear}</td>
        </tr>
        <tr>
            <td>Min Temperature</td><td>{low}</td><td>{avgLow}</td><td>{maxLow} in {recmaxLowYear}</td><td>{recLow} in {recLowYear}</td>
        </tr>
        <tr>
            <td>Avg Temperature</td><td>{avg}</td><td>{avgTemp}</td><td>{hiAvg} in {hiAvgYear}</td><td>{loAvg} in {loAvgYear}</td>
        </tr>
        <tr>
            <td>HDD</td><td>{hdd}</td><td>{nmlHDD}</td><td>{HDDMax} in {HDDMaxYear}</td><td>{HDDMin} in {HDDMinYear}</td>
        </tr>
        <tr>
            <td>CDD</td><td>{cdd}</td><td>{nmlCDD}</td><td>{CDDMax} in {CDDMaxYear}</td><td>{CDDMin} in {CDDMinYear}</td>
        </tr>
        <tr>
            <td>Rainfall</td><td>{rain}</td><td>{avgRain:.2f}</td><td>{recRain:.2f} in {recRainYear}</td><td>{lowestRainfall}</td>
        </tr>       
            
        
    </table>   
    </div>
   
    </body>
    </html>'''
   
    f.write(message)

