#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import urllib
import requests
import csv
import re


# In[2]:


#urltest = 'https://api.synopticdata.com/v2/stations/latest?token=146a1e25358f48f0a9d83a9a0d55e05c&state=ca&network=1,2&minmax=1&minmaxtype=local&units=english&within=60&vars=air_temp'
#urltest = 'https://api.synopticdata.com/v2/stations/latest?token=demotoken&bbox=-125,24.5,-66.95,49.35&country=us&network=1,2&minmax=1&minmaxtype=utc&units=english&within=60&vars=air_temp'
#urltest = 'https://api.synopticdata.com/v2/stations/latest?token=146a1e25358f48f0a9d83a9a0d55e05c&bbox=-125,24.5,-66.95,49.35&country=us&network=1,2&minmax=1&minmaxtype=utc&units=english&within=60&vars=air_temp'
urltest = 'https://api.synopticdata.com/v2/stations/latest?token=146a1e25358f48f0a9d83a9a0d55e05c&bbox=-125,24.5,-66.95,49.35&country=us&network=1,2,26,123&minmax=1&minmaxtype=utc&units=english&within=60&vars=air_temp&showemptystations=0'

r =  requests.get(urltest)
r.encoding = 'utf-8'
print (r.json())
print (r.encoding)
print (r.headers)

#
# set the data directory/file here
# the data file name is synoptic.json
#

data_dir_file = '/home/ec2-user/synoptic.json' # ***This needs to be changed to your installtion directory***

with open(data_dir_file) as fd:   
     json.dump(r.json(), fd)


# In[ ]:




