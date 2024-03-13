#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
import glob

files = glob.glob('*temps_????.png')

count = 0
for x in files:
    prefix = x[0:3]
    suffix = x[-4:]
    year = x[-8:-4]
    newNameTemps = f'{prefix}{year}Temps{suffix}'
    os.rename(x, newNameTemps)
    

#for x in os.listdir():
#    if x.endswith(".png"):
#        # Prints only text file present in My Folder
#        print(x)



# In[ ]:




