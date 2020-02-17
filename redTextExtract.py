# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:01:47 2020

@author: anonymous user
"""
import pandas as pd
datafile_loc = (r"C:\Users\A8DPDZZ\Documents\OpenMV\test scratch.txt")
df = pd.read_csv(datafile_loc, header=None)
df = df.rename(columns={0:"Status",1:"Mo",2:"Wd",3:"Day",4:"Hr",5:"Min",6:"Sec",7:"Subsec"})
df_red = df[df['Status'].str.contains("red identified")] 
print(df_red)