#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re

def getWFOs(str1):

    WFOwfo = re.search('ATTN...WFO.*', str1, re.M)
    if WFOwfo:
       #print WFOwfo.group(0)
       WFOwfo1 = WFOwfo.group(0)
                     
    WFOs = WFOwfo1[13:]
    #print WFOs
    MetWFO = WFOs[:-3]
    #print MetWFO
    FinalWFO = re.sub('\...',' ', MetWFO)
    print("The final WFO list is ", FinalWFO)
    
    return(FinalWFO)

