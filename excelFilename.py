#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
from datetime import datetime

def wxflow():
    now = datetime.now()
    myMonth = now.strftime("%B")
    myYear = now.strftime("%Y")
    path_name = '/Users/jameshayes/'
    platform = "Tempest"
    xls_suffix = '.xlsx'
    xls_filename = f'{myMonth}_{myYear}_{platform}{xls_suffix}'
   
    return(xls_filename, path_name)


# In[ ]:


import datetime
from datetime import datetime

def tempest_ec2():
    now = datetime.now()
    myMonth = now.strftime("%B")
    myYear = now.strftime("%Y")
    path_name = '/home/ec2-user/'
    platform = "Tempest"
    xls_suffix = '.xlsx'
    xls_filename = f'{myMonth}_{myYear}_{platform}{xls_suffix}'
   
    return(xls_filename, path_name)


# In[2]:


import datetime
from datetime import datetime

def davis():
    now = datetime.now()
    myMonth = now.strftime("%B")
    myYear = now.strftime("%Y")
    path_name = '/home/ec2-user/'
    platform = "Davis"
    xls_suffix = '.xlsx'
    xls_filename = f'{myMonth}_{myYear}_{platform}{xls_suffix}'
   
    return(xls_filename, path_name)

