import json
import urllib
import requests
import os
import datetime
from datetime import datetime
from tqdm.notebook import tqdm
import time

def getAlertsPANJ():

    states = ['PA', 'NJ', 'LA']
    file_path = '/Users/jameshayes/'

    #try:
    #    os.remove(f'{file_path}/nwsAlerts.json')
    #except FileNotFoundError: 
    #    print("The file was not found")

    for y in states:
        urlTest = f"https://api.weather.gov/alerts/active?area={y}"
        print(f'Retrieving active alerts for {y}...')
        r =  requests.get(urlTest)
        r.encoding = 'utf-8'
        x = r.json()
                
        data = x['features']
        w = len(data)
        print(w)
                
        if w == 0:
            print(f'There are no watches/warnings/advisories in effect for {y}')
            print('\n')
            continue
            
        j=0
        while j <= w:
            
            print(j,w)
            q = (data[j])
            id = q['properties']
            areaDesc = id['areaDesc']
            print(areaDesc)
            areaDesc = areaDesc.replace(";",",")
            geocode = id['geocode']
            affectedZones = id['affectedZones']
            references = id['references']
            parameters = id['parameters']
            sent = id['sent']
            effective = id['effective']
            onset = id['onset']
            expires = id['expires']
            ends = id['ends']
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
            vtec = parameters['VTEC']
            
                    
            
        
 
        # Putting together the time parameters - first start time
        yearOnset = int(onset[:4])
        monthOnset = int(onset[5:7])
        dayOnset = int(onset[8:10])
        timeOnset = onset[11:16]
        hourOnset = int(timeOnset[0:2])
        if hourOnset == 0:
            hourOnset = 12
        minuteOnset = (timeOnset[3:5])
        minOnset = int(timeOnset[3:5])
        newOnset = (str(hourOnset) + minuteOnset)  
        startTime = datetime(yearOnset,monthOnset,dayOnset,hourOnset,minOnset)
        startTime = round(startTime.timestamp())
    
        # Now ending time
        yearEnds = int(ends[:4])
        monthEnds = int(ends[5:7])
        dayEnds = int(ends[8:10])
        timeEnds = ends[11:16]
        hourEnds = int(timeEnds[0:2])
        minuteEnds = (timeEnds[3:5])
        minEnds = int(timeEnds[3:5])
        newEnds = (str(hourEnds) + minuteEnds)
        endTime = (datetime(yearEnds,monthEnds,dayEnds,hourEnds))
        endTime = round(endTime.timestamp())
    
    
        #Currently in effect or not
    
        nowTime = round(time.time())
        if nowTime in range(startTime, endTime):
            print(f'{event} is currently in effect')
        else:
            print(f'{event} is NOT currently in effect')      
    
        # AM or PM?
        if hourOnset == 0:
            XX = " AM"
        elif hourOnset < 13:
            XX = " AM"
        else:
            XX = " PM"
    
        # Calculate day of the week
        dayNum = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
        weekdayStartTime = datetime(yearOnset,monthOnset,dayOnset,hourOnset,minOnset)
        weekdayEndTime = datetime(yearEnds,monthEnds,dayEnds,hourEnds,minEnds)
    
        dayOfWeekStart = weekdayStartTime.weekday()
        dayOfWeekEnd = weekdayEndTime.weekday()
    
        first = dayNum[dayOfWeekStart]
        last = dayNum[dayOfWeekEnd]
    
        #print out Watch/Warning/Advisory information
    
        print('\n')
        print(f'From: {senderName}')
        print(f'Watches/Warnings/Advisories in effect: {event}')
        print(f'Areas Affected: {areaDesc} counties')
        print(f'Valid from {newOnset}{XX} {first} to {newEnds}{XX} {last}')    
            
        j+=1
        
  
 
    #with open(f'{file_path}nwsAlerts.json','a') as fd:
    #    json.dump(r.json(), fd)
        
    return     