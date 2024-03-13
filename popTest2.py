#!/usr/bin/env python
# coding: utf-8

# In[58]:


import pandas as pd
import dataFile
import getNameNumbers
import sqlalchemy
import mysql.connector
import sqlite3
import getDays
import pymysql as dbapi

todayInfo = getDays.getToday()
yesterdayInfo = getDays.getYesterday()
tomorrowInfo = getDays.getTomorrow()

month, month_num, date, year = todayInfo[0], todayInfo[1], todayInfo[2], todayInfo[3]
yesterday = yesterdayInfo[2]
yesterday = int(yesterday)
nextDay = tomorrowInfo[2]
nextDay = int(nextDay)


QUERY = """
        SELECT @startTime := timeStamp FROM testTempest ORDER BY id DESC LIMIT 1;
        SELECT @endTime := DATE_SUB(@startTime, INTERVAL 24 Hour);
        SELECT * from testTempest WHERE timeStamp BETWEEN @endTime AND @startTime;
        """

print(QUERY)


db = dbapi.connect(host='3.135.162.69',user='chuckwx',passwd='jfr716!!00', database = 'hourlyt')

cur = db.cursor()
cur.execute(QUERY)
result = cur.fetchall()
print(result)


# In[ ]:




