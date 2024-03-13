#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import calcTimeNow
import getDaysInMonth
import getNameNumbers


# In[ ]:


path1 = '/var/www/html/000/'

sta = ['Tempest', 'Davis']

wl = getNameNumbers.tempest_ec2()
xls_filename, xls_fullfile, path_name, date, month_name, year, r = wl[0], wl[1], \
wl[2], wl[3], wl[4], wl[5], wl[6]
    
x_indexes = np.arange(1, r)
height = 0.0
width = 0.25
                
wxdata1 = f'{path_name}{month_name}_{year}_Tempest.xlsx'
wxdata = f'{path_name}{month_name}_{year}_Davis.xlsx'

df = pd.read_excel(wxdata1, skiprows=[0,1])
df = df.drop(df.columns[[1,2,3,4,5,6,8,9]], axis=1)
df = df.drop(df.index[date:r]) 

df1 = pd.read_excel(wxdata, skiprows=[0,1])
df1 = df1.drop(df1.columns[[1,2,3,4,5,7,8,9,10,11,12,13,14]], axis=1)
df1 = df1.drop(df1.index[date:r])              

df2 = pd.merge(df,df1, on='Date')
df2['Date'] = df2['Date'].astype(int)
        
plt.bar(df['Date'], df['corR'], color ='red', width = 0.3, label = "Tempest Corrected")
plt.bar((df1['Date'] + width), df1['Rainfall'], color ='green', width = 0.3, label = "Davis")  
        
plt.figsize = (10,6)
plt.locator_params(axis='x', nbins= r)
plt.tick_params(axis='x', colors='black', direction='out', length=4, width=1)
plt.locator_params(axis='x', nbins= r)
plt.xlim(1, r)
plt.xticks(fontsize=8)
    
plt.xlabel('Date', fontsize=12, fontweight ='bold')
plt.ylim(0, None)
plt.grid(axis = "y", linewidth = 1.0, color = 'black')
plt.yticks(fontsize=12)
plt.ylabel('Rainfall (inches)', fontsize=12, fontweight ='bold')
plt.legend()
plt.title(f'{month_name} {year} Rainfall - Davis vs Tempest', fontsize=12, fontweight ='bold')
plt.savefig(f'{path1}rainfall_DavisTempest') 

