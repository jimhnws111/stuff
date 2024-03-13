#!/usr/bin/env python
# coding: utf-8

# In[76]:


import pandas as pd
import datetime
from datetime import datetime
import sqlalchemy
import mysql.connector
import sqlite3

df = pd.read_csv('/home/ec2-user/CompleteWeatherRecordsExport.csv')

database_username = 'chuckwx'
database_password = 'jfr716!!00'
database_ip       = '3.135.162.69'
database_name     = 'trweather'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name), connect_args={'connect_timeout': 30})
df.to_sql(con=database_connection, name='trweather', if_exists='replace')


# In[ ]:




