#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

df1 = pd.read_csv('/home/ec2-user/HiLoRain.csv', names = ['High','Low','Rainfall', 'Hourly Rate', 'Fake Rain','Tstorm?','Time'], index_col = False)
df1['Platform'] = 'Davis'
df2 = pd.read_csv('/home/ec2-user/HiLoRain_tempest.csv', names = ['High','Low','Rainfall','Hourly Rate', 'Fake Rain','Tstorm?','Time'], index_col = False)
df2['Platform'] = 'Tempest'
pd.set_option('display.precision', 2)
pd.set_option('display.colheader_justify', 'center')
df3 = pd.concat([df1,df2])
df3.to_html('/var/www/html/000/together.html', index = False)  

