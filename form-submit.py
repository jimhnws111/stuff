#!/usr/bin/env /Users/jameshayes/opt/anaconda3/bin/python

print("Content-Type: text/x-python\n\n")

import cgi
import webbrowser

form = cgi.FieldStorage()
f_name=form["f_name"].value
s_name=form["s_name"].value

print("Month",f_name)
print("Year",s_name)

Smash = f_name + s_name
print("Month and name", Smash)
first_part = ("http://trclimate.org/")
last_part = ("_ALT.html")

full_url = (f'{first_part}{Smash}{last_part}')
print(full_url)

webbrowser.open(full_url)

