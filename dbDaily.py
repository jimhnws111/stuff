#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from pandas import DataFrame
import os
import calendar
from pretty_html_table import build_table
import sys
import json
from pandas import json_normalize

#
# Read in file with user request for monthly data
#

colNames = ['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall']
df = pd.read_json('/var/www/html/000/daily.txt')
#df = pd.read_json('/Users/jameshayes/monthly.txt')
df = df.drop(df.columns[[0, 10]], axis=1)
print(df)

html_table_blue_light = build_table(df, 'blue_light')

with open('/var/www/html/000/dailyTable.html', 'w') as f:
#with open('/Users/jameshayes/monthlyTable.html', 'w') as f: 
    f.write(html_table_blue_light)

