#!/usr/bin/env python
# coding: utf-8

# In[35]:


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
from datetime import date
import calcOneDay
import daysAndDates
import calendar

# Calculate the time and date for end of day calculations

xy = calcOneDay.calcOneDay()
start, end = (xy[0], xy[1])
dayInfo = daysAndDates.daysAndDates()

month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
month_num = int(month_num)
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])
#print(month, month_num, date, year)
month_name = calendar.month_name[month_num]
month_abbrev = month_name[0:3]

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
print(result7)

#
# Calculate phrasing for the web page
#

avgRainfall = result7[0]
print(avgRainfall)
avgRain = avgRainfall[3]
lowestRainfall = "0.00 in 1988"


# In[36]:


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
cur.execute(QUERY8)
result10 = cur.fetchall()
dailyHDDMax = result10[0]
recYearNum =  len(result10)
HDDMax = int(dailyHDDMax[3])
HDDMaxYear = int(dailyHDDMax[4])

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
HDDMin = int(dailyHDDMin[3])
HDDMinYear = int(dailyHDDMin[4])


# In[37]:


with open('/Users/jameshayes/testDays.html', 'w') as f:
    
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
            <th>Normal</th>
            <th>Record Highest</th>
            <th>Record Lowest</th>  
        
        </tr>
        <tr>
            <td>Max Temperature</td><td>{avgHigh}</td><td>{recHigh} in {recHighYear}</td><td>{minHigh} in {recminHighYear}</td>
        </tr>
        <tr>
            <td>Min Temperature</td><td>{avgLow}</td><td>{maxLow} in {recmaxLowYear}</td><td>{recLow} in {recLowYear}</td>
        </tr>
        <tr>
            <td>Avg Temperature</td><td>{avgTemp}</td><td>{hiAvg} in {hiAvgYear}</td><td>{loAvg} in {loAvgYear}</td>
        </tr>
        <tr>
            <td>HDD</td><td>{nmlHDD}</td><td>{HDDMax} in {HDDMaxYear}</td><td>{HDDMin} in {HDDMinYear}</td>
        </tr>
        <tr>
            <td>CDD</td><td>{nmlCDD}</td><td></td><td></td>
        </tr>
        <tr>
            <td>Rainfall</td><td>{avgRain:.2f}</td><td>{recRain:.2f} in {recRainYear}</td><td>{lowestRainfall}</td>
        </tr>       
            
        
    </table>   
    </div>
   
    </body>
    </html>'''
   
    f.write(message)


# In[ ]:





# In[ ]:




