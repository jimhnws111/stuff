#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import csv
import sqlalchemy
import mysql.connector
import sqlite3
import os
from dateutil.tz import tzutc, tzlocal
import pytz
import datetime
import time
from datetime import datetime, timedelta

colNames1 = ['temp', 'dew_point','hum', 'wind_dir', 'wind_speed', 'rainfall','rain_rate', 'htindx', 'final_baro', 'baro_trend', 'timestamp']
df1 = pd.read_csv('/home/ec2-user/davisTableBig.csv', names = colNames1)

timestamp = (df1['timestamp'].iloc[-1])
timestamp = int(timestamp)
timezone = pytz.timezone("America/New_York")
recentTime = (df1['timestamp'].iloc[-1])
recentTime = int(recentTime)
dt_object = datetime.fromtimestamp(recentTime)
localT = dt_object.astimezone(timezone)
lastTime = localT.strftime('%I:%M %p')

temp = (df1['temp'].iloc[-1]) 
dew_point = (df1['dew_point'].iloc[-1]) 
hum = (df1['hum'].iloc[-1]) 
wind_dir = (df1['wind_dir'].iloc[-1])
wind_speed = (df1['wind_speed'].iloc[-1])
rainfall = (df1['rainfall'].iloc[-1])
rain_rate = (df1['rain_rate'].iloc[-1])
htindx = (df1['htindx'].iloc[-1])
final_baro = (df1['final_baro'].iloc[-1])
baro_trend = (df1['baro_trend'].iloc[-1])

df2 = pd.DataFrame(columns = ['timestamp', 'temp', 'dew_point','hum', 'wind_dir', 'wind_speed', 'rainfall','rain_rate', 'htindx', 'final_baro', 'baro_trend', 'lastTime'])
newRow = pd.DataFrame({'timestamp': timestamp, 'temp': temp, 'dew_point': dew_point, 'hum': hum, 'wind_dir': wind_dir, 'wind_speed': wind_speed, 'rainfall': rainfall, 'rain_rate': rain_rate, 'htindx': htindx, 'final_baro': final_baro, 'baro_trend': baro_trend, 'lastTime': lastTime}, index = [0])
df2 = pd.concat([newRow, df2[:]]).reset_index(drop = True)


#
# use environmental variables for the SQL query
#

#db_user = os.environ.get('dbUser')
#db_password = os.environ.get('dbPass')

database_username = 'chuckwx'
database_password = 'jfr716!!00'
database_ip       = '3.135.162.69'
database_name     = 'trweather'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
df2.to_sql(con=database_connection, name='davisMinute', if_exists='append', index = False)  




conn = mysql.connector.connect(
  host='3.135.162.69',
  user= 'chuckwx',
  password='jfr716!!00'
)

mycursor = conn.cursor()
mycursor.execute("USE trweather;")
pop1 = ("select * from davisMinute WHERE davisMinute.id mod 30 = 0 ORDER BY id DESC LIMIT 25;")
         
mycursor.execute(pop1)
hours = mycursor.fetchall()

colNames3 = ['id', 'timestamp', 'temp', 'dew_point','hum', 'wind_dir', 'wind_speed', 'rainfall','rain_rate', 'htindx', 'final_baro', 'baro_trend', 'lastTime']
df4 = pd.DataFrame(hours, columns = colNames3)
df4 = df4.drop(df4.columns[[0, 1, 2, 4, 5,  6, 7, 8, 9, 10]], axis = 1)
df4 = df4.iloc[::-1]

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import seaborn as sns

df4['dew_point'] = df4['dew_point'].astype(int)
df4['lastTime'] = df4['lastTime'].astype(str)

dp = df4['dew_point']
y = dp.to_numpy()
hour = df4['lastTime']
x = hour.to_numpy()

sns.set_style('darkgrid')

print("Ready to create images")

path1 = '/var/www/html/000/'
plt.figure(figsize= (10,6))
plt.xticks(fontsize = 9, rotation = 45, fontweight = 'bold')
plt.ylabel('Dew Point (F)', fontsize=12, fontweight ='bold')
plt.yticks(fontsize = 12, fontweight = 'bold')
plt.grid(axis = "y", linewidth = 1.0, color = 'gray')
plt.grid(axis = "x", linewidth = 1.0, color = 'gray')
plt.plot(x, dp, marker = "*", color = "red", linewidth = 4, label = "Dew Point")
plt.title('12 Hour Davis Dew Point', fontsize = 12, fontweight = 'bold')
plt.savefig(f'{path1}testDP')       
#plt.show()

