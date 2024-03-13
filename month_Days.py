#!/usr/bin/env python
# coding: utf-8

# In[17]:


month_days = [0,31,28,31,30,31,30,31,31,30,31,30,31]


# In[18]:


def is_leap(year):
    return year%4 == 0 and (year%100 !=0 or year%400 == 0)


# In[19]:


def days_in_month(year,month):
    if not 1 <= month <= 12:
        return 'Invalid month'
    
    if month == 2 and is_leap(year):
        return 29
    
    return month_days[month]
