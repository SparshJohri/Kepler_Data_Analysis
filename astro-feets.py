# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

#works on Spyder

from lightkurve import search_targetpixelfile
import feets
import feets.datasets as dataset
import feets.datasets.synthetic as syn
from scipy import stats
from matplotlib import pyplot as plt

import sys


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
df=pd.read_csv("CodyTable.csv")
epic_ids= df.iloc[ : ,0]

ds=syn.create_normal(0, 1, 0, .0008, seed=42)
print(ds.data.B)

#sys.exit(0)
epic_ids= [203382255]
for id in epic_ids:
    pixelfile = search_targetpixelfile(id).download(quality_bitmask='hardest')
    lc = pixelfile.to_lightcurve(aperture_mask='all');
    
    epic_data = {
        "I": {
            "time":lc.time,
            "magnitude": lc.flux,
            "error": lc.flux_err}
    }
    #f_lc = dataset.base.LightCurve(lc.time,lc.flux,lc.flux_err)
    flc = dataset.base.Data(id=str(id), ds_name='K2', \
                               description='Cody paper',bands=('I'), \
                               metadata=None,data=epic_data)
    plt.plot(flc.data.I.time, flc.data.I.magnitude, '-')
    plt.savefig('\\temp\\'+str(id)+'.png' , format='png',dpi=400)   
    plt.show()
    
    #lc.plot()
    #break
    

sys.exit(0)

driver = webdriver.Chrome('chromedriver.exe')
pms= list()
i=0
for id in epic_ids:
    i= i+1
    
    page = 'http://simbad.u-strasbg.fr/simbad/sim-id?Ident=EPIC+'+str(id)\
    +'&submit=submit+id'
    #print('\n getting page: ',page)
    driver.get(page) #get the page
    
    try:
        ids = driver.find_elements_by_xpath("//*[contains(@id,'basic_data')]") 
        path = '//*[@id="' + ids[0].get_attribute('id') +'"]/table/tbody/tr/td/font' 
        element = driver.find_elements_by_xpath(path) 
        #print(element[0].text)
        #print(' ') table/tbody/tr[5]
        if(element[0].text.find('T Tau-type Star') != -1 or 
                element[0].text.find('Pre-main sequence Star') != -1 or
                element[0].text.find('Emission-line Star') != -1 or
                element[0].text.find('Young Stellar Object') != -1 or
                element[0].text.find('Flare Star') != -1 or
                element[0].text.find('Variable Star of Orion Type') != -1 or
                element[0].text.find('Brown Dwarf') != -1 or
                element[0].text.find('Star in Association') != -1
                ):
            print( 'EPIC ',id,' is a PMS star')
            pms.append(id)
            try:
                spt = 'Nan'
                
                #soectral type is somewhere row 6-9; you have to search for it
                for index in range(6,9):
                    #print(index)
                    path = '//*[@id="' + ids[0].get_attribute('id') +'"]/table/tbody/tr['+str(index)+']/td'
                    element = driver.find_elements_by_xpath(path) 
                    #print('... ',element[0].text)
                    if(element[0].text.find('Spectral type:') != -1):
                        spt = element[0].text
                        break
            except IndexError:
                 pass     
            #print(spt)
            if( spt.find('Nan') == -1) :
                path = '//*[@id="' + ids[0].get_attribute('id') +'"]/table/tbody/tr['+str(index)+']/td[2]/b/tt' 
                element = driver.find_elements_by_xpath(path)    
                spt = element[0].text
            print(spt+'\n')
    except IndexError:
        print('not found') 
        
#time.sleep(600)       
print( 'PMS stars found: ',len(pms)) 
'''
driver.get('http://simbad.u-strasbg.fr/simbad/sim-id?Ident=EPIC+2037866955&submit=submit+id') #get the page
try:
    ids = driver.find_elements_by_xpath("//*[contains(@id,'basic_data')]") 
    path = '//*[@id="' + ids[0].get_attribute('id') +'"]/table/tbody/tr/td/font' 
    element = driver.find_elements_by_xpath(path) 
    print(element[0].text)
except IndexError:
    print('not found')


#return structure fo the targetpixelfile
#http://docs.lightkurve.org/api/lightkurve.targetpixelfile.KeplerTargetPixelFile.html#lightkurve.targetpixelfile.KeplerTargetPixelFile
tpf = search_targetpixelfile(203382255).download();
print("Mission:",tpf.mission,"  Campaign:", tpf.campaign, "  Tahrget:KIC", tpf.targetid)
print('Quality',tpf.quality)
print('cadence no', tpf.cadenceno)
#print(tpf.show_properties())


#tpf.plot(frame=1)

#integrate each frame with "aperture method"
#and create a time series of intensity
lc = tpf.to_lightcurve();
lc.plot()
'''

driver.quit()
print('Done')