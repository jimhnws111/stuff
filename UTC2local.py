#!/usr/bin/env python
# coding: utf-8

# In[11]:


import datetime
import time
from datetime import datetime, date
from dateutil.tz import tzutc, tzlocal
import pytz
import checkDST

def UTC2local():
    timezone = pytz.timezone("America/New_York")
    now = int(time.time())
    dt_object = datetime.fromtimestamp(now)
    localT = dt_object.astimezone(timezone)
    mm,ss = 0,0
    
    # Check DST setting
    #isDST = checkDST.checkDST()
    
    #if isDST == 1:
    start = int(datetime(localT.year, localT.month, localT.day, mm, ss).strftime("%s"))
    start = start + 14400 # DST time offset
    end = round(time.time())
        
    return(start,end)
    
    #else:
    #    start = int(datetime(localT.year, localT.month, localT.day, mm, ss).strftime("%s"))
    #    start = start + 18000 #standard time offset
    #    end = round(time.time())
        
    #    return(start,end)


# In[12]:


UTC2local()


# In[ ]:




