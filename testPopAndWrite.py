#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import dataFile
import getNameNumbers
import sqlalchemy
import mysql.connector
import sqlite3

# creating connection
conn = mysql.connector.connect(
  host="3.135.162.69",
  user="chuckwx",
  password="jfr716!!00"
   
)

mycursor = conn.cursor()
mycursor.execute("USE hourlyt;")
pop1 = ("select @startTime := timeStamp from testTempest order by id DESC LIMIT 1;")
pop2 = ("SELECT @endTime := DATE_SUB(@startTime, INTERVAL 24 Hour);")
pop3 = ("SELECT * from testTempest WHERE timeStamp BETWEEN @endTime AND @startTime into OUTFILE '/tmp/testTempest1.csv';")
popSelect = pop1 + pop2 + pop3

mycursor.execute(popSelect)


# In[1]:


path = '/tmp/'
path1 = '/home/ec2-user/'
path2 = '/var/www/html/000/'
file_name = 'testTempest1.csv'
data_file = f'{path}{file_name}'
lastFile = f'{path1}poppedSQL.csv'

df = pd.read_csv(data_file, index_col=False, sep = '\t', names = ['id', 'DateTime', 'LocalTime', 'Temperature'])
df = df.drop(df.columns[[0]], axis = 1)
print(df)

#df.to_csv(lastFile, sep = ',', index = False)
df.to_html(path2 + 'testT' + '.html', index = False, justify = 'center')


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import numpy as np

t = df['Temperature']
y = t.to_numpy()
date = df['LocalTime']
x = date.to_numpy()

plt.figure(figsize= (10,6))
plt.yticks(fontsize = 12)
plt.ylabel('Temperature (F)', fontsize=12, fontweight ='bold')
#plt.locator_params(axis='y', nbins=20)

plt.xticks(fontsize = 8, rotation = 45, fontweight = 'bold')
plt.ylabel('Temperature (F)', fontsize=12, fontweight ='bold')
plt.title('Hourly Temperatures - last 24 hours', fontsize = 12, fontweight = 'bold')
plt.plot(x, y, marker = "*", color = "red", linewidth = 4, label = "Temperature")
plt.grid(True)
plt.autoscale(enable = True, axis = 'both', tight = True)

plt.savefig(f'{path2}testFire')  

