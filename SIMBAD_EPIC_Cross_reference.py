# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 23:54:35 2019

@author: bhata
"""

from selenium import webdriver
import pandas


driver = webdriver.Chrome('chromedriver.exe') #opens the webdriver
csv_file = pandas.read_csv("Campaign_2_EPICS.csv") #opens the csv_file
epics = csv_file.iloc[pandas.np.r_[30:35, 275:288, 330:334, 670:690, 750:755, 1100:1106, 1107:2207]] 
#gets the appropriate EPID IDs (saves time this way)
key_phrases = ['T Tau-type Star', 'Pre-main sequence Star', 'Emission-line Star', 'Young Stellar Object', 'Flare Star'\
               'Variable Star of Orion Type', 'Brown Dwarf', 'Star in Association'] #establishes which phrases indicate a PMS star

pms= pandas.DataFrame(columns = ["EPIC ID","Type"]) #sets up the dataframe that will take the PMS stars

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

for id in epics["EPIC ID"]:
    driver.get('http://simbad.u-strasbg.fr/simbad/sim-id?Ident=EPIC+'+str(id)+'&submit=submit+id') #gets the page
    #-------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------
    try:
        ids = driver.find_elements_by_xpath("//*[contains(@id,'basic_data')]") 
        path = '//*[@id="' + ids[0].get_attribute('id') +'"]/table/tbody/tr/td/font' 
        element = driver.find_elements_by_xpath(path)
        element = element[0] #goes through the path to find the label associated with the stellar body
        #-------------------------------------------------------------------------------------------------------------
        #-------------------------------------------------------------------------------------------------------------
        in_key_phrases = False #sets up the variable that will tell us if the label indicates that the stellar body is a PMS star
        phrase = "" #will get the label of the stellar body (Star, Brown Dwarf, T Tau-type Star, High Proper-Motion Star, etc.)
        for i in key_phrases:
            if element.text.find(i)!= -1:
                in_key_phrases = True
                phrase = i
                break #finds if the label matches one of the key phrases
        #-------------------------------------------------------------------------------------------------------------
        #-------------------------------------------------------------------------------------------------------------            
        if in_key_phrases == True:
            print( 'EPIC ID ',id,': pre-main sequence!!!')
            pms = pms.append(pandas.Series([id, phrase], index=pms.columns), ignore_index=True)
            #appends the star's EPIC ID and label into the PMS dataframe
        else:
            print( 'EPIC ID ',id,': NOT pre-main sequence')
        #-------------------------------------------------------------------------------------------------------------
        #-------------------------------------------------------------------------------------------------------------
    except IndexError: #checks if the given EPIC ID is even in the SIMBAD database
        print('EPIC ID ', id, ': not in database')

    except TimeoutError: #checks if a web page takes too long to load (that would crash the program if not addressed)
        print("Web page took too long to download. Terminating the for-loop.")
        break
    #-------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------
pms.set_index('EPIC ID', inplace=True, drop = True)
print( 'PMS stars found: ',len(pms)) 
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
export_csv = pms.to_csv (r'Campaign_2_PMS.csv')
print("File exported")
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
print("End of Program")
driver.quit() #closes the web page