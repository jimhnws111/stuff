#!/usr/bin/env python
# coding: utf-8

# In[2]:


import re

def getFloodType(str1):

    x11 = re.search('Concerning.*', str1)
    if x11:
        x12 = x11.group(0)
        pat = re.compile('possible|likely')
        x13 = re.search(pat, x12)
        
        if x13 is None:
            floodtype = "none"
            print('The flood type is', floodtype)
        
        if x13:
            print(x13.group(0))
            flood = x13.group(0)
            floodtype = flood
            print('The flood type is', floodtype)
                
        return(floodtype)          


# In[ ]:




