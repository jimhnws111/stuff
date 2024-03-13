#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime
import time
import calcTimeStamp
#from datetime import timezone
from datetime import datetime, timedelta
import UTC2local

xy = UTC2local.UTC2local()
start, end = (xy[0], xy[1])
print(end - start)
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
import pprint

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


import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json
import pprint

with open(data_dir_file) as fr:
    davisAPI = json.load(fr) 

print(davisAPI.keys())
#print(davisAPI)    
    
a = davisAPI['sensors']   
b = a[1]
print(b.keys())
c = (b['data'])
cLen = len(c)
#print(cLen)

with open('/home/ec2-user/davis1m.csv', 'w') as outfile: 
    i = 0
    while i < cLen:
        d = c[i]
        hi_temp = (d['temp_hi'])
        lo_temp = (d['temp_lo'])
        rainfall = (d['rainfall_in'])
        hi_hum = (d['hum_hi'])
        lo_hum = (d['hum_lo'])
        wind_dir = (d['wind_dir_of_prevail'])
        wind_speed = (d['wind_speed_hi'])
        #baro = (d['bar_hi'])
        rain_rate = (d['rain_rate_hi_in'])
        time = (d['ts'])
        date_time = datetime.fromtimestamp(time)
        print(f'{hi_temp},{lo_temp},{rainfall},{hi_hum},{lo_hum},{wind_dir},{wind_speed},{rain_rate},{date_time}', file = outfile)
        i += 1

