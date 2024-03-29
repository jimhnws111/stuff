#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime
from datetime import datetime
import dataFile
import getNameNumbers
import requests
import getData

#
# Get the start and end times, depending on product
#

def reckonTime():
    
    """Make sure the proper version of dataFromTempest
    is executed at the proper time"""

    now = datetime.now()
    x = now.strftime("%Y-%m-%d")
    print("This script started at:", now)

    t1 = ' 21:00'
    t2 = ' 22:00'
    time1 = x + t1
    time2 = x + t2
    val1 = datetime.strptime(time1, "%Y-%m-%d %H:%M")
    val2 = datetime.strptime(time2, "%Y-%m-%d %H:%M")

    if val1 < now < val2:
        end = int(datetime.timestamp(now))
        start = (end - 55800)
        st = datetime.fromtimestamp(start)
        en = datetime.fromtimestamp(end)
        start = str(start)
        end = str(end)   
        
        return(start, end, st, en)    
        
    else:
        startEnd = getData.getData()
        start, end = startEnd[0], startEnd[1]  
        print("Made it here imstead")
    
        return(start, end)
    
reckonTime()  

