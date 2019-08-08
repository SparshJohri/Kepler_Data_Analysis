# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 23:16:21 2019

@author: bhata
"""

import pandas


column = ["A", "B", "C"]
row = ["E", "F"]
my_data = pandas.DataFrame(columns = column, index = row)

for i in range(len(my_data)):
    my_data.iloc[i]["A"]=0
    my_data.iloc[i]["B"]=0
    my_data.iloc[i]["C"]=0

print(my_data)

export_csv = my_data.to_csv (r'C:\Sparsh Johri 2019\Kepler Data\data1.csv')