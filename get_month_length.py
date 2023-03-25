#!/usr/bin/env python
# coding: utf-8

# In[28]:


def get_month_length(month_number_UTC, year_UTC):
      
    if (year % 400 == 0):
        leap_year = True
    elif (year % 100 == 0):
        leap_year = False
    elif (year % 4 == 0):
        leap_year = True
    else:
        leap_year = False  
        
        
    if month_number_UTC in (1, 3, 5, 7, 8, 10, 12):
        month_length = 31
    elif month_number_UTC == 2:
        if leap_year:
            month_length = 29
        else:
            month_length = 28
    else:
        month_length = 30
        
    print(month_number_UTC)
    
    return month_length


# In[ ]:





# In[ ]:





# In[ ]:




