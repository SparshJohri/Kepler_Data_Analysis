import lightkurve as lk
import pandas
import pathlib
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def hello():
    print('hello world!')
def outlier_removal(lc, sigma_value):
    lc = lc.remove_outliers(sigma = sigma_value)
    return lc #removes outliers

def plot_EPIC_ID(epic, sigma_value = 5):
    search = lk.search_targetpixelfile(epic, mission='K2')
    print(search)
    pixelfile = search.download(quality_bitmask='hard' ) #gets the data about the EPIC ID
    print('*********Quarter :' ,pixelfile.quarter, 'Mission : ',pixelfile.mission )
    #pixelfile.interact(notebook_url='localhost:8893')
    fname = str(epic)+'.fits'
               
    lc = pixelfile.to_lightcurve(aperture_mask='all') #gets the light curve information
    lc = outlier_removal(lc, sigma_value) #calls the function that removes outliers
    lc.to_fits(path=fname, overwrite=True)
    # files.download(fname)    
    return lc #returns the light curve information
print("Functions defined.")