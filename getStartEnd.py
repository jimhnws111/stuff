#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
from datetime import datetime
import requests
import json
import dataFile
import getData
import checkDST

def getStartEnd():

    """Get the start and end times, depending on product"""

    now = datetime.now()
    x = now.strftime("%Y-%m-%d")
    print("FUCK!", now)
    print("This is the time of x: ", x)

    t1 = ' 20:00'
    t2 = ' 21:00'
    time1 = x + t1
    time2 = x + t2
    print("These are the time values", time1, time2)
    val1 = datetime.strptime(time1, "%Y-%m-%d %H:%M")
    val2 = datetime.strptime(time2, "%Y-%m-%d %H:%M")
    print(val1, val2)

    if val1 < now < val2:
        end = int(datetime.timestamp(now))
        start = (end - 59400)
        start = str(start)
        end = str(end) 
        print("Chose this one")

    else:
        startEnd = getData.getData()
        start, end = startEnd[0], startEnd[1] 
        start = str(start)
        end = str(end) 
        print("Nope. Chose this one instead")  
    
    return(start, end)

