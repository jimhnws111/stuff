#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import dataFile
import datetime
from datetime import datetime
from dateutil.tz import tzutc, tzlocal
import pytz
import sqlalchemy
import mysql.connector
import sqlite3

#
# Read in the CSV file for processing in pandas
#

path_to_file = '/home/ec2-user/'
full_file =(f'{path_to_file}latestTempest1m.csv')
df = pd.read_csv(full_file, index_col=False)

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

latestT = (df['temperature'].iloc[-1]) 
lastT = round((latestT*1.8) + 32)

timezone = pytz.timezone("America/New_York")
recentT = (df['timestamp'].iloc[-1])
dt_object = datetime.fromtimestamp(recentT)
localT = dt_object.astimezone(timezone)
lastTime = localT.strftime('%-I:%M %p')  
#time24 = localT.strftime('%-I')  
#time24 = int(time24)

year = localT.strftime('%Y')
month = localT.strftime('%B')
date = localT.strftime('%-d')
hour = localT.strftime('%-H')
minute = localT.strftime('%-M')

df2 = pd.DataFrame(columns = ['Year', 'Month', 'Date', 'Hour', 'Temperature'])
newRow = pd.DataFrame({'Year': year, 'Month': month, 'Date': date, 'Hour': hour, 'Temperature' : lastT}, index = [0])
df2 = pd.concat([newRow, df2[:]]).reset_index(drop = True)
print(df2)

database_username = 'chuckwx'
database_password = 'jfr716!!00'
database_ip       = '3.135.162.69'
database_name     = 'hourlyt'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args={'connect_timeout': 30})
df2.to_sql(con=database_connection, name='hourlyT', if_exists='append', index = False)

