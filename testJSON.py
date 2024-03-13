#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import base64
import sys
import io
import os
import pandas as pd
import requests

get_json = sys.argv[1]
#final_output = json.loads(base64.b64decode(get_json))
obj = json.loads(get_json)

df = pd.DataFrame(obj)
df = df.drop(df.columns[[0, 7]], axis = 1)

rain = (df[['Rain']]).astype(float)
high = df[['HiTemp']]
low =  df[['LowTemp']]
year = (df[['Year']]).astype(int)
month = (df[['Month']]).astype(int)
day = (df[['Day']]).astype(int)

df['Day'] = df['Day'].astype(int)
df['High'] = round(df['HiTemp'].astype(float),0)
df['Low'] = round(df['LowTemp'].astype(float),0)


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

HI = df['High']
LO = df['Low']
DAY = df['Day']

y = HI.to_numpy()
y1 = LO.to_numpy() 
    
fig = go.Figure()
fig.add_trace(go.Scatter(
   x=df['Day'],
   y=df['High'],
   name="High",
   marker = {'color' : 'red'},
   line = {'width': 4} ))

fig.add_trace(go.Scatter(
   x=df['Day'],
   y=df['Low'],
   name="Low",
   marker = {'color' : 'blue'},
   line = {'width': 4}))       
                 

fig.update_layout(
   title_text = f'Test', title_x = 0.5, title_font_family = "Arial Black", 
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
         
fig.write_image(f'/var/www/html/000/newTemps1.png', engine="kaleido")


# In[ ]:


import requests

with open('/var/www/html/000/newTemps1.png', 'rb') as fd:
    img_data = fd.read()
    
url = "http://trclimate.org/images/"    
files = {"image": ("newTemps1.png", img_data)}
headers = {}
r = requests.post(url, files=files, headers = headers)
print(r)

if r.status_code == 201:
    print("Image uploaded successfully!")


# In[ ]:




