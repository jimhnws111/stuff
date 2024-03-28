#!/usr/bin/env python
# coding: utf-8

# In[5]:


import datetime
from datetime import datetime
import dataFile
import getNameNumbers
import requests
import getData

#
# Get the start and end times, depending on product
#

now = datetime.now()
x = now.strftime("%Y-%m-%d")
print("This script started at:", now)

t1 = ' 20:00'
t2 = ' 21:00'
time1 = x + t1
time2 = x + t2
val1 = datetime.strptime(time1, "%Y-%m-%d %H:%M")
val2 = datetime.strptime(time2, "%Y-%m-%d %H:%M")

if val1 < now < val2:
    end = int(datetime.timestamp(now))
    start = (end - 55800)
    start = str(start)
    end = str(end)    
        
else:
    startEnd = getData.getData()
    start, end = startEnd[0], startEnd[1]   
    
print(start, end)    

def dataFromTempest():
    
    """Create information to retrieve info from the Tempest API"""

    token = '877f6425-04a5-4f33-86e7-7123b7ef53d9'
    protocol = 'https://'
    urlSiteDevice = 'swd.weatherflow.com/swd/rest/observations/device/'
    urlSiteStation = 'swd.weatherflow.com/swd/rest/observations/station/'
    deviceID = '246921'
    stationID = '95775'
    preToken = '&token='
    preStart = '?time_start='
    preEnd = '&time_end='
    start_time = start
    end_time = end
    dayOffset = '&day_offset=1'
    format1 = '&format=csv'

    #
    # Put it together
    # 

    goGetDeviceSummary = (f'{protocol}{urlSiteDevice}{deviceID}{preStart}{start_time}{preEnd}{end_time}{format1}{preToken}{token}')
    r =  requests.get(goGetDeviceSummary)

    #path = '/home/ec2-user/'
    path = '/Users/jameshayes/'
    file_name = 'tempest_temp.csv'
    full_file = f'{path}{file_name}'

    with open(full_file,'w') as fd:
         fd.write(r.text)         
            
dataFromTempest()            


# In[ ]:




