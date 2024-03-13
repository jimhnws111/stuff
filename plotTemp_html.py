#!/usr/bin/env python
# coding: utf-8

# In[1]:


import getDays
import daysAndDates

#
# Calculating some date/time stuff
#

dayInfo = daysAndDates.daysAndDates()
month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])
month_num = int(month_num)
date = int(date)
month_abbrev = month[0:3]


# In[2]:


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


# In[8]:


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
        df = pd.DataFrame(records, columns = ['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
        df = df.drop(df.columns[[0,6,7]], axis=1)
    else:
        df = pd.DataFrame(records1, columns = ['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10'])
        df = df.drop(df.columns[[0,6,7,8,9]], axis=1)  
        
    df['Date'] = df['Date'].astype(int)
    df['High'] = df['High'].astype(int)
    df['Low'] = df['Low'].astype(int)
    
    HI = df['High']
    LO = df['Low']
    DATE = df['Date']

    y = HI.to_numpy()
    y1 = LO.to_numpy() 
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
       x=df['Date'],
       y=df['High'],
       name="High",
       marker = {'color' : 'red'},
       line = {'width': 4} ))

    fig.add_trace(go.Scatter(
       x=df['Date'],
       y=df['Low'],
       name="Low",
       marker = {'color' : 'blue'},
       line = {'width': 4}))       
                 

    fig.update_layout(
        title_text = f'{month_abbrev} {year} {qwe}', title_x = 0.5, title_font_family = "Arial Black", 
        yaxis_title = "Temperature", 
        yaxis = dict(
            tickfont_family="Arial Black",
            range = [0,100], 
            tickmode = 'linear',
            tickfont = dict(size = 14),  
            tick0 = 0,
            dtick = 10,
            tickangle = 0),
        xaxis = dict(
        tickmode = 'linear',
        tickfont = dict(size = 14), 
        tickfont_family="Arial Black",
        tick0 = 1,
        dtick = 1),
        
        legend = dict(
            font_family="Arial Black"),
            legend_title = "Temperature",
            font = dict(size=20),
    )
           
    fig.update_xaxes(showgrid = True, linewidth=1, linecolor='black')
    fig.update_yaxes(showgrid = True, linewidth=1, linecolor='black')
    fig.update_xaxes(showgrid = True, gridwidth=1, gridcolor='black')
    fig.update_yaxes(showgrid = True, gridwidth=1, gridcolor='black')     
               
    #fig.show()    
    fig.write_html(f'/var/www/html/000/newTemps1_{qwe}.html', auto_open = True)    
    fig.write_image(f'/var/www/html/000/newTemps1_{qwe}.png', engine="kaleido")


# In[ ]:





# In[ ]:




