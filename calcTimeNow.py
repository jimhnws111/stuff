#!/usr/bin/env python
# coding: utf-8

# In[14]:


import datetime as datetime
from datetime import datetime

def calcTimeNow():
    now = datetime.now()
    myMonth = now.strftime("%b")
    numMonth = now.strftime("%m")
    myYear = now.strftime("%Y")
    date = now.strftime("%d")              
    return(now,myMonth,myYear,date,numMonth)

def calcMonthNow():
    now = datetime.now()
    month_name = now.strftime("%B")
    
    return(month_name)


# In[15]:


calcTimeNow()


# In[ ]:




