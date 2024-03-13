#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pymysql as dbapi
import sys
import csv
from tabulate import tabulate
import getDays
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('/home/ec2-user/sandbox2.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def sandbox2():  
           
    todayInfo = getDays.getToday()
    yesterdayInfo = getDays.getYesterday()
    tomorrowInfo = getDays.getTomorrow()

    month, month_num, date, year = todayInfo[0], todayInfo[1], todayInfo[2], todayInfo[3]
    yesterday = yesterdayInfo[2]
    yesterday = int(yesterday)
    nextDay = tomorrowInfo[2]
    nextDay = int(nextDay)

    #
    # Get normal highs and lows
    #

    QUERY = """SELECT * FROM avgHiLo 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)
    
    #
    # use environmental variables for the SQL query
    #

    db_user = os.environ.get('dbUser')
    db_password = os.environ.get('dbPass') 

    db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

    cur = db.cursor()
    cur.execute(QUERY)
    result = cur.fetchall()

    dataset = result[0]
    nmlHi = int(dataset[3])
    nmlLo = int(dataset[4])
    
    #
    # Get the record high for the date
    #

    QUERY1 = """SELECT * FROM recHigh 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)


    db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

    cur = db.cursor()
    cur.execute(QUERY1)
    result1 = cur.fetchall()
    recordHigh = result1[0]
    recHigh = int(recordHigh[1])
    recHighYear = int(recordHigh[4])

    #
    # Get the record low for the date
    #

    QUERY2 = """SELECT * FROM recLow 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)


    db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

    cur = db.cursor()
    cur.execute(QUERY2)
    result2 = cur.fetchall()
    recYearNum =  len(result2)
    recordLow = result2[0]
    recLow = int(recordLow[1])
    recLowYear = int(recordLow[4])

    #
    # Get the record rainfall for the date
    #
    
    QUERY3 = """SELECT * FROM recRain 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)


    db = dbapi.connect(host='3.135.162.69',user=db_user,passwd=db_password, database = 'trweather')

    cur = db.cursor()
    cur.execute(QUERY3)
    result3 = cur.fetchall()
    recYearNum =  len(result3)
    recordRain = result3[0]
    recRain = float(recordRain[1])
    recRainYear = int(recordRain[4])
    
    return(result1,result2, result3, nmlHi, nmlLo)


# In[8]:


sandbox2()


# In[ ]:




