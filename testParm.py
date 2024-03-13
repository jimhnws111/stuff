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

assInput = json.loads(sys.argv[1])
getInput = json.dumps(assInput)

colNames = ['Rainfall', 'High', 'Low', 'Year', 'Month', 'Day']
#df = pd.read_json('/var/www/html/000/monthly.txt')
#df = pd.read_json('/Users/jameshayes/monthly.txt')
#df = df.drop(df.columns[[0]], axis=1)
#print(df)

#html_table_blue_light = build_table(df, 'blue_light')

#with open('/var/www/html/000/monthlyTable.html', 'w') as f:
#with open('/Users/jameshayes/monthlyTable.html', 'w') as f: 
#    f.write(html_table_blue_light)

#
# Get month name from the month number and year
#

#xd = (df.loc[df['Month']].values[0])
#sd = (df.loc[df['Month']].values[0])
#print(sd)

#month_num = int(xd[4])
#month_name = calendar.month_name[month_num]
#year = int(sd[3])
#print(month_num, month_name, year)

