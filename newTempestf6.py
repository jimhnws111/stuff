#!/usr/bin/env python
# coding: utf-8

# In[35]:


import calcOneDay
import getDays

# Calculate the time and date for end of day calculations

xy = calcOneDay.calcOneDay()
start, end = (xy[0], xy[1])

todayInfo = getDays.getToday()
yesterdayInfo = getDays.getYesterday()
tomorrowInfo = getDays.getTomorrow()

month, month_num, date, year = todayInfo[0], todayInfo[1], todayInfo[2], todayInfo[3]
yesterday = yesterdayInfo[2]
yesterday = int(yesterday)
nextDay = tomorrowInfo[2]
nextDay = int(nextDay)


# In[37]:


import sqlalchemy
import mysql.connector
import sqlite3
import pandas as pd
from pandas import DataFrame, Series
import math
import pymysql

# creating connection
conn = mysql.connector.connect(
  host="3.135.162.69",
  user="chuckwx",
  password="jfr716!!00"
)

mycursor = conn.cursor()
mycursor.execute("USE tempestwx;")
pop1 = ("select * from tempestWX order by timestamp DESC LIMIT 1440;")
mycursor.execute(pop1)
allDays = mycursor.fetchall()

colNames = ['timestamp', 'wind_avg', 'wind_gust', 'wind_dir', 'pressure', 'temperature', 'humidity', 
           'uv', 'solar_radiation', 'precip', 'strike_distance', 'strike_count', 'battery', 'local_daily_precip',
           'precip_final', 'local_daily_precip_final']
df = pd.DataFrame(allDays, columns = colNames)
df = df.drop(df.columns[[1, 2, 3, 4, 6, 7, 8, 11, 12, 13, 15]], axis = 1) 

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

max_temp  = (df.sort_values(by='temperature', ascending=False))
max_T = max_temp.iloc[:1]
maxT = max_T['temperature'].values[0]
maxT = round((maxT*1.8) + 32)

min_temp  = (df.sort_values(by='temperature', ascending=True))
min_T = min_temp.iloc[:1]
minT = min_T['temperature'].values[0]
minT = round((minT*1.8) + 32)

#cor_rain = (df.sort_values(by='local_daily_precip_final', ascending=False))
#corR_rain = cor_rain.iloc[:1]
#corR = corR_rain['local_daily_precip_final'].values[0]
#corR = round((corR*0.03937), 2)

cor_rain = df['precip_final'].sum()
corR = round((cor_rain*0.03937), 2)
print(corR)

tot_rain = df['precip'].sum()
totR = round((tot_rain*0.03937), 2)

avgTemp = math.ceil((int(maxT + minT)/2))

hdd = int(65 - avgTemp)
if hdd < 0:
    hdd = 0
cdd = int(avgTemp - 65)
if cdd < 0:
    cdd = 0  

strike_distance = (df.sort_values(by='strike_distance', ascending=False))
lightning1 = (df['strike_distance'].between(1,8))
lightning2 = (df['strike_distance'].between(9,16))

df.insert(5,'lightning1',lightning1)
df.insert(6,'lightning2',lightning2)

#Determine if the strike distance is close enough to count as a thunderstorm
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
        
     

    
    
rte1 = (year, month_num, yesterday, maxT, minT, avgTemp, hdd, cdd, totR, corR, q, r1)
df2 = pd.DataFrame(rte1)
df2 = df2.transpose()
df2.columns = ['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10'] 

database_username = 'chuckwx'
database_password = 'jfr716!!00'
database_ip       = '3.135.162.69'
database_name     = 'tempestf6'
database_connection = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args={'connect_timeout': 30})
df2.to_sql(con=database_connection, name='testTempestf6', if_exists='append', index = False)


# In[31]:


import sqlalchemy
import mysql.connector
import sqlite3
import pandas as pd
from pandas import DataFrame, Series
import math
import pymysql as dbapi

#
# Get the data from the mySQL table for yesterday
#

html_path = '/var/www/html/000/'

QUERY3 = """SELECT * FROM testTempestf6 
         WHERE Month = %s""" % (month_num)

db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'tempestf6')

cur = db.cursor()
cur.execute(QUERY3)
dateResult = cur.fetchall()
print(dateResult)

colNames = (['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10']) 
df4 = pd.DataFrame(dateResult, columns = colNames) 
df4 = df4.reindex(columns=['Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10'])
df4.to_html(f'{html_path}throttleTempest.html', index = False) 


# In[ ]:




