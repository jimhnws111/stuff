#!/usr/bin/env python
# coding: utf-8

# In[173]:


import json
import urllib
import requests
import csv


# In[174]:


import pandas as pd
import calendar

#
# Read JSON request into a pandas Dataframe
#

colNames = ['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall']
df = pd.read_json('/var/www/html/000/daily.txt')
#df = pd.read_json('/Users/jameshayes/daily.txt')
df = df.drop(df.columns[[0, 10]], axis=1)

#
# Get month name from month number and make some conversions 
#

date = int(df['Date'])
month_num  = int(df['Month'])
month_name = calendar.month_name[month_num]
year = int(df['Year'])

high = int(df['High'])
low = int(df['Low'])
avg = int(df['Average'])
hdd = int(df['HDD'])
cdd = int(df['CDD'])
rain = float(df['Rainfall'])


# In[179]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate
import sqlGet
import getDays
import logging

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
# Calculate phrasing for the web page
#

avgRainfall = result7[0]
avgRain = avgRainfall[3]
lowestRainfall = "0.00 in 1988"


# In[180]:


#
# Write out the web page 
#


#with open('/Users/jameshayes/dailyTest.html', 'w') as f:
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
            <td>Max Temperature</td><td>{high}</td><td>{avgHigh}</td><td>{recHigh} in {recHighYear}</td><td>{minHigh} in {recminHighYear}</td>
        </tr>
        <tr>
            <td>Min Temperature</td><td>{low}</td><td>{avgLow}</td><td>{maxLow} in {recmaxLowYear}</td><td>{recLow} in {recLowYear}</td>
        </tr>
        <tr>
            <td>Avg Temperature</td><td>{avg}</td><td>{avgTemp}</td><td></td><td></td>
        </tr>
        <tr>
            <td>HDD</td><td>{hdd}</td><td>{nmlHDD}</td><td></td><td></td>
        </tr>
        <tr>
            <td>CDD</td><td>{cdd}</td><td>{nmlCDD}</td><td></td><td></td>
        </tr>
        <tr>
            <td>Rainfall</td><td>{rain:.2f}</td><td>{avgRain:.2f}</td><td>{recRain} in {recRainYear}</td><td>{lowestRainfall}</td>
        </tr>       
            
        
    </table>   
    </div>
   
    </body>
    </html>'''
    f.write(message)


# In[ ]:





# In[ ]:




