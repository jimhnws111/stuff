#!/usr/bin/env python
# coding: utf-8

# In[5]:


import excelFilename

def setUpHTML_mac():
    html_path = '/Users/jameshayes/Sites/'
    kw = excelFilename.wxflow()
    xls_filename, path_to_file = (kw[0],kw[1])
    new_file = f'{path_to_file}{xls_filename}'
    
    return(new_file, html_path)

def setUpHTML_davis():
    html_path = '/var/www/html/000/'
    ky = excelFilename.davis()
    xls_filename, path_to_file = (ky[0],ky[1])
    new_file = f'{path_to_file}{xls_filename}'
    print(new_file)
    
    return(new_file, html_path)

def setUpHTML_tempest_ec2():
    html_path = '/var/www/html/000/'
    kw = excelFilename.tempest_ec2()
    xls_filename, path_to_file = (kw[0],kw[1])
    new_file = f'{path_to_file}{xls_filename}'
    
    return(new_file, html_path)


# In[6]:


setUpHTML_tempest_ec2()


# In[ ]:




