#!/usr/bin/env python
# coding: utf-8

# In[6]:


import json
import pandas as pd
import calendar
from PIL import Image
from pretty_html_table import build_table
import sys
import os

#
# Read JSON request into a pandas Dataframe
#

df = pd.read_json('/var/www/html/000/monthly.txt')
pd.options.display.float_format = '{:,.2f}'.format

#
# Exit the program if the DataFrame is empty
#

'''
if df.empty:
    print("The dataset is empty")
    Image2 = Image.open('/var/www/html/000/allInOne.png')
    Image2copy = Image2.copy()
    Image1 = Image.open('/var/www/html/000/NoData.png')
    Image1copy = Image1.copy()
    Image2copy.paste(Image1copy, (0, 0))
    Image1copy.save('/var/www/html/000/allInOne.png')     
    
    with open('/var/www/html/000/try1.html', 'w') as f:
        html_table_blue_light = build_table(df, 'blue_light', text_align='center', width="50px")
        f.write(html_table_blue_light)   
    
    with open('/var/www/html/000/try2.html', 'w') as fd2:        
        html_table_green_light = build_table(df, 'green_light', text_align='center')  
        fd2.write(html_table_green_light)  
    
    #htmlFile = ['/var/www/html/000/try1.html', '/var/www/html/000/try2.html']
    
    #for files in htmlFile:        
    #    if os.path.isfile(files):
    #        os.remove(files)
    #    else:
    #        print("Error: %s file not found" % files)
        
    sys.exit()    
'''

#
# Calculating some needed variables for later
#

df = df.drop(df.columns[[0]], axis=1)
date = ((df['Day'])).astype(int)
month_num  = (df['Month']).astype(int)
month_num = month_num[0]
print(month_num)
month_name = calendar.month_name[month_num]
month_abbrev = month_name[0:3]
Year = (df['Year']).astype(int)
year = Year[0]
yearStr = (df['Year']).astype(str)
monthYear = month_abbrev + " " + yearStr
monthYear = monthYear[0]


# In[ ]:


import pandas as pd
import numpy as np
from pretty_html_table import build_table

#
# Calculate the last day of each month
# As well as some means and totals
#

lastDay = calendar.monthrange(year,month_num)
lastDay1 = lastDay[1]

high = (df['HiTemp']).round(0).astype(int)
low = (df['LowTemp']).round(0).astype(int)
avg = ((high + low)/2).round(0).astype(int)
#avg = ((high + low)/2).round(0).astype(int).apply(np.ceil)
hdd = (65 - avg).round(0).astype(int)
hdd = hdd.where(hdd > 0, 0) 
cdd = (avg - 65).round(0).astype(int)
cdd = cdd.where(cdd > 0, 0) 
rain = ((df['Rain']).astype(float).fillna(0))
sumRain = df['Rain'].sum().round(2)

if year < 1989:
    rain = str(rain)
    rain = "M"    
    
month_High_avg = high.mean().round(1) 
month_Low_avg = low.mean().round(1) 
month_avg = avg.mean().round(1)
totHDD = hdd.sum()
totCDD = cdd.sum()

df.insert(6, 'Avg', avg)
df.insert(7, 'HDD', hdd)
df.insert(8, 'CDD', cdd)
df.insert(9, 'High', high)
df.insert(10, 'Low', low)
df.insert(11, 'Date', date)

df = df.reindex(columns=['Year', 'Month', 'Date', 'High', 'Low', 'Avg', 'HDD', 'CDD','Rain'])
df = df.drop(df.columns[[0,1]], index = None, axis=1)
print(df)

avgData = np.array([monthYear, month_High_avg, month_Low_avg, month_avg, totHDD, totCDD, sumRain])
throttle = ['Month', 'Hi', 'Lo', 'Avg', 'HDD', 'CDD', 'Rain']
df2 = pd.DataFrame(avgData, throttle)
df3 = df2.transpose()

#
# Creating and writing table components for display 
#

html_table_blue_light = build_table(df, 'blue_light', text_align='center', width = 'auto')
html_table_green_light = build_table(df3, 'green_light', text_align='center')

with open('/var/www/html/000/try1.html', 'w') as fd1:
          fd1.write(html_table_blue_light)   
        
with open('/var/www/html/000/try2.html', 'w') as fd2:
          fd2.write(html_table_green_light)          


# In[ ]:


import plotly.graph_objects as go
import pandas as pd

fig = go.Figure(data=[go.Table(
    columnwidth = [5,5,5,10,5,5,10],
    header=dict(values=list(df.columns),
                fill_color='lightblue',
                font_size=14,
                line_color='black',
                align='center'),
    cells=dict(values=[df.Date, df.High, df.Low, df.Avg, df.HDD, df.CDD, df.Rain],
               fill_color='white',
               line_color='black',
               font_size=14,
               height=30,
               align='center'))
])    

fig.update_layout(width=430, height=1200)

fig.write_html(f'/var/www/html/000/throttleYes.html')


# In[8]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = go.Figure()
fig.add_trace(go.Bar(
       x=df['Date'],
       y=df['Rain'],
       name="Rainfall",
       yaxis='y2',
       opacity=0.8,
       marker = {'color' : 'darkgreen'}))

fig.add_trace(go.Scatter(
       x=df['Date'],
       y=df['High'],
       name="High",
       marker = {'color' : 'red'},
       yaxis='y', 
       line = {'width': 4} ))

fig.add_trace(go.Scatter(
       x=df['Date'],
       y=df['Low'],
       name="Low",
       marker = {'color' : 'blue'},
       yaxis='y',
       line = {'width': 4}))    

fig.update_layout(
       autosize=False,
       width=1000,
       height=600,
       plot_bgcolor='white',
       title_text = f'{month_name} {year}', title_x = 0.5, title_font_family = "Arial Black",
       yaxis=dict(
        title="Temperature (F)",
          range = [-15,110],  
        tick0 = 0,
        dtick = 10,  
        titlefont=dict(
            color="black"
        ),
        tickfont=dict(
            color="black",
            size = 14, 
          
        )
    ),
       yaxis2=dict(
        title="Rainfall (inches)",
        titlefont=dict(
            color="black"
        ),
        tickfont=dict(
            color="black"
        ),
        anchor="free",
        side="right",
        overlaying = "y",    
        position=1.0),
       
       xaxis = dict(
        title="Date",
        titlefont=dict(
            color="black"
        ),   
        tickmode = 'linear',
        tickfont = dict(size = 14), 
        tickfont_family="Arial Black",
        tick0 = 1,
        dtick = 1),
    
        legend=dict(
    
            orientation="h",
            entrywidth=70,
            yanchor="bottom",
            y=1.00,
            xanchor="right",
            x=1
))               
 
fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black', 
               )
fig.update_yaxes(showline=True, linewidth=1.5, linecolor='black', 
               )

fig.write_html(f'/var/www/html/000/allInOne.html', auto_open = True)    
fig.write_image(f'/var/www/html/000/allInOne.png', engine="kaleido")


# In[ ]:




