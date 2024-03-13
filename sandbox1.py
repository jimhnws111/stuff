#!/usr/bin/env python
# coding: utf-8

# In[48]:


import sandbox2
import logging

'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('/home/ec2-user/sandbox1.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
'''

def recordHigh():
    
    results = sandbox2.sandbox2()
    result1 = results[0]
    recYearNum = len(result1)
        
    if recYearNum > 1 and recYearNum < 4:
        recHigh = (result1[0][1])
        recHigh = int(recHigh)
        i = 0 
        years = []
        while i < recYearNum:
            years.append(str(result1[i][4]))
            i+= 1
        
        years.reverse()            
    
        if recYearNum == 2:
            ax = (years[recYearNum - 2])
            ax = float(ax)
            ax = int(ax);print(ax)
            bx = (years[recYearNum - 1])
            bx = float(bx)
            bx = int(bx);print(bx)
            yearx = (f'{ax} and {bx}')
            highPhrase = (f'The record high for today is {recHigh} set in {yearx}')
        elif recYearNum == 3:
            ax = years[recYearNum - 3]
            bx = years[recYearNum - 2]
            cx = years[recYearNum - 1 ]
            yearx = (f'{ax}, {bx} and {cx}')
            highPhrase = (f'The record high for today is {recHigh} set in {yearx}')
        elif recYearNum == 4:
            ax = years[recYearNum - 4]
            bx = years[recYearNum - 3]
            cx = years[recYearNum - 2 ]
            dx =  years[recYearNum - 1 ]
            yearx = (f'{ax}, {bx}, {cx} and {dx}')
            highPhrase = (f'The record high for today is {recHigh} set in {yearx}')
        return(recHigh, yearx, highPhrase)
                
    if recYearNum == 1:
        recHigh1 = (result1[0])
        recHigh = int(recHigh1[1])
        year1x = (result1[0])
        yearx = int(year1x[4])
        highPhrase = (f'The record high for today is {recHigh} set in {yearx}')
        
    return(recHigh, yearx, highPhrase)         


# In[49]:


recordHigh()


# In[50]:


import sandbox2
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

'''
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('/home/ec2-user/sandbox1.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
'''

def recordLow():
    
    results = sandbox2.sandbox2()
    result2 = results[1]
        
    recYearNum = len(result2)        
    
    if recYearNum == 1:
        recLow = (result2[0][1])
        yearx =  (result2[0][4])
        lowPhrase = (f'The record low for today is {recLow} set in {yearx}')   
        
        return(recLow, yearx, lowPhrase)        
    
    if recYearNum > 1 and recYearNum < 4:
        recLow = (result2[0][1])
        i = 0 
        years = []
        while i < recYearNum:
            years.append(str(result2[i][4]))
            i+= 1
        
        years.reverse()
    
    if recYearNum == 2:
        recLow = (result2[0][1])
        logger.info(recLow)
        ax = years[recYearNum - 2]
        bx = years[recYearNum - 1]
        yearx = (f'{ax} and {bx}')
        lowPhrase = (f'The record low for today is {recLow} set in {yearx}')
        
        return(recLow, yearx, lowPhrase)   
            
    if recYearNum == 3:
        recLow = (result2[0][1])
        ax = years[recYearNum - 3]
        bx = years[recYearNum - 2]
        cx = years[recYearNum - 1 ]
        yearx = (f'{ax}, {bx} and {cx}')
        lowPhrase = (f'The record low for today is {recLow} set in {yearx}')
        
        return(recLow, yearx, lowPhrase)   
            
    if recYearNum == 4:
        recLow = (result2[0][1])
        ax = years[recYearNum - 4]
        bx = years[recYearNum - 3]
        cx = years[recYearNum - 2 ]
        dx =  years[recYearNum - 1 ]
        yearx = (f'{ax}, {bx}, {cx} and {dx}')
        lowPhrase = (f'The record low for today is {recLow} set in {yearx}')
        
        return(recLow, yearx, lowPhrase)            
    


# In[51]:


recordLow()


# In[53]:


import sandbox2
import logging 

'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('/home/ec2-user/sandbox1.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
'''

def recordRain():
    
    results = sandbox2.sandbox2()
    result3 = results[2]       
    
    recYearNum = len(result3)
    recRain = (result3[0][1])
    print(recYearNum)
                    
    if recYearNum > 1 and recYearNum < 4:
        recRain = (result3[0][1])
        i = 0 
        years = []
        while i < recYearNum:
            years.append(str(result3[i][4]))
            i+= 1
        
        years.reverse()
    
    if recYearNum == 2:
        recRain = (result3[0][1])
        ax = years[recYearNum - 2]
        bx = years[recYearNum - 1]
        yearx = (f'{ax} and {bx}')
        rainPhrase = (f'The record rainfall for today is {("%.2f" % recRain)} inches set in {yearx}')
        logging.debug(f'Rain Phrase is: {rainPhrase}')
        
        return(recRain, yearx, rainPhrase)   
        
    if recYearNum == 3:
        recRain = (result3[0][1])
        ax = years[recYearNum - 3]
        bx = years[recYearNum - 2]
        cx = years[recYearNum - 1 ]
        yearx = (f'{ax}, {bx} and {cx}')
        rainPhrase = (f'The record rainfall for today is {("%.2f" % recRain)} inches set in {yearx}')
        logging.debug(f'Rain Phrase is: {rainPhrase}')
        
        return(recRain, yearx, rainPhrase)   
        
    if recYearNum == 4:
        recRain = (result3[0][1])
        ax = years[recYearNum - 4]
        bx = years[recYearNum - 3]
        cx = years[recYearNum - 2 ]
        dx =  years[recYearNum - 1 ]
        yearx = (f'{ax}, {bx}, {cx} and {dx}')
        rainPhrase = (f'The record rainfall for today is {("%.2f" % recRain)} inches set in {yearx}')
        logging.debug(f'Rain Phrase is: {rainPhrase}')
        
        return(recRain, yearx, rainPhrase)      

        
    if recYearNum == 1:
        recRain = (result3[0][1])
        yearx = (result3[0][4])
        print(yearx)
        rainPhrase = (f'The record rainfall for today is {("%.2f" % recRain)} inches set in {yearx}')
        logging.debug(f'Rain Phrase is: {rainPhrase}')
        
        return(recRain, yearx, rainPhrase)   


# In[54]:


recordRain()


# In[ ]:





# In[ ]:




