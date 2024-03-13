#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#
# Get the data from the mySQL table for yesterday
#

import pymysql as dbapi
from pretty_html_table import build_table
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import math
import daysAndDates

dayInfo = daysAndDates.daysAndDates()

month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])

QUERY2 = """SELECT * FROM davisUpdate 
         WHERE Month = %s""" % (month_num)


html_path = '/var/www/html/000/'
db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'davisf6')

cur = db.cursor()
cur.execute(QUERY2)
dateResult = cur.fetchall()

colNames = (['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point']) 
df3 = pd.DataFrame(dateResult, columns = colNames) 
df3 = df3.drop(df3.columns[[0, 1]], axis = 1)
df3 = df3.reindex(columns=['Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
df3.to_html(f'{html_path}throttled.html', index = False)     

html_table_blue_light = build_table(df3, 'blue_light')

with open(f'{html_path}davisLocal.html', 'w') as f:
          f.write(html_table_blue_light)   

