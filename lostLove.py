#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import calcOneDay
import getDays
from datetime import datetime, timedelta
import calcTimeNow
import daysAndDates
import os

# Calculate the time and date for end of day calculations

xy = calcOneDay.calcOneDay()
start, end = (xy[0], xy[1])
dayInfo = daysAndDates.daysAndDates()

month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])
print(month, month_num, date, year)


# In[22]:


#
# Get the data from the mySQL table for yesterday
#

import pandas as pd
import pymysql as dbapi
from pretty_html_table import build_table
import os

#
# use environmental variables for the SQL query
#

db_user = os.environ.get('dbUser')
db_password = os.environ.get('dbPass')

QUERY2 = """SELECT * FROM davisUpdate 
         WHERE Month = %s""" % (month_num)


html_path = '/var/www/html/000/'
#html_path = '/Users/jameshayes/'
db = dbapi.connect(host='3.135.162.69', user='chuckwx', passwd='jfr716!!00', database = 'davisf6', port = 3306)

cur = db.cursor()
cur.execute(QUERY2)
dateResult = cur.fetchall()

colNames = (['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point']) 
pd.options.display.float_format = '{:,.2f}'.format
df3 = pd.DataFrame(dateResult, columns = colNames) 
df3 = df3.drop(df3.columns[[0, 1]], axis = 1)
df3 = df3.reindex(columns=['Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
df3.to_html(f'{html_path}throttled.html', index = False)     

html_table_blue_light = build_table(df3, 'blue_light', text_align='center', font_size ='32px')

with open(f'{html_path}davisLocal.html', 'w') as f:
          f.write(html_table_blue_light)   

