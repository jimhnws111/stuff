#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import datetime
from datetime import datetime
import sqlalchemy
import mysql.connector
import sqlite3

#
# creating connection to mySQL
#

mydb = mysql.connector.connect(
  host="3.135.162.69",
  user="chuckwx",
  password="jfr716!!00"    
)

mycursor = mydb.cursor()

#
# Pop out the most recent Davis F6 entry
#

mycursor.execute("use davisf6;")
pop1 = ("select * from davisUpdate order by id DESC LIMIT 1;")
mycursor.execute(pop1)
result = mycursor.fetchall()
print(result)


# In[22]:


import pandas as pd

#
# Read in info form the mySQL table and create a pandas dataFrame
#

colNames = (['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point']) 
df = pd.DataFrame(result, columns = colNames)
df['Day'] = df['Date']
df = df.drop(['index'], axis = 1)

x = pd.to_datetime(df[['Year', 'Month', 'Day']])
df['timeGroup'] = x
df = df.drop(df.columns[[5,6,7,9,10]], axis = 1)
df = df.reindex(columns=['Rainfall', 'High', 'Low', 'Year', 'Month', 'Date', 'timeGroup'])
df.rename(columns = {'Rainfall':'Rain', 'High':'HiTemp', 'Low':'LowTemp', 'Date':'Day'}, inplace = True)


# In[26]:


import pandas as pd

#
# Set up DataFrame info to be written to the trw table
#

rain = float(df['Rain'])
hiTemp = int(df['HiTemp'])
lowTemp = int(df['LowTemp'])
year = int(df['Year'])
month = int(df['Month'])
day = int(df['Day'])

timeGroup = (df['timeGroup']).astype('string')
timeGroup = repr(timeGroup)
timeGroup = timeGroup.split(' ')
timeGroup = timeGroup[4]
timeGroup = timeGroup.split('\n')
timeGroup = timeGroup[0]

print(rain, hiTemp, lowTemp, year, month, day, timeGroup)


# In[27]:


import sqlalchemy
import mysql.connector
import sqlite3
import pandas as pd

#
# Write the values from the DataFrame to the trw table
#


sql = ("INSERT INTO trw"
      "(Rain, HiTemp, LowTemp, Year, Month, Day, timeGroup) "
       "VALUES (%s, %s, %s, %s, %s, %s, %s)")

strVals = rain, hiTemp, lowTemp, year, month, day, timeGroup
print(strVals)

mycursor.execute("use trweather;")
mycursor.execute(sql, strVals)
mydb.commit()


# In[ ]:




