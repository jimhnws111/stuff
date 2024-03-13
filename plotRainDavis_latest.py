#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import seaborn as sns
import calcTimeNow
import getDaysInMonth
import getNameNumbers


# In[ ]:


from matplotlib.ticker import FormatStrFormatter

path1 = '/var/www/html/trclimate/'

sta = ['Davis']

for qwe in sta:

    wl = getNameNumbers.davis()
    xls_filename, xls_fullfile, path_name, date, month_name, year, r = wl[0], wl[1], \
    wl[2], wl[3], wl[4], wl[5], wl[6]      
                 
    wxdata = f'{path_name}{month_name}_{year}_{qwe}.xlsx'
    df = pd.read_excel(wxdata, skiprows=[0,1])
            
    if qwe == 'Tempest':
        df = df.drop(df.columns[[1,2,3,4,5,8,9]], axis=1)
        df = df.drop(df.index[date:r+1]) 
        df['Date'] = df['Date'].astype(int)
       
    else:
        df = df.drop(df.columns[[1,2,3,4,5,7,8,9,10,11,12,13,14]], axis=1)
        df = df.drop(df.index[date:r+1])
        df['Date'] = df['Date'].astype(int)
        
        
    #Plot the results in matplotlib
    
    plt.style.use('fivethirtyeight')  
    
    #sns.set_style("whitegrid", {'grid.color': 'black'})
    plt.figure(figsize=(10, 6))
    plt.xlim(1, date - 1)
    plt.xticks(fontsize=12)
    plt.xlabel('Date', fontsize=12, fontweight ='bold')
    plt.yticks(fontsize=12)
    #plt.ylim(0, None)
    sns.barplot(data = df, x = 'Date', y = 'Rainfall', color = 'g')
    plt.autoscale(enable = True, axis = 'both', tight = True)
    plt.grid(True)
    plt.ylabel('Rainfall (inches)', fontsize=12, fontweight ='bold')
    plt.title(f'{month_name} {year} Rainfall', fontsize=12, fontweight ='bold')
    plt.savefig(f'{path1}rain_{qwe}') 

