#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import urllib
import requests
import os
import datetime
from datetime import datetime
import time


# In[3]:


# Get the first part of the gridded forecast...

file_path = '/var/www/html/000/' 
file_name = 'skylinefcst.txt'
full_file = file_path + file_name

urlTest1 = 'https://api.weather.gov/points/40.3422,-76.7151' # here
urlTest2 = 'https://api.weather.gov/points/39.9752,-74.1298' # home   

r =  requests.get(urlTest1)
r.encoding = 'utf-8'
x = r.json()

firstHack = x['properties']['forecast']
r1 = requests.get(firstHack)
x1 = r1.json()

secondHack = x1['properties']['periods']
w = len(secondHack)
j = 0

print('Here is the forecast for Skyline View, PA','\n')

with open(full_file, 'w') as outfile: 
    print('Here is the forecast for Skyline View, PA','\n', file = outfile)

    while j < w:
        dse = (secondHack[j])
        dayOfWeek = dse['name']
        detailedFcst = dse['detailedForecast']
        dayFcst = (f'{dayOfWeek}...{detailedFcst}')
        print(dayFcst)
    
        print(f'{dayFcst}', file = outfile)
    
        j+= 1


# In[6]:


# Get the first part of the gridded forecast...

file_path = '/var/www/html/000/' 
file_name = 'tomsriverfcst.txt'
full_file = file_path + file_name

urlTest2 = 'https://api.weather.gov/points/39.9752,-74.1298' # home   

r = requests.get(urlTest2)
r.encoding = 'utf-8'
x = r.json()

firstHack = x['properties']['forecast']
r1 = requests.get(firstHack)
x1 = r1.json()

secondHack = x1['properties']['periods']
w = len(secondHack)
j = 0
print(f'Here is the forecast for Toms River, NJ','\n')


with open(full_file, 'w') as outfile: 
    print('Here is the forecast for Toms River NJ','\n', file = outfile)

    while j < w:
        dse = (secondHack[j])
        dayOfWeek = dse['name']
        detailedFcst = dse['detailedForecast']
        dayFcst = (f'{dayOfWeek}...{detailedFcst}')
        print(dayFcst)
    
        print(f'{dayFcst}', file = outfile)
    
        j+= 1       


# In[ ]:





# In[ ]:




