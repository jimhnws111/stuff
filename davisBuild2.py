#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime
import time
from datetime import datetime, timedelta
import UTC2local

#
# Set up the start and end tims for API call
#

xy = UTC2local.UTC2local()
start, end = (xy[0], xy[1])
start = str(start)
end = str(end)


# In[ ]:


import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json

parameters = {
  "api-key": "vy8jbrjsxlbwgojepq3vfyfqfywyhvbd", 
  "api-secret": "sdqfm6wdfy9w0pqp2vdka38o6b4vcsvc",
  "station-id": 81211, 
  "end-timestamp": end,
  "start-timestamp": start,
  "t": int(time.time())
}

parameters = collections.OrderedDict(sorted(parameters.items()))

for key in parameters:
    print("Parameter name: \"{}\" has value \"{}\"".format(key, parameters[key]))

apiSecret = parameters["api-secret"];
parameters.pop("api-secret", None);

data = ""
for key in parameters:
    data = data + key + str(parameters[key])

print("Data string to hash is: \"{}\"".format(data))
print('\n')

"""
Calculate the HMAC SHA-256 hash that will be used as the API Signature.
"""
apiSignature = hmac.new(
  apiSecret.encode('utf-8'),
  data.encode('utf-8'),
  hashlib.sha256
).hexdigest()

"""
Let's see what the final API Signature looks like.
"""
print("API Signature is: \"{}\"".format(apiSignature))
print('\n')

# Building the URL to get the station

first_part = ('https://api.weatherlink.com/v2/historic/81211?')
api_key = ('api-key=vy8jbrjsxlbwgojepq3vfyfqfywyhvbd')
add_apisig = ('&api-signature=')
add_t = ('&t='+ str(int(time.time())))
start1 = "&start-timestamp=" + start
end1 = "&end-timestamp=" + end

#
URLfinal = (first_part + api_key + add_t + start1 + end1 + add_apisig + apiSignature)
print(URLfinal)

r =  requests.get(URLfinal)
r.encoding = 'utf-8'

r =  requests.get(URLfinal)

data_dir_file = '/home/ec2-user/davis.json' 
with open(data_dir_file, "w") as fd:   
     json.dump(r.json(), fd)


# In[ ]:


import time
from datetime import datetime

with open(data_dir_file) as fr:
    davisAPI = json.load(fr)   
  
a = davisAPI['sensors']    
b = a[1]
c = (b['data'])
cLen = len(c)
print(cLen)

with open('/home/ec2-user/testout.csv', 'w') as outfile: 
    i = 0
    while i < cLen:
        d = c[i]
        hi_temp = (d['temp_hi'])
        lo_temp = (d['temp_lo'])
        rainfall = (d['rainfall_in'])
        time = (d['ts'])
        date_time = datetime.fromtimestamp(time)
        print(f'{hi_temp},{lo_temp},{rainfall},{date_time}', file = outfile)
        i += 1
        
import pandas as pd
import datetime
from datetime import datetime
from dateutil.tz import tzutc, tzlocal
import pytz

path_name = '/home/ec2-user/'
file_name = 'testout.csv'
full_file = (path_name + file_name)

#
# Set up pandas dataframe and extract needed data
#

df = pd.read_csv(full_file, index_col=False,names=['temp_hi', 'temp_lo', 'rainfall','time'])

pd.set_option('display.max_rows', 1440)
pd.set_option('display.max_columns', 35)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

max_temp  = (df.sort_values(by='temp_hi', ascending=False))
max_T = max_temp.iloc[:1]
maxT = max_T['temp_hi'].values[0]
maxT = round(maxT)

min_temp  = (df.sort_values(by='temp_lo', ascending=True))
min_T = min_temp.iloc[:1]
minT = min_T['temp_lo'].values[0]
minT = round(minT)
minT = str(minT)
minT = minT.strip()

totR = df['rainfall'].sum()
totR = round(totR,2)
ncR = "None"
storm = "None"
print(storm)

timezone = pytz.timezone("America/New_York")
recentT = (df['time'].iloc[-1])
datetime_obj = datetime.strptime(recentT, '%Y-%m-%d %H:%M:%S')
localT = datetime_obj.astimezone(timezone)
print(localT)
#lastTime = datetime_obj.strftime('%I:%M %p')
lastTime = localT.strftime('%I:%M %p')
print(lastTime)
#lastTime = datetime_obj.strftime('%I:%M %p')

# write the data to a csv file with an html suffix

with open('/home/ec2-user/HiLoRain.csv', 'w') as outfile:
    print(f'{maxT},{minT},{totR},{ncR},{storm},{lastTime}', file = outfile)

