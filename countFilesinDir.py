#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os

dir_path = '/home/ec2-user/'
count = 0

for a in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, a)):
        count += 1
print("This is the number of files in the directory: ", count)


# In[14]:


import fnmatch

dir_path = '/home/ec2-user/'
dir_path_next = '/home/ec2-user/needSQL'
count = len(fnmatch.filter(os.listdir(dir_path), '*.py'))
print(f'This is the number of Python files in the {dir_path}: {count}')
print('\n')

count = len(fnmatch.filter(os.listdir(dir_path), '*.log'))
print(f'This is the number of log files in the {dir_path}: {count}')
print('\n')

count = len(fnmatch.filter(os.listdir(dir_path_next), '*.py'))
print(f'This is the number of Python files in the {dir_path_next}: {count}')
print('\n')


# In[10]:


'''
import os

count = 0
dir_path = '/home/ec2-user/'
for path in os.scandir(dir_path):
    if path.is_file():
        count += 1
print(f'This is the number of files in {dir_path}: {count}')
'''


# In[ ]:




