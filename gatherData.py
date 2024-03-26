#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pymysql as dbapi
import os
import getData1
import daysAndDatesNew
import sys

#
# Get some needed data first
#

bsd = daysAndDatesNew.daysAndDatesNew()
month, month_num, date, year = bsd[0], bsd[1], bsd[2], bsd[3]
db_user = 'chuckwx'
db_password = 'jfr716!!00'
print(db_user, db_password)

def gatherData():

    QUERY = """SELECT * FROM avgHiLo 
               WHERE Month = %s 
               AND Day = %s""" % (month_num, date)


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

    recordRain = result3[0]
    recRain = recordRain[1]
    recRainYear = int(recordRain[4])


# In[35]:


gatherData()


# In[ ]:




