#!/usr/bin/env python
# coding: utf-8

# In[11]:


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


# In[12]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import datetime
from datetime import datetime
import sqlalchemy
import mysql.connector
import sqlite3
import getDays
import pymysql as dbapi

#
# Now the Tempest F6 table
#

QUERY = """SELECT * FROM tempestCompF6 
           WHERE month = %s""" % (month_num)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'tempestf6')

cur = db.cursor()
cur.execute(QUERY)
records = cur.fetchall()

qwe = ['Davis']

if qwe == 'Davis':
        df1 = pd.DataFrame(records, columns = ['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD','Rainfall', 'Max_Dew_Point'])
        df1 = df1.drop(df1.columns[[0,6,7]], axis=1)       
else:
        df = pd.DataFrame(records, columns = ['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'totR', 'corR', 'Lightning1_5', 'Lightning6_10'])
        df = df.drop(df.columns[[0,4,5,6,7,8,11,12]], axis=1)       


# In[15]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objs as go

df['Date'] = df['Date'].astype(int)
df['totR'] = df['totR'].astype(float)
df['corR'] = df['corR'].astype(float)
    
fig = go.Figure()
fig.add_trace(go.Bar(
   x=df['Date'],
   y=df['totR'],
   name="Tabulated",
   marker = {'color' : 'red'}))

fig.add_trace(go.Bar(
   x=df['Date'],
   y=df['corR'],
   name="Corrected",
   marker = {'color' : 'green'}))

fig.update_layout(
    title_text = f'{month_abbrev} {year} Tempest', title_x = 0.5, title_font_family = "Arial Black", 
    yaxis_title = "Rain (inches)", 
    yaxis = dict(
        tickfont_family="Arial Black"),
    xaxis_title = "Date", font_family="Arial Black", 
    xaxis = dict(
        tickmode = 'linear',
        tickfont = dict(size = 16), 
        tickfont_family="Arial Black",
        tick0 = 1,
        dtick = 1),
    legend = dict(
        font_family="Arial Black"),
        legend_title = "Rain",
    font = dict(
        size=20
    )    
)

fig.update_xaxes(showgrid = True, linewidth=1, linecolor='black')
fig.update_yaxes(showgrid = True, linewidth=1, linecolor='black')
fig.update_xaxes(showgrid = True, gridwidth=1, gridcolor='black')
fig.update_yaxes(showgrid = True, gridwidth=1, gridcolor='black')     
    
'''    
TOTR = df['totR']
CORR = df['corR']
DATE = df['Date']

y = TOTR.to_numpy()
y1 = CORR.to_numpy()
x = DATE.to_numpy()

fig = px.bar(
data_frame = df,
x = "Date",
y = [y, y1],       
orientation = "v",
barmode = 'group',
color_discrete_sequence=['red', 'green'], 
   
)

fig.update_layout(
title = f'{month} {year}  - Tempest Tabulated vs Corrected',
yaxis_title = "Rainfall (inches)", title_x = 0.5,  
xaxis = dict(
tickmode = 'linear',
tickfont = dict(size = 16), 
tick0 = 1,
dtick = 1),
legend_title = "Rainfall", 
    
)
'''

#fig.show()

fig.write_html(f'/var/www/html/000/tempestComp.html', auto_open = True)   
fig.write_image(f'/var/www/html/000/tempestComp.png', engine="kaleido")  


# In[ ]:





# In[ ]:




