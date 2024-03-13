#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import urllib
import requests
import os
import datetime
from datetime import datetime
import time
import checkDST
    
# Define some variables, includ states for auditing 
states = ['PA','NJ']
file_path = '/var/www/html/000/' 
#file_path = '/Users/jameshayes/Sites/'

# Loop through the states in the list           
for y in states:
    urlTest = f'https://api.weather.gov/alerts/active?area={y}'
    print(f'Retrieving active alerts for {y}...\n')
    r =  requests.get(urlTest)
    r.encoding = 'utf-8'
    x = r.json()
                              
    data = x['features']
    w = len(data)
    
    file_name = (f'alerts{y}.txt')
    full_filename = (f'{file_path}{file_name}')
    
    # Delete the previous alert.txt file..
    if os.path.exists(full_filename):
          os.remove(full_filename)
    else:
          print("The file does not exist")

                                                                                                                                
    if w <= 0:
        print(f'There are no watches/warnings/advisories in effect for {y}')
        print('\n')
        with open(full_filename, 'w') as outfile:   
             print(f'There are no watches/warnings/advisories in effect for {y}', file = outfile)
        continue
                
    j=0
    while j < w:
        
        
                
        q = (data[j]) 
        #print(j,q)
        id = q['properties']
        areaDesc = id['areaDesc']
        areaDesc = areaDesc.replace(";","")
        geocode = id['geocode']
        affectedZones = id['affectedZones']
        references = id['references']
        parameters = id['parameters']
        sent = id['sent']
        effective = id['effective']
        onset = id['onset']
        expires = id['expires']
        ends = id['ends']
        #print(j,w,expires)
       
        if ends is None:
            ends = id['expires']
           
                   
        status = id['status']
        messageType = id['messageType']
        category = id['category']
        severity = id['severity']
        urgency = id['urgency']
        event = id['event']
                                   
        sender = id['sender']
        senderName = id['senderName']
        headline = id['headline']
        description = id['description']
        instruction =id['instruction']
        parameters = id['parameters']
        #vtec = parameters['VTEC']
        for VTEC in id['parameters']:
            if 'VTEC' in parameters:
                pass
            else:
                id['VTEC'] = 'Missing'  
                 
                                      
        # Putting together the time parameters - first start time
        yearOnset = int(onset[:4])
        monthOnset = int(onset[5:7])
        dayOnset = int(onset[8:10])
        timeOnset = onset[11:16]
        hourOnset = int(timeOnset[0:2])         
        
        if hourOnset in range(1,12):  
            print(f' 1-12 This is the hourOnset for this example: {hourOnset}')
            xx = 'AM'
            
        if hourOnset in range(12,24):
            if hourOnset == 12:
                hourOnset = 12
            else:
                hourOnset = hourOnset - 12
            print(f'12-24 This is the hourOnset for this example: {hourOnset}')
            xx = "PM"
            
        if hourOnset == 0:
            hourOnset = 12
            print("As it turns out, I am here", y)
            print(f'This is the hourOnset for this example: {hourOnset}')
            xx = 'AM'
            
                
        minuteOnset = (timeOnset[3:5])
        minOnset = int(timeOnset[3:5])  
        newOnset = (str(hourOnset) + minuteOnset)
        startTime = datetime(yearOnset,monthOnset,dayOnset,hourOnset,minOnset)
        startTimeEpoch = round(startTime.timestamp())     
                   
        # Now the stop time    
        UTC_offset = (ends[-5:])
        UTC_offset = int(UTC_offset[:2])
        yearEnds = int(ends[:4])
        monthEnds = int(ends[5:7])
        dayEnds = int(ends[8:10])
        timeEnds = ends[11:16]
        hourEnds = int(timeEnds[0:2]) 
                                            
        if hourEnds in range(1,12):    
            xxE = 'AM'
        
        if hourEnds in range(12,24):
            hourEnds = hourEnds - 12
            xxE = "PM"        
            
        if hourEnds == 0:
            hourEnds = 12
            xxE = 'AM'
            #dayEnds = dayEnds + 1 
        
        
        minuteEnds = (timeEnds[3:5])
        minEnds = int(timeEnds[3:5])
        newEnds = (str(hourEnds) + minuteEnds)
        
        endTime = (datetime(yearEnds,monthEnds,dayEnds,hourEnds,minEnds))
        endTimeEpoch = round(endTime.timestamp())
        diff = (endTimeEpoch - startTimeEpoch)                      
                              
        # Calculate day of the week, start and stop times for formstting
        dayNum = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        
        weekdayStartTime = datetime(yearOnset,monthOnset,dayOnset,hourOnset,minOnset)
        weekdayEndTime = datetime(yearEnds,monthEnds,dayEnds,hourEnds,minEnds)
                       
        dayOfWeekStart = weekdayStartTime.weekday()        
        dayOfWeekEnd = weekdayEndTime.weekday()
        
        first = dayNum[dayOfWeekStart]
        last = dayNum[dayOfWeekEnd]                          
       
        if newOnset == 0:
            newOnset = 12
                    
        if newEnds == 0:
            newEnds = "until further notice"  
            
        # 
        # Check on the DST status
        #
        
        isDST = checkDST.checkDST()
        if isDST == 1:
            tz = ['EDT','CDT','MDT','PDT']
            ldt = (UTC_offset - 4)
            tz1 = tz[ldt]     
            
        else:
            tz = ['EST','CST','MST','PST']
            ldt = (UTC_offset - 5)
            tz1 = tz[ldt]     
                
         
        # Write to file for further processing...
        with open(full_filename, 'a') as outfile:   
            print("Watch/Warning/Advisory information...","\n", file = outfile)
            print(f'From: {senderName}', file = outfile)
            print(f'Watches/Warnings/Advisories in effect: {event},', file = outfile)
            print(f'Areas Affected: {areaDesc} counties', file = outfile)
                       
            if newEnds == "until further notice":
                print(f'Valid from {newOnset} {xx} {tz1} {first} until further notice...', file = outfile)
            else:
                print(f'Valid from {newOnset} {xx} {tz1} {first} to {newEnds} {xxE} {tz1} {last}', file = outfile)  
             
        j+=1


# In[ ]:





# In[ ]:





# In[ ]:




