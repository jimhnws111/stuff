#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def NoDaysInMonth(month,year): 
  
    months = ['January','February', 'March','April','May','June','July','August','September','October','November','December']

    if (year % 400 == 0):
        leap_year = True
    elif (year % 100 == 0):
        leap_year = False
    elif (year % 4 == 0):
        leap_year = True
    else:
        leap_year = False

    month31 = ['January','March', 'May', 'July', 'August', 'October', 'December']
    month30 = ['April', 'June', 'September', 'November']
    month28 = ['February']
 
    if month in month31:
        r = 31
    elif month in month30:
        r = 30 
    elif month in month28:
        if leap_year:
            r = 29
        else:
            r = 28
    else:
        r = 31           
        
    return(r)    

