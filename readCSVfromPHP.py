#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from pandas import DataFrame
import os
import calendar
from pretty_html_table import build_table
import sys
import json
from pandas import json_normalize

#
# Read in file with user request for monthly data
#

colNames = ['Rainfall', 'High', 'Low', 'Year', 'Month', 'Day']
df = pd.read_json('/var/www/html/000/monthly.txt')
df = df.drop(df.columns[[0]], axis=1)

#
# Get month name from the month number and year
#

xd = (df.loc[df['Month']].values[0])
sd = (df.loc[df['Month']].values[0])
print(sd)

month_num = int(xd[4])
month_name = calendar.month_name[month_num]
year = int(sd[3])
print(month_num, month_name, year)

df = df.reindex(columns=['Year', 'Month', 'Day', 'HiTemp', 'LowTemp', 'Rain'])
df = df.fillna(0)
print(df)
                         
html_table_blue_light = build_table(df, 'blue_light', text_align='center')

with open('/var/www/html/000/monthlyTable.html', 'w') as f:
    f.write(html_table_blue_light)


# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

df['Day'] = df['Day'].astype(int)
df['High'] = df['HiTemp'].astype(int)
df['Low'] = df['LowTemp'].astype(int)
    
HI = df['High']
LO = df['Low']
DAY = df['Day']

y = HI.to_numpy()
y1 = LO.to_numpy()
x = DAY.to_numpy()
            
plt.style.use('seaborn-v0_8-white')
    
path1 = '/var/www/html/000/'
plt.figure(figsize= (6,4))
plt.locator_params(axis = 'x', nbins = 31)
plt.xlim(1,31)
plt.ylim(0, 105)
plt.xticks(fontsize=10, rotation='vertical')
plt.xlabel('Date', fontsize=10, fontweight ='bold')
plt.yticks(fontsize=12)
plt.ylabel('Temperature (F)', fontsize=10, fontweight ='bold')
plt.locator_params(axis='y', nbins=20)
plt.title(f'{month_name} {year} Temperatures', fontsize=12, fontweight ='bold')
#plt.grid(axis = "y", linewidth = 1.0, color = 'gray')
#plt.grid(axis = "x", linewidth = 1.0, color = 'gray')   
plt.plot(x, y, color = "red", linewidth =3, label ="High")
plt.plot(x, y1, color = "blue", linewidth =3, label ="Low")
plt.legend(fontsize = 12)
plt.savefig(f'{path1}monthlyTemps_db')
#plt.show()


# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import datetime

path1 = '/var/www/html/000/'

df['Day'] = df['Day'].astype(int)
df['Rainfall'] = df['Rain'].astype(float)
    
RAINFALL = df['Rainfall']
DAY = df['Day']

y = RAINFALL.to_numpy()
x = DAY.to_numpy()

plt.style.use('seaborn-v0_8-white')
    
plt.figure(figsize= (6,4))
plt.locator_params(axis = 'x', nbins = 31)
plt.xlim(1, 31)
plt.xticks(fontsize=10, rotation='vertical') 
plt.xlabel('Date', fontsize=12, fontweight ='bold')
plt.yticks(fontsize=12)
plt.ylabel('Rainfall (inches)', fontsize=12, fontweight ='bold')
plt.locator_params(axis='y', nbins=20)
plt.title(f'{month_name} {year} Rainfall', fontsize=12, fontweight ='bold')
#plt.grid(axis = "y", linewidth = 1.0, color = 'gray')
#plt.grid(axis = "x", linewidth = 1.0, color = 'gray')


plt.bar(df['Day'], df['Rain'], color ='green', width = 0.7)
plt.autoscale(enable = True, axis = 'y', tight = True)
#plt.legend(fontsize = 12)
plt.savefig(f'{path1}monthlyRain_db')
#plt.show()


# In[ ]:





# In[ ]:




