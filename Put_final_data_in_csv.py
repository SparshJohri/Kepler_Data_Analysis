# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 22:37:18 2019

@author: bhata
"""

import pandas

campaign_2_targets = pandas.read_csv("Campaign_2_EPICS.csv") #gets all of the Campaign 2 targets
campaign_2_targets.set_index(campaign_2_targets .columns[0], inplace=True, drop = True) #sets up the EPIC ID as the index of the dataframe
pre_main_sequence_stars = pandas.read_csv("Campaign_2_PMS.csv"  ) #gets of the Campaign 2 PMS stars
pre_main_sequence_stars.set_index(pre_main_sequence_stars.columns[0], inplace=True, drop = True) #sets up the EPIC ID as the index of the dataframe
final_table = pandas.DataFrame(columns = ["Epic ID", "Right Ascension", "Declination", "Magnitude", "Investigation IDs", "Type"])
#sets up the final table that will contain the complete information about the PMS stars

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

for i in range(len(pre_main_sequence_stars.index)): #iterates through the PMS stars
    epic_id = pre_main_sequence_stars.index[i] #gets the EPIC ID
    table1 = campaign_2_targets.loc[epic_id] #gets the data pertaining to the EPIC ID from the campaign 2 targets dataframe
    #-------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------
    RA = table1[table1.index[0]]
    Dec= table1[table1.index[1]]
    mag= table1[table1.index[2]]
    inv= table1[table1.index[3]]
    typ= pre_main_sequence_stars.iloc[i]["Type"]
    #-------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------
    final_table = final_table.append(pandas.Series([epic_id, RA, Dec, mag, inv, typ], index = final_table.columns),\
                                     ignore_index=True) 
    #puts the data about the EPIC ID, right ascension, declination, magnitude, investigation IDs, and type into the final table dataframe
    #-------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------
    print(campaign_2_targets.loc[epic_id])
    print("-----------------------------------------------------")
    #-------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------
final_table.set_index('Epic ID', inplace=True, drop = True) #sets up the EPIC ID as the index of the final table
export_csv = final_table.to_csv (r'Data_on_PMS_Stars.csv') #exports the final table into a csv file