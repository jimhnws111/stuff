#!/usr/bin/env python
# coding: utf-8

# In[178]:


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


# In[179]:


#
# reads in the JSON file as a Python dictionary
#

fr = open('/home/ec2-user/TEST996.json')
dataAPI = json.load(fr)


# In[180]:


'''
Some basic error checking to see if the Max/Min data is available
for each station, and adds a dummy value if it is not there
'''

x = 0
for data in dataAPI['STATION']:
    if 'MINMAX' in data:
        pass #print('It is here', x, data)
    else:
        print('it is NOT here', x, data)
        data['MINMAX'] = 'None','None','None','None','None'
        #print(data)
              
    x = x + 1 

#
# Set up filename
#

dt = (datetime.now(timezone.utc))
dt1 = ((dt.strftime("%m")) + "/" + (dt.strftime("%d") + "/" ) + (dt.strftime("%Y")))
dh = (dt.strftime("%H%M"))
print()
print(f"There are {x} observations at {dh} UTC on {dt1}") 
print()




#x = datetime.datetime.now()
#print(x)
path_to_file = ('/home/ec2-user/')
name_of_file = ('Updated_API_')
type_of_file = ('.txt')
file_time =(((dt.strftime("%Y")) + (dt.strftime("%m")) + (dt.strftime("%d")) + (dt.strftime("%H")) + (dt.strftime("%M"))))
file_name = ((path_to_file) + (name_of_file) + (file_time) + (type_of_file))
print(file_name)

#
# Write the text file
#

with open(file_name, 'w') as outfile:
    for data in dataAPI['STATION']:
        names = data['NAME'];names1 = names.rstrip();n = names.replace(',','')
        stid = data['STID'];stid1 = stid.rstrip()
        lat = data['LATITUDE'];lat1 = lat.rstrip()
        lon = data['LONGITUDE']; lon1 = lon.strip()
        minimaxi = data['MINMAX'];minmax1 = str(minimaxi);minmax2 = minmax1.replace('{','').replace('}','').replace('[','').replace(']','')
        minmax3 = minmax2.replace("'air_temp_value_1': ",'').replace("'dates': ",'')
        minmax4 = minmax3.replace(" 'datetime_min_utc':",'').replace(" 'value_min_utc':",'').replace(" 'dates':",'' )
        minmax5 = minmax4.replace(" 'value_max_utc':",'').replace(" 'datetime_max_utc':",'').replace(" 'datetime_timezone': 'utc',",'' )
        # split minmax5 for a more precise definition
        inter = minmax5.split(',')
        date_utc = inter[0]
        date_max_utc = inter[1]
        min_utc = inter[2]
        max_utc = inter[3]
        date_min_utc = inter[4]
        id = data['ID']; id1 = id.rstrip()
        obs = data['OBSERVATIONS']
        state = data['STATE'];state1 = state.rstrip()
        Ev = data['ELEVATION']
        if Ev == None: 
            Ev = "0"
        tz = data['TIMEZONE'];tz1 =tz.rstrip() 
        #print(stid1 + ",", n + ",", state1 + ",", lat1 + ",",lon1 + ",", Ev + ",", tz1 + ",", minmax5, file = outfile)      
        print(stid1 + ",", n + ",", state1 + ",", lat1 + ",",lon1 + ",", Ev + ",", tz1 + ",", date_utc + ",", min_utc + ",", date_min_utc + ",", max_utc + ",", date_max_utc, file = outfile)    
outfile.close()


# In[181]:


#
# Remove liens with missing data
#

lines = []
# read file
with open(file_name, 'r') as f:
    # read an store all lines into list
    lines = f.readlines()

# Write file
with open(file_name, 'w') as f:
    # iterate each line
    for line in lines:
          
        # condition for data to be deleted
        if 'None' not in line:
        #if line.strip("\n") != 'None': 
            f.write(line)            


# In[182]:


#
# Read in the blacklist and remove those lines
#

values = []
lines = []

import os
import sys

#Set the path and file name of the blacklist file

path_to_file = ('/home/ec2-user/')
name_of_file = ('blacklist.txt')

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
        
with open(file_name, 'r') as f:
        lines = f.readlines()
        print(f'read in the file {file_name}')
                  
with open(file_name, 'w') as fd:
         print(f'writing the file {file_name}')
         for line in lines:
                
                result = any(map(line.startswith, values))
                if result == False:
                    fd.writelines(line) 


# In[183]:


#
# Set up panda DataFrames parameters
#

#
# Determine the time
#

import datetime as datetime
from datetime import datetime  
from datetime import timezone

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
        
df = pd.read_csv(file_name, names = ['STID', 'Location', 'State','Lat', 'Lon', 'Elev','TZ','Date','LOW','Time_Min_UTC','HIGH', 'Time_Max_UTC'] )
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

#
# Set the path 
#

new_Path = ('/home/ec2-user/')

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

#
# Create a csv file for plotting
#

