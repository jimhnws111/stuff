#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import getDays

#
# Importing some time and date information
#

todayInfo = getDays.getToday()
yesterdayInfo = getDays.getYesterday()
print(todayInfo)
print(yesterdayInfo)
tomorrowInfo = getDays.getTomorrow()

month, month_num, date, year = todayInfo[0], todayInfo[1], todayInfo[2], todayInfo[3]
yesterday = yesterdayInfo[2]
yesterday = int(yesterday)
nextDay = tomorrowInfo[2]
nextDay = int(nextDay)
print(month, month_num, date, year, yesterday, nextDay)


# In[ ]:


import pandas as pd
from pandas import DataFrame, Series
import math

path = '/home/ec2-user/'
file_name = 'davisDataDump.csv'
data_file = f'{path}{file_name}'
df = pd.read_csv(data_file, index_col=False,names=['temp_hi', 'temp_lo', 'rainfall', 'dew_hi', 'dew_lo'])
print(df)

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

max_temp  = (df.sort_values(by='temp_hi', ascending=False))
max_T = max_temp.iloc[:1]
maxT = max_T['temp_hi'].values[0]
maxT = round(maxT)

min_temp  = (df.sort_values(by='temp_lo', ascending=True))
min_T = min_temp.iloc[:1]
minT = min_T['temp_lo'].values[0]
minT = round(minT)

dew_max = (df.sort_values(by='dew_hi', ascending=False))
dew_max1 = dew_max.iloc[:1]
dewMax = dew_max1['dew_hi'].values[0]
dewMaxT = round(dewMax)

dew_min = (df.sort_values(by='dew_lo', ascending=True))
dew_min1 = dew_min.iloc[:1]
dewMin = dew_min1['dew_lo'].values[0]
dewMinT = round(dewMin)

totR = df['rainfall'].sum()
print(totR)

avgTemp = math.ceil((int(maxT + minT)/2))

hdd = (65 - avgTemp)
if hdd < 0:
    hdd = 0
cdd = (avgTemp - 65)
if cdd < 0:
    cdd = 0    


# In[ ]:


import sqlalchemy
import mysql.connector
import sqlite3

df2 = pd.DataFrame(columns = ['Year', 'Month', 'Date', 'High', 'Low', 'Rainfall', 'Max_Dew_Point'])
newRow = pd.DataFrame({'Year': year, 'Month': month_num, 'Date': yesterday, 'High': maxT, 'Low': minT, 'Rainfall' : totR, 'Max_Dew_Point': dewMaxT }, index = [yesterday])
df2 = pd.concat([newRow, df2]).reset_index(drop = True)
print(df2)

database_username = 'chuckwx'
database_password = 'jfr716!!00'
database_ip       = '3.135.162.69'
database_name     = 'davisf6'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args={'connect_timeout': 30})
df2.to_sql(con=database_connection, name='davisTest', if_exists='append', index = False)

