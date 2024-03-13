#!/usr/bin/env python
# coding: utf-8

# In[11]:


import calcTimeNow

def getDaysInMonth():
    
    xr = calcTimeNow.calcTimeNow()
    month_name = calcTimeNow.calcMonthNow()
    year, date = xr[2],xr[3]
    year = int(year)

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
 
    if month_name in month31:
        r = 31
    elif month_name in month30:
        r = 30 
    elif month_name in month28:
        if leap_year:
            r = 29
        else:
            r = 28
    else:
        r = 31           
        
    return(r)    

