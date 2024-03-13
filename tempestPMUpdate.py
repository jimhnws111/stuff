#!/usr/bin/env python
# coding: utf-8

# In[1]:


import calcOneDay
import getDays
import daysAndDates
from datetime import datetime, timedelta
import calcTimeNow
import checkDST

# Calculate the time and date for end of day calculations
#
# First determine whether we are in DST or not
#

# Check DST setting
isDST = checkDST.checkDST()

if isDST == 1:
    now = datetime.now()
    end = int(datetime.timestamp(now))
    start = (end - 55800)
    start = str(start)
    end = str(end)
    
else:
    now = datetime.now()
    end = int(datetime.timestamp(now))
    start = (end - 59400)
    start = str(start)
    end = str(end)

dayInfo = daysAndDates.daysAndDates()
print(dayInfo)

month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])
month_num = int(month_num)
date = int(date)


# In[ ]:


import datetime
from datetime import datetime
import dataFile
import getNameNumbers
import requests

#
# Get data from the Tempest database 
#

token = '877f6425-04a5-4f33-86e7-7123b7ef53d9'
protocol = 'https://'
urlSiteDevice = 'swd.weatherflow.com/swd/rest/observations/device/'
urlSiteStation = 'swd.weatherflow.com/swd/rest/observations/station/'
deviceID = '246921'
stationID = '95775'
preToken = '&token='
preStart = '?time_start='
preEnd = '&time_end='
start_time = start
end_time = end
dayOffset = '&day_offset=1'
format1 = '&format=csv'

#
# Put it together
# 

goGetDeviceSummary = (f'{protocol}{urlSiteDevice}{deviceID}{preStart}{start_time}{preEnd}{end_time}{format1}{preToken}{token}')
r =  requests.get(goGetDeviceSummary)

path = '/home/ec2-user/'
file_name = 'tempest_Update.csv'
full_file = f'{path}{file_name}'

with open(full_file,'w') as fd:
     fd.write(r.text)


# In[ ]:


import pandas as pd
import numpy as np
from pandas import DataFrame,Series
import math

#
# Read in Tempest data from csv into a Pandas DataFrame
#

df = pd.read_csv('/home/ec2-user/tempest_Update.csv', index_col=False)

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


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate
import os

#
# Get normal highs and lows
#

#
# use environmental variables for the SQL query
#

db_user = os.environ.get('dbUser')
db_password = os.environ.get('dbPass')

QUERY = """SELECT * FROM avgHiLo 
           WHERE Month = %s 
           AND Day = %s""" % (month_num, date)

db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

cur = db.cursor()
cur.execute(QUERY)
result = cur.fetchall()

dataset = result[0]
nmlHi = int(dataset[3])
nmlLo = int(dataset[4])

#
# Get the record high for the date
#

QUERY1 = """SELECT * FROM recHigh 
           WHERE Month = %s 
           AND Day = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

cur = db.cursor()
cur.execute(QUERY1)
result1 = cur.fetchall()
recordHigh = result1[0]
recHigh = int(recordHigh[1])
recHighYear = int(recordHigh[4])

#
# Get the record low for the date
#

QUERY2 = """SELECT * FROM recLow 
           WHERE Month = %s 
           AND Day = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

cur = db.cursor()
cur.execute(QUERY2)
result2 = cur.fetchall()
recYearNum = len(result2)
recordLow = result2[0]
recLow = int(recordLow[1])
recLowYear = int(recordLow[4])

#
# Get the record rainfall for the date
#

QUERY3 = """SELECT * FROM recRain 
           WHERE Month = %s 
           AND Day = %s""" % (month_num, date)


db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

cur = db.cursor()
cur.execute(QUERY3)
result3 = cur.fetchall()
recordRain = result3[0]
recRain = recordRain[1]
recRainYear = int(recordRain[4])


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate
import sandbox1
import sandbox2
from gtts import gTTS 
import os

#
# Retrieve normal and record data that has been checked for 
# multiple values 
#

nmlData = sandbox2.sandbox2()
nmlHi = nmlData[3]
nmlLo = nmlData[4]

highData = sandbox1.recordHigh()
lowData = sandbox1.recordLow()
rainData = sandbox1.recordRain()

highPhrase = highData[2]
lowPhrase = lowData[2]
rainPhrase = rainData[2]

#
# Write the phrases to a text file for display on the page
#

with open('/var/www/html/000/climoTempestText.txt','w') as outfile1: 
    print(f'Daily almanac for {month} {date}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The high so far today was {maxT} degrees', file = outfile1)
    print(f'The low so far today was {minT} degrees', file = outfile1)
    print(f'The average temperature was {avgTemp} degrees', file = outfile1)
    print(f'The rainfall so far today was {("%.2f" % corR)} inches', file = outfile1)
    if hdd == 0:
        print('')
    else:
        print(f'There were {hdd} heating degree days', file = outfile1)
    if cdd == 0:
        print('')
    else:
        print(f'There were {cdd} cooling degree days', file = outfile1)
            
    
    print('\n', file = outfile1)
    
    print(f'Normal and Record information for {month} {date}, {year}', file = outfile1)
    print('\n', file = outfile1)
    print(f'The normal high for today is {nmlHi} degrees', file = outfile1)
    print(f'The normal low for today is {nmlLo} degrees' , file = outfile1)
    print('\n', file = outfile1)
    print(highPhrase, file = outfile1)
    print(lowPhrase, file = outfile1)
    print(rainPhrase, file = outfile1)  
    

maxT = str(maxT)   
minT = str(minT)
avgTemp = str(avgTemp)
totR = str(totR)
nmlHi = str(nmlHi)
nmlLo = str(nmlLo)
date = str(date)

# Text to convert to audio 
mytext = 'Daily almanac for ' + month + ' ' + date + '  ' + year + ','
mytext1 = 'The high today was ' + maxT + ','
mytext2 = 'The low today was ' + minT + ', '  
mytext4 = 'The rainfall today was ' +  totR + ',' + ','
mytext5 = 'The normal high for today is ' + nmlHi + ','
mytext6 = 'The normal low for today is ' + nmlLo + ','
mytext7 = highPhrase + ','
mytext8 = lowPhrase + ','
mytext9 = rainPhrase

cliMsg = (mytext + mytext1 + mytext2 + mytext4 + mytext5 + mytext6 + mytext7 + mytext8 + mytext9)
    
# Language in which you want to convert 
language = 'en'
  
# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
myobj = gTTS(text=cliMsg, lang=language, slow=False) 
  
# Saving the converted audio in a mp3 file named 
# welcome  
myobj.save("/var/www/html/000/almanac.mp3") 

