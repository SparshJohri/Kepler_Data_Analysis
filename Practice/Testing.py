# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 09:45:10 2019

@author: bhata
"""

from selenium import webdriver
import pandas


driver = webdriver.Chrome('chromedriver.exe') 
#establishes the driver
print("Driver established")
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
driver.get('https://keplerscience.arc.nasa.gov/k2-approved-programs.html') #gets the page
campaigns = driver.find_elements_by_xpath("//*[contains(@id,'campaign-2')]")

for campaign in range(len(campaigns)):
    campaigns[campaign] = campaigns[campaign].get_attribute(('id'))

campaign = campaigns[0]

titles = list()

programs = '//*[@id="' + campaign +'"]/div[1]/div[2]/table[1]/tbody[1]/tr'
programs = driver.find_elements_by_xpath(programs)
programs = len(programs)

for i in range(programs):
    path = '//*[@id="' + campaign +'"]/div[1]/div[2]/table[1]/tbody[1]/tr['+str(i+1)+']/td[3]/a'
    title = driver.find_elements_by_xpath(path)[0].text.lower()
    titles.append(title)

#key_phrases = ['t tau-type star', 'pre-main sequence Star', 'emission-line star', 'young stellar object', 'flare star'\
#               'variable star of orion type', 'brown dwarf', 'star in association']

key_phrases = ["brown dwarf", "young", "pre-main sequence"]

places = list()

for i in range(programs):
    in_key_phrases = False #sets up the variable that will tell us if the label indicates that the stellar body is a PMS star
    phrase = "" #will get the label of the stellar body (Star, Brown Dwarf, T Tau-type Star, High Proper-Motion Star, etc.)
    for j in key_phrases:
        if titles[i].find(j)!= -1:
            in_key_phrases = True
            phrase = i
            break #finds if the label matches one of the key phrases          
    if in_key_phrases == True:
        places.append(i)
 
information = list()       
labels = list() #will hold the names of each program

for tr_value in places:
    
    path = '//*[@id="'+ campaign +'"]/div[1]/div[2]/table[1]/tbody[1]/tr['+str(tr_value)+']/td[4]/a' 
    #the path for the data   
    path1 = '//*[@id="' + campaign +'"]/div[1]/div[2]/table[1]/tbody[1]/tr['+str(tr_value)+']/td[1]' 
    #the path for the name of the program
    
    label = driver.find_elements_by_xpath(path1)[0].text
    labels.append(label) #appends the name of the program into the list of labels
    
    table_place = driver.find_elements_by_xpath(path)[0] #gets to the right place in the table
    URL = table_place.get_attribute("href") #gets the URL
    csv_file = pandas.read_csv(URL)
    csv_file.set_index(csv_file.columns[0], inplace=True, drop = True)
    information.append(csv_file)
    print(tr_value)
 


information = pandas.Series(information, index = labels) #converts "information" into a Series    
campaign_2_targets  = pandas.read_csv("Campaign_2_EPICS.csv")
campaign_2_targets .set_index(campaign_2_targets .columns[0], inplace=True, drop = True)

epics = list()
for i in range(len(information)):
    sub_epics = list(information.iloc[i].index)
    for j in sub_epics:
        epics.append(j)
print(len(epics))
epics = list(set(epics))
print(len(epics))


column_values = list(campaign_2_targets.columns) + ["Spectral Type", "Classification"]
stars = pandas.DataFrame(columns = column_values)
for i in epics:
    try:
        stars.loc[i] = campaign_2_targets.loc[i]
    except KeyError:
        pass


pms_stars = pandas.DataFrame(columns = column_values)
key_phrases = ['T Tau-type Star', 'Pre-main sequence Star', 'Emission-line Star', 'Young Stellar Object', 'Flare Star'\
               'Variable Star of Orion Type', 'Brown Dwarf', 'Star in Association']

#a = list(pandas.np.r_[30:35, 275:288, 330:334, 670:690, 750:755, 1100:1106, 1107:1200])
a = [2070, 1614]
for EPIC in a:
    driver.get('http://simbad.u-strasbg.fr/simbad/sim-id?Ident=EPIC+'+str(stars.index[EPIC])+'&submit=submit+id')
    try:
        ids = driver.find_elements_by_xpath("//*[contains(@id,'basic_data')]") 
        path = '//*[@id="' + ids[0].get_attribute('id') +'"]/table/tbody/tr/td/font' 
        element = driver.find_elements_by_xpath(path)
        element = element[0].text #goes through the path to find the label associated with the stellar body
        
        in_key_phrases = False #sets up the variable that will tell us if the label indicates that the stellar body is a PMS star
        phrase = "" #will get the label of the stellar body (Star, Brown Dwarf, T Tau-type Star, High Proper-Motion Star, etc.)
        for i in key_phrases:
            if element.find(i)!= -1:
                in_key_phrases = True
                phrase = i
                break #finds if the label matches one of the key phrases
        if in_key_phrases == True:
            print( 'EPIC ID ', stars.index[EPIC],': pre-main sequence!!!')
            pms_stars.loc[stars.index[EPIC]] = stars.loc[stars.index[EPIC]]
            pms_stars.loc[stars.index[EPIC]]["Classification"] = phrase
            
            
            
            #appends the star's EPIC ID and label into the PMS dataframe
        else:
            print( 'EPIC ID ', stars.index[EPIC],': NOT pre-main sequence')
        #-------------------------------------------------------------------------------------------------------------
        #-------------------------------------------------------------------------------------------------------------
    except IndexError: #checks if the given EPIC ID is even in the SIMBAD database
        print('EPIC ID ', stars.index[EPIC], ': not in database')

driver.quit() #closes the web page
    
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
print("End of Program")