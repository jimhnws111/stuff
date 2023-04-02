#!/usr/bin/env python
# coding: utf-8

# In[39]:


import datetime
import time
import calcTimeStamp
from datetime import timezone
from datetime import datetime, timedelta

# Calculate the time and date for calculations so far

xy = calcTimeStamp.calcTimeStamp()
start, end = (xy[0], xy[1])
start = str(start)
end = str(end)


# In[40]:


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
data_dir_file = '/Users/jameshayes/davis.json' 
with open(data_dir_file, "w") as fd:   
     json.dump(r.json(), fd)


# In[41]:


import collections
import hashlib
import hmac
import time
from datetime import datetime
import requests
import json
import pprint

with open('/Users/jameshayes/davis.json') as fr:
    davisAPI = json.load(fr)
    
  
a = davisAPI['sensors']    
b = a[1]
c = (b['data'])
cLen = len(c)
print(cLen)

with open('/Users/jameshayes/testout.csv', 'w') as outfile: 
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


# In[42]:


import pandas as pd

#
# Read in the CSV file for processing in pandas
#

path_name = '/Users/jameshayes/'
file_name = 'testout.csv'
full_file = (f'{path_name}{file_name}')

df = pd.read_csv(full_file, index_col=False,names=['temp_hi', 'temp_lo', 'rainfall','time'])


# In[43]:


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

recentT = (df['time'].iloc[-1])
print(recentT)
datetime_obj = datetime.strptime(recentT, '%Y-%m-%d %H:%M:%S')
lastTime = datetime_obj.strftime('%I:%M %p')


# write the data to a csv file with an html suffix

with open('/Users/jameshayes/Sites/HiLoRain.csv', 'w') as outfile:
    print(f'{maxT},{minT},{totR},{lastTime}',file = outfile)
 

#Write to an HTML for display
df1 = pd.read_csv('/Users/jameshayes/Sites/HiLoRain.csv', names = ['High','Low','Rainfall','Time'], index_col = False)
pd.set_option('display.precision', 2)
df1_style = df1.style.set_properties(**{"background-color": "lightblue",  
                           "color" : "black",
                           "border" : "1.5px black",
                           "text-align": "center",
                           "font-weight": "bold",
                           "font-size": "20px"})

df1.to_html('/Users/jameshayes/Sites/SoFarTest.html', index = False)  


# In[44]:


import pandas as pd

df2 = pd.read_html('/Users/jameshayes/Sites/SoFarTest.html')
a = df2[0]
df3 = pd.DataFrame(a)
properties = {"color": "black", "font-size": "20px", "background-color":"lightblue", "text-align":"center"}
df3_style = df3.style.set_properties(**properties)
df3_style.hide(axis = 'index')
df3_style.format({'Rainfall':"{:.2f}"})

df3_style.to_html('/Users/jameshayes/Sites/new_test.html', index=False, justify ='center')


# In[45]:


# Clip out offending lines in the hmtl file created in the previous section

values = ['>&nbsp;</th>\n','level0 row0" >0</th>\n']

with open('/Users/jameshayes/Sites/new_test.html', 'r') as ff:
         lines = ff.readlines()
         
with open('/Users/jameshayes/Sites/newer_test.html', 'w') as fg:
         for line in lines:
                
                result = any(map(line.endswith, values))
                if result == False:
                    fg.writelines(line)                   


# In[ ]:





# In[ ]:




