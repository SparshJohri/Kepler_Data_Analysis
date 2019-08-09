# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 20:10:39 2019

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
campaign = driver.find_elements_by_xpath("//*[contains(@id,'campaign-2')]")[0].get_attribute(('id'))
path = '//*[@id="' + campaign +'"]/ul[1]/li[4]/a' #goes to the appropriate place in the page
print("Path gotten")
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
label = driver.find_elements_by_xpath(path)[0]
URL = label.get_attribute("href") #gets the URL
print("URL gotten")
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
csv_file = pandas.read_csv(URL) #uses the URL to open the csv file into a pandas dataframe
csv_file.set_index('EPIC ID', inplace=True, drop = True) #causes the EPIC ID's to become the indexes of the dataframe
print("File read")
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
for i in range(len(csv_file.columns)-1):
    data = csv_file[csv_file[csv_file.columns[i]]!=" "]
    #gets the subset of data that doesn't have an empty right ascension, declination, or magnitude
print("Data filtered")
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
export_csv = data.to_csv (r'Campaign_2_EPICS.csv') #exports the dataframe as a csv to a file
print("File exported")
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
print("End of Program")
driver.quit() #closes the web page