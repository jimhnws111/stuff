#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import urllib
import requests
import csv
import re
import pandas as pd
import sys
import collections
import datetime as datetime
from datetime import datetime  
from datetime import timezone
import numpy as np


# In[4]:


#
# reads in the JSON file as a Python dictionary
# should be the same directory into which the data file
# was written - most likely the installation directory
# filename is synoptic.json

data_dir_file = '/Users/jameshayes/synoptic.json' # ***THIS NEEDS TO BE CHANGED***

with open(data_dir_file) as fr:
    dataAPI = json.load(fr)

#
# Set some file name variables
#
# Set path_to_file to your installation directory
#

path_to_file = ('/Users/jameshayes/') # ***THIS NEEDS TO BE CHANGED to your installation directory*** 
name_of_file = ('API_data.txt') # this is the file to which the sorted data is written
full_file = f'{path_to_file}{name_of_file}'

#
# Determine the number of observations to process
#

x = 0
for data in dataAPI['STATION']:
    if 'MINMAX' in data:
        pass 
    else:
        data['MINMAX'] = 'None'
                      
    x = x + 1 

print()    
print(f'There are {x} observations this hour')
print()
    
station = dataAPI['STATION']
y = 0 

with open(full_file, 'w') as outfile: 

    while (y < x):
      
        mnet_id = station[y]
        stid = mnet_id.get('STID')
        station_name = mnet_id.get('NAME')
        station_name = station_name.replace(',','')
        state = mnet_id.get('STATE')
        lat = mnet_id.get('LATITUDE')
        lon = mnet_id.get('LONGITUDE')
        el = mnet_id.get('ELEVATION')
        tz = mnet_id.get('TIMEZONE')
        temps_info = mnet_id.get('MINMAX')
        if temps_info == 'None':
            print(f'The air temperature information is missing for {stid}') 
            air_temps_info = 'None'
            dates = 'None'
            max_utc = 'None'
            min_utc = 'None'
            time_min_utc = 'None'
            time_max_utc = 'None'
            y +=1
            continue      
  
        air_temps_info = temps_info.get('air_temp_value_1')
        dates = air_temps_info.get('dates')
        dates = (''.join(dates))
        max_utc = air_temps_info.get('value_max_utc')
        max_utc = ("".join([str(i)for i in max_utc]))  
        min_utc = air_temps_info.get('value_min_utc')
        min_utc = ("".join([str(i)for i in min_utc]))
        time_min_utc = air_temps_info.get('datetime_min_utc')
        time_min_utc = (''.join(time_min_utc))
        time_max_utc = air_temps_info.get('datetime_max_utc')
        time_max_utc = (''.join(time_max_utc))
        
        print(f'{stid},{station_name},{state},{lat},{lon},{el},{tz},{dates},{min_utc},{time_min_utc},{max_utc},{time_max_utc}', file = outfile)
        y +=1    
       

print()        
print(f'Wrote {y} stations to {full_file}')   
                 


# In[5]:


#
# Remove lines with missing data
#

lines = []
# read file
with open(full_file, 'r') as f:
    # read an store all lines into list
    lines = f.readlines()

# Write file
with open(full_file, 'w') as f:
    # iterate each line
    for line in lines:
          
        # condition for data to be deleted
        if 'None' not in line:
        #if line.strip("\n") != 'None': 
            f.write(line)            


# In[6]:


import os
import sys

#
# Read in the blacklist and remove those lines
#

values = []
lines = []

#Set the path and file name of the blacklist file
#Set the path to your installation directory

#
path_to_file = ('/Users/jameshayes/') # ***THIS NEEDS TO BE CHANGED***
name_of_file = ('blacklist.txt') # file containing the blacklisted files.
new_fileName = f'{path_to_file}{name_of_file}'

# read blacklist file

try:

    with open(new_fileName, 'r') as f:
        values = f.readlines()
        for i,n in enumerate(values):
            values[i] = n.strip("\n")          
        
except os.error as err:
       print(f"Unable to open {new_fileName}: {err}", file=sys.stderr)      
                                     
dummy_name = 'test1009.txt'
dummy_file = f'{path_to_file}{dummy_name}' 

#number of values
a = (len(values))
print(values)

#
# Set the values for checking in the loop
#

print(f'There are {a} members of the blacklist')
        
with open(full_file, 'r') as f:
        lines = f.readlines()
        print(f'read in the file {full_file}')
                  
with open(full_file, 'w') as fd:
         print(f'writing the file {full_file}')
         for line in lines:
                
                result = any(map(line.startswith, values))
                if result == False:
                    fd.writelines(line) 


# In[8]:


import datetime as datetime
from datetime import datetime  
from datetime import timezone

#
# Set up panda DataFrames parameters
# This is where the data is prepared for HTML presentation
# using pandas
#

#
# Determine the time
#

dt = (datetime.now(timezone.utc))
dt1 = ((dt.strftime("%m")) + "/" + (dt.strftime("%d") + "/" ) + (dt.strftime("%Y")))
dh = (dt.strftime("%H"))

compTime = dh
compTime = int(dh)


if compTime >= 0 and compTime < 1:
    timeUTC = "01z"
elif compTime >= 1 and compTime < 6:
    timeUTC = "06z"    
elif compTime >= 6 and compTime < 12:
    timeUTC = "12z"
elif compTime >= 12 and compTime < 13:
    timeUTC = "13z"
elif compTime >= 13 and compTime < 18:
    timeUTC = "18z"
elif compTime >= 18 and compTime < 24:
    timeUTC = "00z"
else:
    timeUTC = "00z"

print(compTime,timeUTC)
        
df = pd.read_csv(full_file, names = ['STID', 'Location', 'State','Lat', 'Lon', 'Elev','TZ','Date','LOW','Time_Min_UTC','HIGH', 'Time_Max_UTC'] )
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

#
# Set the path 
#
# This path is where you want to the created HTML files to reside. It is 
# different from the installation directory. Check with the webmaster 
# to fins the path to the coreect directory on your system
#

new_Path = ('/Users/jameshayes/') # ***THIS NEEDS TO BE CHANGED***

#
# Write the MAX html file first
#

ccc = (df.sort_values(by="HIGH", ascending=False))
cccc = ccc.round({"HIGH":0})
cccc.head(50).to_html(new_Path + 'Max' + '.html', index = False)

#
# Now write the MIN html file
#

ddd = (df.sort_values(by='LOW', ascending=True))
dddd = ddd.round({"LOW":0})
dddd.head(50).to_html(new_Path + 'Min' + '.html', index = False)


# In[ ]:




