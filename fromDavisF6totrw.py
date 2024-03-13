#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
from datetime import datetime
import sqlalchemy
import mysql.connector
import sqlite3
import pandas as pd

#creating connection
mydb = mysql.connector.connect(
  host="3.135.162.69",
  user="chuckwx",
  password="jfr716!!00"    
)

mycursor = mydb.cursor()

mycursor.execute("use davisf6;")
pop1 = ("select * from davisF6 order by id DESC LIMIT 1 into OUTFILE '/tmp/testDavisF6.csv';")
mycursor.execute(pop1)

dataFile = '/tmp/testDavisF6.csv'

df = pd.read_csv(dataFile, sep = '\t', names = ['id', 'Year', 'Month', 'Day', 'HiTemp', 'LowTemp', 'Rain', 'Max_Dew_Point'])
df = df.drop(['id'], axis = 1)

x = pd.to_datetime(df[['Year', 'Month', 'Day']])
df['timeGroup'] = x
df = df.drop(df.columns[[6]], axis = 1)
df2 = (df.iloc[:,[5,3,4,0,1,2,6]])

rain = float(df2['Rain']); print(rain)
hiTemp = int(df2['HiTemp']);print(hiTemp)
lowTemp = int(df2['LowTemp'])
year = int(df2['Year'])
month = int(df2['Month'])
day = int(df2['Day'])
timeGroup = (df2['timeGroup']).astype('string')
timeGroup = repr(timeGroup)
timeGroup = timeGroup.split(' ')
timeGroup = timeGroup[4]
timeGroup = timeGroup.split('\n')
timeGroup = timeGroup[0]

sql = ("INSERT INTO trw "
      "(Rain, HiTemp, LowTemp, Year, Month, Day, timeGroup) "
       "VALUES (%s, %s, %s, %s, %s, %s, %s)")

strVals = rain, hiTemp, lowTemp, year, month, day, timeGroup
print(strVals)

mycursor.execute("use trweather;")
mycursor.execute(sql, strVals)
mydb.commit()


# In[ ]:




