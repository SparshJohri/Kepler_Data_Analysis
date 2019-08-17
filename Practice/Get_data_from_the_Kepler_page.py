# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 19:18:59 2019

@author: bhata

You will have to download the webdriver into your file explorer. The path for your driver will almost certainly be different than the one for me.

"""
from selenium import webdriver
import pandas
import numpy
from collections import Counter


driver = webdriver.Chrome('C:\\Users\\bhata\\Documents\\K2fov\\Web Scraping\\chromedriver.exe') 
#establishes the driver

driver.get('https://keplerscience.arc.nasa.gov/k2-approved-programs.html') #gets the page

ids = driver.find_elements_by_xpath("//*[contains(@id,'campaign-2')]") 
campaign_ids = list()
for i in ids:
    campaign_ids.append(i.get_attribute('id')) #finds campaign-2

information = list() #this will get the EPIC ID's within each program

i = campaign_ids[0] #establishes that we're only looking at campaign 2

path = '//*[@id="' + i +'"]/div[1]/div[2]/table[1]/tbody[1]/tr' 
#this is where the data in the table is

programs = driver.find_elements_by_xpath(path)
print(len(programs)) #how many programs there are

labels = list() #will hold the names of each program

for tr_value in range(1, len(programs)+1):
    path = '//*[@id="' + i +'"]/div[1]/div[2]/table[1]/tbody[1]/tr['+str(tr_value)+']/td[4]/a' 
    #the path for the data   
    path1 = '//*[@id="' + i +'"]/div[1]/div[2]/table[1]/tbody[1]/tr['+str(tr_value)+']/td[1]' 
    #the path for the name of the program
    
    label = driver.find_elements_by_xpath(path1)[0].text
    labels.append(label) #appends the name of the program into the list of labels
    
    m_dwarfs = driver.find_elements_by_xpath(path)[0] #gets to the right place in the table
    csv_file=(m_dwarfs.get_attribute("href")) #gets the URL
    
    print(87-tr_value, " files left.")
    
    csv_file = pandas.read_csv(csv_file) #gets the data and puts it into a dataframe
    camp = list()
    for j in range(len(csv_file)):
        camp.append(2)
    csv_file = csv_file.assign(Campaign = camp) #adds in the campaign number as a column    
    csv_file.set_index('EPIC ID', inplace=True, drop = True) 
    #sets up the EPIC ID's as the index of the csv file
    
    information.append(csv_file)
    #appends the csv file into a list of programs, each program containing a list of epic ID's
    
 
information = pandas.Series(information, index = labels) #converts "information" into a Series
print("Information series created.")
print("Query by program number")
print(information.index)

information1 = pandas.DataFrame(columns = information[0].columns) #establishes information1

for i in range(len(information)):
    information1 = information1.append(information[i]) 
    #appends each of the EPIC ID's in information into a dataframe, irrespective of program
    #redundant entries exist because some EPIC ID's are used in multiple programs

my_dataframe = pandas.DataFrame(columns = information1.columns) 
#establishes the final dataframe we will refer to
uniques = dict(Counter(information1.index)) 
#gets the unique EPIC ID's and how many times each one occurs; puts it into a dictionary

my_counter = 0 
for i in uniques:
    if uniques[i]!=1:
        my_dataframe.loc[i]=information1.loc[i].iloc[0] 
        #if an EPIC ID occurs more than once, 
        #query "information1" and only put in the first value into "my_dataframe"
    else:
        if type(information1.loc[i][information1.columns[0]])!=str:
            my_dataframe.loc[i] = information1.loc[i] 
        #if an EPIC ID only occurs once, 
        #query "information1" and put the output of the query into "my_dataframe"
    
    my_counter += 1
    if (my_counter%300) == 0:
        print(my_counter/300)

data = my_dataframe #gives the data a nicer name than "my_dataframe"

export_csv = data.to_csv (r'C:\Sparsh Johri 2019\Kepler Data\Campaign_2_EPICS.csv')
print("End of Program")
driver.quit()


    