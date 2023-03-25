#!/usr/bin/env python
# coding: utf-8

# In[32]:


import datetime
import time
from datetime import datetime

def calcTimeStamp():
    now = datetime.now()
    dayOfMonth = int(now.strftime("%d"))
    month = int(now.strftime("%m"))
    year = int(now.strftime("%Y"))
    start = datetime(year, month, dayOfMonth).strftime("%s") 
    end = round(time.time())
    
    return(start,end)

