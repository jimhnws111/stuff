#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re

def getLatLon(str1):

    LatLon = re.search('LAT...LON.*', str1, re.M|re.S)
    if LatLon:
        print(LatLon.group(0))
        LatLon1 = LatLon.group(0) 
        
    return(LatLon1)    

