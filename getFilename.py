#!/usr/bin/env python
# coding: utf-8

# In[8]:


def getFilename():
    
    import datetime
    from datetime import date
    from datetime import datetime, time, timedelta
    import calendar, month_Days
    import excelFilename    
       
    tdy = date.today()
    year, month, day = tdy.year, tdy.month, tdy.day
    print(day)
    month_name = calendar.month_name[month]
    days_in_month = month_Days.days_in_month(year,month) 
     
    sa1 = excelFilename.wxflow()
    xls_filename, path_name = (sa1[0], sa1[1])
    xls_fullfile = (f'{path_name}{xls_filename}')
               
    e = ['January', 'March', 'May', 'July', 'August', 'October', 'December']
    f = ['April', 'June', 'September', 'November']
    g = ['February']  
    
    return(day)