df2 = pd.DataFrame().assign(STID=df['STID'], HIGH=df['HIGH'])
df3 = pd.DataFrame().assign(STID=df['STID'], LOW=df['LOW'])

#
# Write the MAX csv file first
#

eee = (df2.sort_values(by="HIGH", ascending=False))
eeee = eee.round({"HIGH":0})
eeee = eee.round(0)
eeee.head(50).to_csv(new_Path + 'Max' + '_' + timeUTC + '.csv', index = False)

#
# Now write the MIN csv file
#

fff = (df3.sort_values(by='LOW', ascending=True))
ffff = fff.round({"LOW":0})
ffff = fff.round(0)
ffff.head(50).to_csv(new_Path + 'Min' + '_' + timeUTC + '.csv', index = False)


# In[76]:


# 
# Investigate the feasibility of comparing highs - 00z vs 01z
#

#df5 = pd.read_csv(f'{new_Path}Max_01z.csv')
#df6 = pd.read_csv(f'{new_Path}Max_00z.csv')

#newdf = df5.merge(df6, on=['STID'], how='left')
#bool_series = pd.isnull(newdf["HIGH_y"])
#df7 = newdf[bool_series]

#dFinal = df7.drop(['HIGH_x', 'HIGH_y'], axis=1)
#dFinal = dFinal.iloc[1: , :]
#dFinal.to_csv(f'{new_Path}01z_highSort.csv',index = False)
    
#with open(f'{new_Path}01z_highSort.csv', 'r') as f:
#        sta = f.readlines()
#        for i,n in enumerate(sta):
#            sta[i] = n.strip("\n")      


# In[185]:


# 
# Investigate the feasibility of comparing lows - 12z vs 13z
#

df5 = pd.read_csv(f'{new_Path}Min_12z.csv')
df6 = pd.read_csv(f'{new_Path}Min_13z.csv')

newdf = df5.merge(df6, on=['STID'], how='left')
bool_series = pd.isnull(newdf["LOW_y"])
df7 = newdf[bool_series]

dFinal = df7.drop(['LOW_x', 'LOW_y'], axis=1)
#dFinal = dFinal.iloc[1: , :]
dFinal.to_csv(f'{new_Path}13z_lowSort.csv',index = False)
    
with open(f'{new_Path}13z_lowSort.csv', 'r') as f:
        sta = f.readlines()
        for i,n in enumerate(sta):
            sta[i] = n.strip("\n")      


# In[78]:


'''
import datetime as datetime
from datetime import datetime  
from datetime import timezone

dt = (datetime.now(timezone.utc))
dt1 = ((dt.strftime("%m")) + "/" + (dt.strftime("%d") + "/" ) + (dt.strftime("%Y")))
dh = (dt.strftime("%H"))

yy = (dt.strftime("%Y"))
mm = (dt.strftime("%m"))
dd = (dt.strftime("%d"))

pref = "Updated_API_"
statTime = "1156"
suff = ".txt"

new_Path = ('/Users/jameshayes/')
New_Filename = (f'{new_Path}{pref}{yy}{mm}{dd}{statTime}{suff}')
test_File = (f'{new_Path}{pref}{yy}{mm}11{statTime}{suff}')
add_on_file = (f'{new_Path}add_on.txt')
print(sta)

with open(test_File, 'r') as f:
        lines = f.readlines()
        print(f'Read in the file {test_File}')
                  
with open(add_on_file, 'w') as fd:
         print(f'Writing the file {add_on_file}')
         for line in lines:
                                
                result = any(map(line.startswith, sta))
                if result == True:
                    fd.writelines(line) 
'''                    


# In[177]:


'''
# Compare low temperature files for changes

file1=(f'{new_Path}Updated_API_202210141156.txt')
file2=(f'{new_Path}Updated_API_202210141216.txt')    
df8=pd.read_csv(file1, names = ['STID', 'Location', 'State','Lat', 'Lon', 'Elev','TZ','Date','LOW','Time_Min_UTC','HIGH', 'Time_Max_UTC'] )
df8.columns =['STID', 'Location', 'State','Lat', 'Lon', 'Elev','TZ','Date','LOW','Time_Min_UTC','HIGH', 'Time_Max_UTC']
df9=pd.read_csv(file2, names = ['STID', 'Location', 'State','Lat', 'Lon', 'Elev','TZ','Date','LOW','Time_Min_UTC','HIGH', 'Time_Max_UTC'] )
df9.columns =['STID', 'Location', 'State','Lat', 'Lon', 'Elev','TZ','Date','LOW','Time_Min_UTC','HIGH', 'Time_Max_UTC']

k10=(df8['STID'],df8['LOW'])
df10 = pd.DataFrame(k10)
k11=(df9['STID'],df9['LOW'])
df11 = pd.DataFrame(k11)


#on=['STID'], how='left')
#frames = [df10, df11]
#result = pd.concat(frames, axis=1)
#display(result)
'''


# In[ ]:




