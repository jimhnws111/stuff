#!/usr/bin/env python
# coding: utf-8

# In[1]:


import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json
import dataFile
import getData
import checkDST
import getStartEnd

#
# Start the module
#

def dataFromDavis1():
    
    import getStartEnd
    startEnd = getStartEnd.getStartEnd()
    start, end = startEnd[0], startEnd[1]
 
    print(start, end)    
    
    parameters = {
      "api-key": "vy8jbrjsxlbwgojepq3vfyfqfywyhvbd", 
      "api-secret": "sdqfm6wdfy9w0pqp2vdka38o6b4vcsvc",
      "station-id": 81211, 
      "end-timestamp": end,
      "start-timestamp": start,
      "t": int(time.time())
    }

    parameters = collections.OrderedDict(sorted(parameters.items()))

   #for key in parameters:
   #     print("Parameter name: \"{}\" has value \"{}\"".format(key, parameters[key]))

    apiSecret = parameters["api-secret"];
    parameters.pop("api-secret", None);

    data = ""
    for key in parameters:
        data = data + key + str(parameters[key])

    #logger.info('Data string to hash is: \"{}\"'.format(data))   


    apiSignature = hmac.new(
      apiSecret.encode('utf-8'),
      data.encode('utf-8'),
      hashlib.sha256
    ).hexdigest()


    #logger.info('API Signature is: \"{}\"'.format(apiSignature))

    # Building the URL to get the station

    first_part = ('https://api.weatherlink.com/v2/historic/81211?')
    api_key = ('api-key=vy8jbrjsxlbwgojepq3vfyfqfywyhvbd')
    add_apisig = ('&api-signature=')
    add_t = ('&t='+ str(int(time.time())))

    start1 = "&start-timestamp=" + start
    end1 = "&end-timestamp=" + end

    URLfinal = (first_part + api_key + add_t + start1 + end1 + add_apisig + apiSignature)

    r =  requests.get(URLfinal)
    davisAPI = (r.json())
    
    return(davisAPI)

dataFromDavis1()


# In[ ]:




