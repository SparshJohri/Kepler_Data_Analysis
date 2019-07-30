# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 19:18:59 2019

@author: bhata

You will have to download the webdriver into your file explorer. The path for your driver will almost certainly be different than the one for me.

"""
from selenium import webdriver
import pandas
import numpy


driver = webdriver.Chrome('C:\\Users\\bhata\\Documents\\K2fov\\Web Scraping\\chromedriver.exe')
driver.get('https://keplerscience.arc.nasa.gov/k2-approved-programs.html') #get the page
ids = driver.find_elements_by_xpath("//*[contains(@id,'campaign-2')]")
campaign_ids = list()
for i in ids:
    campaign_ids.append(i.get_attribute('id'))

information = list()
i = campaign_ids[0]
path = '//*[@id="' + i +'"]/div[1]/div[2]/table[1]/tbody[1]/tr'
programs = driver.find_elements_by_xpath(path)
print(len(programs))
labels = list()

for tr_value in range(1, len(programs)):
    path = '//*[@id="' + i +'"]/div[1]/div[2]/table[1]/tbody[1]/tr['+str(tr_value)+']/td[4]/a' #the path   
    path1 = '//*[@id="' + i +'"]/div[1]/div[2]/table[1]/tbody[1]/tr['+str(tr_value)+']/td[1]'
    
    label = driver.find_elements_by_xpath(path1)[0].text
    labels.append(label)    
    
    m_dwarfs = driver.find_elements_by_xpath(path)[0] #gets to the right place in the table
    csv_file=(m_dwarfs.get_attribute("href")) #gets the URL
    print(87-tr_value, " files left.")
    csv_file = pandas.read_csv(csv_file)
    camp = list()
    for j in range(len(csv_file)):
        camp.append(2)
    csv_file = csv_file.assign(Campaign = camp) #adds in the campaign number as a column
    csv_file.set_index('EPIC ID', inplace=True, drop = True)
    information.append(csv_file)
    
 
information = pandas.Series(information, index = labels)
print("Information series created.")
print("Query by program number")
print(information.index)

information1 = pandas.DataFrame(columns = information[0].columns)
information1["Program"] = numpy.NaN

place = 0

for i in range(len(information)):
    information1 = information1.append(information[i])


lengths = list()
for i in range(86):
    lengths.append(len(information[i]))

for i in range(1, 86):
    lengths[i] = lengths[i]+lengths[i-1]
    
place = 0

for i in range(len(information1)):
    if i==lengths[place]:
        place += 1
        print("Done with program number ", place)
    information1["Program"].iloc[i] = [information.index[place]]


print(information1)


print("End of Program")
driver.quit()