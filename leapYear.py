#!/usr/bin/env python
# coding: utf-8

# In[14]:


def leapYear(year):

    if (year % 400 == 0):
        leap_year = True
    elif (year % 100 == 0):
        leap_year = False
    elif (year % 4 == 0):
        leap_year = True
    else:
        leap_year = False
        
    return leap_year    


# In[ ]:




