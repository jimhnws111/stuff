#!/usr/bin/env python
# coding: utf-8

# In[33]:


from datetime import datetime, timedelta
import calcOneDay
import getDays
import calendar

def daysAndDatesNew():

    # Calculate the time and date for end of day calculations

    xy = calcOneDay.calcOneDay()
    start, end = (xy[0], xy[1])

    todayInfo = getDays.getToday()
    day = int(todayInfo[2])
    yesterdayInfo = getDays.getYesterday()
    print(yesterdayInfo)
    
    tomorrowInfo = getDays.getTomorrow()  
                    
    if day == 1:
        yesterday = int(yesterdayInfo[2])
        nextDay = (int(tomorrowInfo[2]))
        month, month_num, date, year = yesterdayInfo[0], yesterdayInfo[1], yesterdayInfo[2], yesterdayInfo[3]
        month_num1 = int(month_num)
        nextMonth_num = month_num1 + 1
        nextMonth = (calendar.month_name[nextMonth_num])           
        
        return(month, month_num, date, year, yesterday, nextDay, nextMonth)             
            
    else:
        yesterday = int(yesterdayInfo[2])
        nextDay = int(tomorrowInfo[2])
        month, month_num, date, year = todayInfo[0], todayInfo[1], todayInfo[2], todayInfo[3]   
              
        return(month, month_num, date, year, yesterday, nextDay)


# In[34]:


daysAndDatesNew()


# In[ ]:





# In[ ]:





# In[ ]:




