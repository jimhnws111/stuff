#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sqlalchemy
import mysql.connector
import sqlite3
import pandas as pd
from pandas import DataFrame, Series

# creating connection
conn = mysql.connector.connect(
  host="3.135.162.69",
  user="chuckwx",
  password="jfr716!!00"
)

mycursor = conn.cursor()
mycursor.execute("USE trweather;")
pop1 = ("select * from trw order by timeGroup DESC LIMIT 30;")
mycursor.execute(pop1)
allDays = mycursor.fetchall()

colNames = ['Index', 'Rain', 'HiTemp', 'LowTemp', 'Year', 'Month', 'Day', 'timeGroup']
df = pd.DataFrame(allDays, columns = colNames)
df = df.iloc[::-1]
newDate = df['Month'] + df['Day']

df = df.drop(df.columns[[0, 2, 3, 7]], axis = 1)       
print(df)


# In[4]:


from pretty_html_table import build_table


html_table_blue_light = build_table(df, 'blue_light')

with open('/var/www/html/000/pretty_table.html', 'w') as f:
    f.write(html_table_blue_light)


# In[ ]:




