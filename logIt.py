#!/usr/bin/env python
# coding: utf-8

# In[6]:


import logging
import os

#
# Set up some logging
#

def logIt():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler('/home/ec2-user/davisCompleteTest.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


# In[ ]:




