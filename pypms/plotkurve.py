# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 19:40:41 2019

@author: lokes
"""
import bokeh
import lightkurve as lk
import pandas
import pathlib
import os
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact
import ipywidgets as widget
import pandas

#from google.colab import files

print("Imports done.")


def outlier_removal(lc, sigma_value):
    lc = lc.remove_outliers(sigma = sigma_value)
    return lc #removes outliers

def plot_EPIC_ID(epic, bitmask, remove_outlier = True, sigma_value = 5):
    pixelfile = lk.search_targetpixelfile(epic).download(quality_bitmask=bitmask) #gets the data about the EPIC ID
    #fluxes = pixelfile.flux
    #print(np.std(fluxes[154]))
    #print(fluxes)
    
    #pixelfile.plot(frame = 128)
    #pixelfile.plot(frame = 0)
    fname = str(epic)+'.fits'
               
    lc = pixelfile.to_lightcurve(aperture_mask='all') #gets the light curve information
    if remove_outlier == True:
        lc = outlier_removal(lc, sigma_value) #calls the function that removes outliers
        print("Outliers removed")
    else:
        print("Outliers remain")
    lc.to_fits(path=fname, overwrite=True)
    #files.download(fname)    
    return lc, pixelfile #returns the light curve information

print("Functions defined.")


campaign_epics = pandas.read_csv("https://raw.githubusercontent.com/SparshJohri/Kepler_Data_Analysis/master/Campaign_2_EPICS.csv")
campaign_epics = list(campaign_epics[campaign_epics.columns[0]])
cody_epics = pandas.read_csv("https://raw.githubusercontent.com/SparshJohri/Kepler_Data_Analysis/master/CodyTable.csv")
cody_epics = list(cody_epics[cody_epics.columns[0]])

def epic_plotter(targets, bitmask_qual, remove_outlier):
    flux = []
    time = []
    light_curve_info, pxfl = plot_EPIC_ID(targets, bitmask_qual, remove_outlier) #gets the light curve information for the ith EPIC ID in targets
    flux.append(light_curve_info.flux) #gets the flux data about the ith EPIC ID, and adds it to the list of information about the fluxes of all the EPIC ID's
    time.append(light_curve_info.time) #gets the time data about the ith EPIC ID, and adds it to the list of information about the times of all the EPIC ID's
    data = pandas.DataFrame({"Time":time[-1], "Flux":flux[-1]}) #creates a dataframe with the time and flux
    data.set_index(data.columns[0], inplace=True, drop = True) #sets the time as the index for finding the flux

    flux = list(data["Flux"]) #gets the flux data about the EPIC ID
    time = list(data.index) #gets the time information about the EPIC ID
    plt.plot(time, flux) #plots using matplotlib
    light_curve_info.plot() #plots using the lightkurve.plot function
    pxfl.interact()
    plt.show() #shows the plots

target_list = cody_epics
interact(epic_plotter, targets = target_list, bitmask_qual = ["none","default", "hard", "hardest"], remove_outlier = [True, False])