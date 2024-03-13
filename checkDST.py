#!/usr/bin/env python
# coding: utf-8

# In[30]:


from datetime import datetime
import time

def checkDST():

    #
    # Calculate the current time
    # and convert to datetime
    #

    ts = time.time()
    ts = (int(ts))
    setTime = datetime.fromtimestamp(ts)

    #
    # Set the time changes in datetime format
    # and compare today to those dates
    #

    est2edt = '2024-03-10 06:00:00'
    est2EDT = datetime.strptime(est2edt, '%Y-%m-%d %H:%M:%S')
    edt2est = '2024-11-03 06:00:00'
    edt2EST = datetime.strptime(edt2est, '%Y-%m-%d %H:%M:%S')

    if est2EDT < setTime < edt2EST:
        isDST = 1
    else:
        isDST = 0
    
    return (isDST)


# In[ ]:




