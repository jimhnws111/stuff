#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import datetime
from datetime import datetime
from dateutil.tz import tzutc, tzlocal
import pytz
import sqlalchemy
import mysql.connector
import sqlite3
import os

#
# Read in the CSV file for processing in pandas
#

path_to_file = '/home/ec2-user/'
full_file =(f'{path_to_file}latestTempest1m.csv')
df = pd.read_csv(full_file, index_col=False)

#
# Create YYYY-MM-DD from timestamp

timezone = pytz.timezone("America/New_York")
recentTime = (df['timestamp'].iloc[-1])
dt_object = datetime.fromtimestamp(recentTime)
localT = dt_object.astimezone(timezone)
localTime = localT.replace(tzinfo=None)
localSet = localTime.strftime(('%Y-%m-%d %H:%M'))

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

latestT = (df['temperature'].iloc[-1]) 
print(latestT)
lastT = round((latestT*1.8) + 32)

timezone = pytz.timezone("America/New_York")
recentT = (df['timestamp'].iloc[-1])
dt_object = datetime.fromtimestamp(recentT)
localT = dt_object.astimezone(timezone)
lastTime = localT.strftime('%I:%M %p')  
time24 = localT.strftime('%-H')  
time24 = int(time24)
print(time24)

print(lastT, localTime, lastTime)

# write the data to a csv file with an html suffix

#new_path = '/Users/jameshayes/'
#new_path = '/home/ec2-user/'

#with open(f'{new_path}testT_tempest.csv', 'w') as outfile:
#    print(f'{localTime},{lastTime},{lastT}',file = outfile)
    
df2 = pd.DataFrame(columns = ['timestamp', 'localT', 'temperature'])
newRow = pd.DataFrame({'timestamp': localSet, 'localT': lastTime, 'temperature': lastT}, index = [0])
df2 = pd.concat([newRow, df2[:]]).reset_index(drop = True)
print(df2)

#
# use environmental variables for the SQL query
#

db_user = os.environ.get('dbUser')
db_password = os.environ.get('dbPass')

database_username = db_user
database_password = db_password
database_ip       = '3.135.162.69'
database_name     = 'hourlyt'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
df2.to_sql(con=database_connection, name='testTempest', if_exists='append', index = False) 

