#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pymysql as dbapi
import sys
import csv
import sandbox1
import sandbox2
#from daysAndDatesNew import daysAndDatesNew
import daysAndDatesNew
from createF6 import createF6

#
# Import data for use in the alamanc
#

dayInfo = daysAndDatesNew.daysAndDatesNew()
month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])

sdf = createF6(df)
maxT, minT, dewMaxT, throttle, rainfall, avgTemp, hdd, cdd = sdf[0], sdf[1], sdf[2], sdf[3], sdf[4], sdf[5], sdf[6], sdf[7]

nmlData = sandbox2.sandbox2()
nmlHi = nmlData[3]
nmlLo = nmlData[4]

highData = sandbox1.recordHigh()
lowData = sandbox1.recordLow()
rainData = sandbox1.recordRain()

highPhrase = highData[2]
lowPhrase = lowData[2]
rainPhrase = rainData[2]

filePath = '/var/www/html/000/climoDavisTest111.txt'
#filePath = '/Users/jameshayes/Sites/climoDavisText111.txt'

def almanac():
    
    """Set and and write the daily almanac"""

    with open(f'{filePath}','w') as outfile1: 
        print(f'Daily almanac for {month} {yesterday}, {year}', file = outfile1)
        print('\n', file = outfile1)
        print(f'The high yesterday was {maxT} degrees', file = outfile1)
        print(f'The low yesterday was {minT} degrees', file = outfile1)
        print(f'The average temperature was {avgTemp} degrees', file = outfile1)
        print(f'The rainfall yesterday was {("%.2f" % rainfall)} inches', file = outfile1)
        if hdd == 0:
            print('')
        else:
            print(f'There were {hdd} heating degree days', file = outfile1)
        if cdd == 0:
            print('')
        else:
            print(f'There were {cdd} cooling degree days', file = outfile1)                      
    
        print('\n', file = outfile1)
    
        if date == 1:
            print(f'Normal and Record information for {nextMonth} {nextDay}, {year}', file = outfile1)
            print('\n', file = outfile1)
            print(f'The normal high for today is {nmlHi} degrees', file = outfile1)
            print(f'The normal low for today is {nmlLo} degrees' , file = outfile1)
            print('\n', file = outfile1)
            print(highPhrase, file = outfile1)
            print(lowPhrase, file = outfile1)
            print(rainPhrase, file = outfile1)  
        
        else:
            print(f'Normal and Record information for {month} {date}, {year}', file = outfile1)
            print('\n', file = outfile1)
            print(f'The normal high for today is {nmlHi} degrees', file = outfile1)
            print(f'The normal low for today is {nmlLo} degrees' , file = outfile1)
            print('\n', file = outfile1)
            print(highPhrase, file = outfile1)
            print(lowPhrase, file = outfile1)
            print(rainPhrase, file = outfile1)                   
            
almanac()            


# In[ ]:




