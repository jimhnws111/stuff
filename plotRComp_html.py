#!/usr/bin/env python
# coding: utf-8

# In[14]:


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
# First the Tempest F6 table
#

QUERY = """SELECT * FROM davisUpdate 
           WHERE month = %s""" % (month_num)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'davisf6')

cur = db.cursor()
cur.execute(QUERY)
records = cur.fetchall()

#
# Now the Davis F6 table
#

QUERY1 = """SELECT * FROM tempestCompF6 
           WHERE month = %s""" % (month_num)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'tempestf6')

cur = db.cursor()
cur.execute(QUERY1)
records1 = cur.fetchall()


# In[18]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

sta = ['Davis', 'Tempest']

for qwe in sta:
    print(qwe)
    
    #
    # Dump the data into a pandas DataFrame
    #

    if qwe == 'Davis':
        df1 = pd.DataFrame(records, columns = ['index', 'Year', 'Month', 'Date', 'High', 'Low','Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
        df1 = df1.drop(df1.columns[[0,4,5,7]], axis = 1)
        df1['Date'] = df1['Date'].astype(int)
        df1['Rainfall'] = df1['Rainfall'].astype(float)
        Davis = df1['Rainfall']              
        
    else:
        df2 = pd.DataFrame(records1, columns = ['index', 'Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD','totR', 'corR', 'Lightning1_5', 'Lightning6_10'])
        df2 = df2.drop(df2.columns[[0,4,5,6,8,9]], axis = 1) 
        df2['Date'] = df2['Date'].astype(int)
        df2['corR'] = df2['corR'].astype(float)
        Tempest = df2['corR']  

        
df1['corR'] = df2['corR'].values
df1 = df1.drop(df1.columns[[3,4,6]], axis = 1)

fig = go.Figure()
fig.add_trace(go.Bar(
   x=df1['Date'],
   y=df1['Rainfall'],
   name="Davis",
   marker = {'color' : 'red'}))

fig.add_trace(go.Bar(
   x=df1['Date'],
   y=df1['corR'],
   name="Tempest",
   marker = {'color' : 'green'}))

fig.update_layout(
    title_text = f'{month_abbrev} {year} Davis vs Tempest', title_x = 0.5, title_font_family = "Arial Black", 
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

#fig.show()
fig.write_html(f'/var/www/html/000/newRComp.html', auto_open = True) 
fig.write_image(f'/var/www/html/000/newRComp.png', engine="kaleido") 


# In[ ]:





# In[ ]:




