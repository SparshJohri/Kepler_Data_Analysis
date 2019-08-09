# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 22:37:18 2019

@author: bhata
"""

import pandas

campaign_2_targets  = pandas.read_csv("Campaign_2_EPICS.csv")
campaign_2_targets .set_index(campaign_2_targets .columns[0], inplace=True, drop = True)
pre_main_sequence_stars = pandas.read_csv("Data_on_PMS_Stars.csv"  )
pre_main_sequence_stars.set_index(pre_main_sequence_stars.columns[0], inplace=True, drop = True)

for i in pre_main_sequence_stars.index:
    print("------------------------------------------------------------------")
    print(i)
    print(pre_main_sequence_stars.loc[i])

print("------------------------------------------------------------------")