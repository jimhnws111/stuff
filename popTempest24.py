#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd
import dataFile
import getNameNumbers
import sqlalchemy
import mysql.connector
import sqlite3
from sqlalchemy import create_engine
import pymysql

# creating connection
engine = create_engine('mysql+pymysql://chuckwx:jfr716!!00@3.135.162.69/hourlyt')

query = """
        select * from testTempest
        where timestamp > now() - interval 28 hour;
        """

df = pd.read_sql(query, engine)
print(df)


# In[60]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import numpy as np

path2 = '/var/www/html/000/'

t = df['temperature']
y = t.to_numpy()
date = df['localT']
x = date.to_numpy()

plt.figure(figsize= (10,6))
plt.yticks(fontsize = 12)
plt.ylabel('Temperature (F)', fontsize=12, fontweight ='bold')

plt.xticks(fontsize = 8, rotation = 45, fontweight = 'bold')
plt.ylabel('Temperature (F)', fontsize=12, fontweight ='bold')
plt.title('Hourly Temperatures - last 24 hours', fontsize = 12, fontweight = 'bold')
plt.plot(x, y, marker = "*", color = "red", linewidth = 4, label = "Temperature")
plt.gca().invert_yaxis()
plt.grid(True)
plt.autoscale(enable = True, axis = 'both', tight = True)

plt.savefig(f'{path2}testSQL')  


# In[ ]:




