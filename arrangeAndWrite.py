#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import daysAndDatesNew

def arrangeAndWrite():     
    
    """Rearrange the dataframe to make a bit more sense and add a couple of elements"""
    
    dayInfo = daysAndDatesNew.daysAndDatesNew()
    month, month_num, date, year, yesterday = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3], dayInfo[4]
    yesterday = int(dayInfo[4])
    f6data = createF6(df)
    maxT, minT, dewMaxT, dewMinT, rain, avgTemp, hdd, cdd = f6data[0], f6data[1], f6data[2], f6data[3], f6data[4], f6data[5], f6data[6], f6data[7] 
 
    df2 = pd.DataFrame(columns = ['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
    newRow = pd.DataFrame({'Year': year, 'Month': month_num, 'Date': yesterday, 'High': maxT, 'Low': minT, 'Average': avgTemp, 'HDD': hdd, 'CDD': cdd, 'Rainfall' : rain, 'Max_Dew_Point': dewMaxT }, index = [yesterday])
    df2 = pd.concat([newRow, df2]).reset_index(drop = True)    
        
    return(df2)

