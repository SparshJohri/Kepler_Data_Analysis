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
from scipy import signal
import numpy as np

import sys


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n



df=pd.read_csv("CodyTable.csv")
epic_ids= df.iloc[ : ,0]

 

#sys.exit(0)
#fig2=[203954898, 203905576, 203928175, 203382255, 204233955]
epic_ids= [204342099]
for id in epic_ids:
    pixelfile = search_targetpixelfile(id).download(quality_bitmask='hardest')
    lc = pixelfile.to_lightcurve(aperture_mask='all');
    print(lc)
    #lc=lc.remove_outliers(sigma=5)
    #lc.flux=signal.medfilt(lc.flux,25) 
    #lc.flux=signal.wiener(lc.flux,55) 
    #lc2_flux=signal.savgol_filter(lc.flux,15,7 ) 
    
    epic_data = {
        "I": {
            "time":lc.time,
            "magnitude": lc.flux,
            "error": lc.flux_err}
    }
    avg = 5
    lc.flux = moving_average(lc.flux,avg)
    lc.time = moving_average(lc.time,avg)
    print(len(lc.flux))    
    
    flc = dataset.base.Data(id=str(id), ds_name='K2', \
                               description='Cody paper',bands=('I'), \
                               metadata=None,data=epic_data)
    #plt.plot(flc.data.I.time, flc.data.I.magnitude, '-')
    print(str(id))
    #plt.savefig('\\temp\\'+str(id)+'.png' , format='png',dpi=400)   
    #plt.show()
    print('\n\n')
    lc.plot()
    #break
    
print('\n\n\n')
sys.exit()

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