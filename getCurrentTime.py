#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime as datetime

# Read the Excel file as a possible pandas dataframe and html file

now = datetime.datetime.now()
myMonth = now.strftime("%B")
myYear = now.strftime("%Y")

print(now)

