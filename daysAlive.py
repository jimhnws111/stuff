#!/usr/bin/env python
# coding: utf-8

# In[30]:


import datetime
from datetime import timedelta

def daysAlive(year,month,day):

    dayBorn = datetime.date(year,month,day)
    tday = datetime.date.today()
    numDays = tday - dayBorn
    
    return(numDays)

