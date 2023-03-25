#!/usr/bin/env python
# coding: utf-8

# In[5]:


import datetime
from datetime import datetime

def dataFile_mac():
    now = datetime.now()
    date = now.strftime("%d") 
    myMonth = now.strftime("%B")
    myMonthNum = now.strftime("%m")
    myYear = now.strftime("%Y")
    addTo = f'_{myYear}{myMonthNum}{date}'

    path_name = '/Users/jameshayes/'
    file_name = f'Tempest{addTo}.csv'
    full_file = (f'{path_name}{file_name}')
    
    return(full_file)
    
def dataFile_ec2():
    now = datetime.now()
    date = now.strftime("%d") 
    myMonth = now.strftime("%B")
    myMonthNum = now.strftime("%m")
    myYear = now.strftime("%Y")
    addTo = f'_{myYear}{myMonthNum}{date}'

    path_name = '/home/ec2-user/'
    file_name = f'Davis{addTo}.csv'
    full_file = (f'{path_name}{file_name}')
    
    return(full_file)

def dataFile_wxflow():
    now = datetime.now()
    date = now.strftime("%d") 
    myMonth = now.strftime("%B")
    myMonthNum = now.strftime("%m")
    myYear = now.strftime("%Y")
    addTo = f'_{myYear}{myMonthNum}{date}'

    path_name = '/home/ec2-user/'
    file_name = f'Tempest{addTo}.csv'
    full_file = (f'{path_name}{file_name}')
    
    return(full_file)


# In[6]:


dataFile_wxflow()


# In[ ]:




