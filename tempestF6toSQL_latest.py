#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import dataFile
import getNameNumbers
import getDays

#
# Read in the CSV file for processing in pandas
#

path = '/home/ec2-user/'
file_name = 'tempest_temp.csv'
full_file = ('/home/ec2-user/tempest_temp.csv')
df = pd.read_csv(full_file, index_col=False)

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)


# In[52]:


import pandas as pd
from pandas import DataFrame, Series

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
  
strike_count = df['strike_count'].sum()


# In[ ]:


import pandas as pd
from pandas import DataFrame, Series
import getDays

todayInfo = getDays.getToday()
yesterdayInfo = getDays.getYesterday()
tomorrowInfo = getDays.getTomorrow()

month, month_num, date, year = todayInfo[0], todayInfo[1], todayInfo[2], todayInfo[3]
yesterday = yesterdayInfo[2]
yesterday = int(yesterday)
nextDay = tomorrowInfo[2]
nextDay = int(nextDay)

#gg = getNameNumbers.sqlWrite()
#print(gg)
#dead1, dead2, dead3, yesterdayDay, date, month_num, year = gg[0], gg[1], gg[2], gg[3], gg[4], gg[5], gg[6]
#date = int(date)
#print(date, month_num, year)

df2 = pd.DataFrame(columns = ['Year', 'Month', 'Date', 'High', 'Low', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10'])
newRow = pd.DataFrame({'Year': year, 'Month': month_num, 'Date': yesterday, 'High': maxT, 'Low': minT, 'totR' : totR, 'corR' : corR, 'Lightning1_5': q, 'Lightning6_10' : r1}, index = [date])
df2 = pd.concat([newRow, df2[:]]).reset_index(drop = True)
print(df2)


# In[ ]:


import pandas as pd
from pandas import DataFrame, Series
import sqlalchemy
import mysql.connector
import sqlite3

print("I made it this far")

'''
database_username = 'chuckwx'
database_password = 'jfr716!!00'
database_ip       = '3.135.162.69'
database_name     = 'tempestf6'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args={'connect_timeout': 30})
df2.to_sql(con=database_connection, name='tempestF6', if_exists='append', index = False)
'''

