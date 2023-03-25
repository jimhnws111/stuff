#!/usr/bin/env python
# coding: utf-8

# In[17]:


import datetime as datetime
from datetime import datetime

def calcTimeNow():
    now = datetime.now()
    myMonth = now.strftime("%b")
    myYear = now.strftime("%Y")
    date = now.strftime("%d")
            
    return(now,myMonth,myYear,date)

