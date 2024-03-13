#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import dataFile
import getNameNumbers
import sqlalchemy
import mysql.connector
import sqlite3
import NoDaysInMonth

# creating connection
conn = mysql.connector.connect(
  host="3.135.162.69",
  user="chuckwx",
  password="jfr716!!00"
)

mycursor = conn.cursor()

mycursor.execute("USE trweather;")
mycursor.execute("SELECT * FROM trweather WHERE Month = 11 AND Year = 2018 INTO OUTFILE '/tmp/testKRBd.csv';")


# In[ ]:


path = '/tmp/'
path1 = '/home/ec2-user/'
path2 = '/var/www/html/000/'
file_name = 'testKRBd.csv'
data_file = f'{path}{file_name}'
lastFile = f'{path1}trweather.csv'

df = pd.read_csv(data_file, index_col=False, sep = '\t', names = ['id', 'Rain', 'HiTemp', 'LowTemp', 'Year', 'Month', 'Day'])
df = df.drop(df.columns[[0]], axis = 1)
df = df.replace('\\N', 0)
df.to_html(path2 + 'testTRW' + '.html', index = False)


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import calcTimeNow
import getDaysInMonth
import numpy as np
import seaborn as sns
from scipy.interpolate import make_interp_spline
import calendar
import NoDaysInMonth

pathWeb = '/var/www/html/trclimate/'

HI = df['HiTemp']
LO = df['LowTemp']
DATE = df['Day']

y = HI.to_numpy()
y1 = LO.to_numpy()
x = DATE.to_numpy()

Month = (df['Month'].iloc[-1])
year = (df['Year'].iloc[-1])
month = calendar.month_name[Month]

#define x as 200 equally spaced values between the min and max of original x 
xnew = np.linspace(x.min(), x.max(), 200) 

#define spline
HIspl = make_interp_spline(x, y, k=2)
y_smooth = HIspl(xnew)
LOspl = make_interp_spline(x, y1, k=2)
y1_smooth = LOspl(xnew)     
r = NoDaysInMonth.NoDaysInMonth(month,year)
  
plt.figure(figsize= (10,6))
plt.locator_params(axis='x', nbins = r)
plt.xlim(1, r)
plt.xticks(fontsize=12)
plt.xlabel('Date', fontsize=12, fontweight ='bold')
            
plt.ylim(0, 105)
plt.yticks(fontsize=12)
plt.ylabel('Temperature (F)', fontsize=12, fontweight ='bold')
plt.locator_params(axis='y', nbins=20)
plt.title(f'{month} {year} Temperatures', fontsize=12, fontweight ='bold')
plt.grid(True)
plt.grid(axis = "y", linewidth = 2.0, color = 'black')
plt.plot(x, y, color = "red", linewidth =3, label ="High")
plt.plot(x, y1, color = "blue", linewidth =3, label ="Low")
plt.legend(fontsize=12)
plt.savefig(f'{pathWeb}testTempPlot')  


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import calcTimeNow
import getDaysInMonth
import numpy as np
import seaborn as sns
from scipy.interpolate import make_interp_spline
import calendar
import NoDaysInMonth

pathWeb = '/var/www/html/trclimate/'

Month = (df['Month'].iloc[-1])
year = (df['Year'].iloc[-1])
df['Day'] = df['Day'].astype(int)
df['Rain'] = df['Rain'].astype(float)

month = calendar.month_name[Month]
r = NoDaysInMonth.NoDaysInMonth(month,year)
dates = np.arange(1,r + 1)
date = df['Day'] 
rain = df['Rain']

#sns.set_style("whitegrid", {'grid.color': 'black'})
plt.figure(figsize= (10,6))
plt.locator_params(axis='x', nbins = r)
plt.xlim(1, r)
plt.xticks(fontsize=12)
plt.xlabel('Date', fontsize=12, fontweight ='bold')         
#plt.ylim(0, None)
plt.yticks(fontsize=12)
plt.ylabel('Rainfall (inches)', fontsize=12, fontweight ='bold')
plt.locator_params(axis='y', nbins=10)
plt.title(f'{month} {year} Rainfall', fontsize=12, fontweight ='bold')
plt.grid(True)
plt.autoscale(tight=True) 
plt.grid(axis = "y", linewidth = 2.0, color = 'black')
plt.bar(df['Day'], df['Rain'], color = "green", width= 0.6)
#sns.barplot(data = df, x = 'date', y = 'Rain', color = 'g')
plt.savefig(f'{pathWeb}testRainPlot')  

