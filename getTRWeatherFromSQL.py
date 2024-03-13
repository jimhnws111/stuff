#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import dataFile
import getNameNumbers
import sqlalchemy
import mysql.connector
import sqlite3
import NoDaysInMonth

# creating connection
conn = mysql.connector.connect(
  host="3.135.162.69",
  user="chuckwx",
  password="jfr716!!00"
)

mycursor = conn.cursor()
mycursor.execute("USE trweather;")
pop1 = ("select @startTime := timeGroup from trw order by timeGroup DESC LIMIT 1;")
pop2 = ("SELECT @endTime := DATE_SUB(@startTime, INTERVAL 30 Day);")
pop3 = ("SELECT * from trw WHERE timeGroup BETWEEN @endTime AND @startTime into OUTFILE '/tmp/trw1.csv';")
popSelect = pop1 + pop2 + pop3

mycursor.execute(popSelect)

