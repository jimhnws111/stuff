#!/usr/bin/env python
# coding: utf-8

# In[12]:


import getDays
import daysAndDates
import logging

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('/home/ec2-user/plotTempTest99.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

dayInfo = daysAndDates.daysAndDates()
month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])
month_num = int(month_num)
date = int(date)


# In[13]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime
from datetime import datetime
import sqlalchemy
import mysql.connector
import sqlite3
import getDays
import pymysql as dbapi

sta = ['Davis', 'Tempest']
path1 = '/var/www/html/000/'

#
# Get data from the Davis F6 table first
#

QUERY = """SELECT * FROM davisUpdate 
           WHERE month = %s""" % (month_num)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'davisf6')

cur = db.cursor()
cur.execute(QUERY)
records = cur.fetchall()

#
# Now the Tempest F6 table
#

QUERY1 = """SELECT * FROM tempestCompF6 
           WHERE month = %s""" % (month_num)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'tempestf6')

cur = db.cursor()
cur.execute(QUERY1)
records1 = cur.fetchall()


# In[14]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

sta = ['Davis', 'Tempest']

for qwe in sta:
    print(qwe)
    sta = ['Davis', 'Tempest']

    #
    # Dump the data into a pandas DataFrame
    #

    if qwe == 'Davis':
        df = pd.DataFrame(records, columns = ['index', 'Year', 'Month', 'Date', 'High', 'Low', 'avgTemp', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
        df = df.drop(df.columns[[0,6,7]], axis=1)
    else:
        df = pd.DataFrame(records1, columns = ['index', 'Year', 'Month', 'Date', 'High', 'Low', 'avgTemp', 'HDD', 'CDD', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10'])
        df = df.drop(df.columns[[0,6,7,8,9]], axis=1) 


    df['Date'] = df['Date'].astype(int)
    df['High'] = df['High'].astype(int)
    df['Low'] = df['Low'].astype(int)
    
    HI = df['High']
    LO = df['Low']
    DATE = df['Date']

    y = HI.to_numpy()
    y1 = LO.to_numpy()
    x = DATE.to_numpy()
            
    plt.style.use('seaborn-v0_8-dark')
    
    path1 = '/var/www/html/000/'
    plt.figure(figsize= (10,6))
    plt.locator_params(axis = 'x', nbins = date)
    plt.xlim(1, date)
    plt.ylim(0, 105)
    plt.xticks(fontsize=12)
    plt.xlabel('Date', fontsize=12, fontweight ='bold')
    plt.yticks(fontsize=12)
    plt.ylabel('Temperature (F)', fontsize=12, fontweight ='bold')
    plt.locator_params(axis='y', nbins=20)
    plt.title(f'{month} {year} Temperatures - {qwe}', fontsize=12, fontweight ='bold')
    plt.grid(axis = "y", linewidth = 1.0, color = 'gray')
    plt.grid(axis = "x", linewidth = 1.0, color = 'gray')   
    plt.plot(x, y, marker = "x", color = "red", linewidth =3, label ="High")
    plt.plot(x, y1, marker = "x", color = "blue", linewidth =3, label ="Low")
    plt.legend(fontsize = 12)
    plt.savefig(f'{path1}newTemps_{qwe}')


# In[ ]:




