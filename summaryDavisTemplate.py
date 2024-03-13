#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd

df1 = pd.read_csv('/Users/jameshayes/Sites/HiLoRain.csv', names = ['High','Low','Rainfall','Time'], index_col = False)
df1['Platform'] = 'Davis'
df2 = pd.read_csv('/Users/jameshayes/Sites/HiLoRain_tempest.csv', names = ['High','Low','Rainfall','Time'], index_col = False)
df2['Platform'] = 'Tempest'
pd.set_option('display.precision', 2)
pd.set_option('display.colheader_justify', 'center')
df3 = pd.concat([df1,df2])
df3.to_html('/Users/jameshayes/Sites/together.html', index = False)  


# In[ ]:




