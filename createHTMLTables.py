#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import pymysql as dbapi
from pretty_html_table import build_table
import os
import daysAndDatesNew

#
# use environmental variables for the SQL query
#

db_user = 'chuckwx'
db_password = 'jfr716!!00'
dayInfo = daysAndDatesNew.daysAndDatesNew()

month, month_num, date, year = dayInfo[0], dayInfo[1], dayInfo[2], dayInfo[3]
yesterday = int(dayInfo[4])
nextDay = int(dayInfo[5])

def createHTMLTables():
    
    """Creare two HTML tables for the F6 data to be viewed"""

    #db_user = os.environ.get('dbUser')
    #db_password = os.environ.get('dbPass')

    QUERY2 = """SELECT * FROM davisCompTest 
             WHERE Month = %s""" % (month_num)


    #html_path = '/var/www/html/000/'
    html_path = '/Users/jameshayes/Sites/'
    print("This is the MFing path ", html_path)
    db = dbapi.connect(host='3.135.162.69', user=db_user, passwd=db_password, database = 'davisf6', port = 3306)

    cur = db.cursor()
    cur.execute(QUERY2)
    dateResult = cur.fetchall()
    
    colNames = (['Year', 'Month', 'Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point']) 
    pd.options.display.float_format = '{:,.2f}'.format
    df3 = pd.DataFrame(dateResult, columns = colNames) 
    df3 = df3.drop(df3.columns[[0, 1]], axis = 1)
    df3 = df3.reindex(columns=['Date', 'High', 'Low', 'Average', 'HDD', 'CDD', 'Rainfall', 'Max_Dew_Point'])
    df3.to_html(f'{html_path}throttledTest.html', index = False)     

    html_table_blue_light = build_table(df3, 'blue_light', text_align='center', font_size='32px')

    with open(f'{html_path}davisCompTest.html', 'w') as f:
              f.write(html_table_blue_light)  

