import lightkurve as lk
import pandas
import pathlib
import os


os.mkdir("EPIC ID Analysis")
def outlier_removal(lc, sigma_value):
    lc = lc.remove_outliers(sigma = sigma_value)
    return lc

def plot_EPIC_ID(epic, sigma_value = 5):    
    #gets the pixelfile data
    pixelfile = lk.search_targetpixelfile(epic).download(quality_bitmask="hardest") #gets the pixel data       
    lc = pixelfile.to_lightcurve(aperture_mask='all') #masks the noisy data
    lc = outlier_removal(lc, sigma_value) #removes remaining outliers
    lc = outlier_removal(lc, sigma_value) #removes remaining outliers
    
    #creates the file path and exports the fits file
    path = pathlib.Path("EPIC ID Analysis"+str(epic)) #creates the path for the EPIC ID; the name of the folder is the EPIC ID
    if path.exists()==False:
        os.mkdir("EPIC ID Analysis\\"+str(epic))
    file = "EPIC ID Analysis\\"+str(epic)+"\\"+str(epic)+"_Info.fits"#path for the fits file; e.g. EPIC ID Analysis/205008727/205008727_Info.fits
    print("Fits directory: ", file)
    lc.to_fits(path=file) #exports the fits file
    lc.plot() #plots the graph
    return lc #returns the lightcurve data

def print_flux_over_time(flux, time, size = None):
    if size == None:
        size = max(len(flux), 20)
    
    print("    Time   |   Flux")
    print("-------------------------")
    for i in range(size):
        print(format(time[i], '.4f'), " | ", flux[i])
        
        
        
campaign_2_pms = pandas.read_csv("Campaign_2_PMS.csv")
pms = list()
for i in range(len(campaign_2_pms)):
    if campaign_2_pms.iloc[i]["Type"] != "Brown Dwarf":
        pms.append(campaign_2_pms.iloc[i]["EPIC ID"])
pms = list()

assigned_targets= [203905576, 203794605, 203725791]#pms
targets = assigned_targets + pms
flux = []
time = []


dataset1 = list()
for i in targets:
    light_curve_info = plot_EPIC_ID(i) #gets the lightcurve information for a particular EPIC ID 
    flux.append(light_curve_info.flux) #gets the flux data for that EPIC ID and records it
    time.append(light_curve_info.time) #gets the time data for that EPIC ID and records it
    data = pandas.DataFrame({"Time":time[-1], "Flux":flux[-1]}) #creates a dataframe with the time and flux
    data.set_index(data.columns[0], inplace=True, drop = True) #sets the time as the queryable index of the EPIC ID data

    file = "EPIC ID Analysis\\"+str(i)+"\\"+str(i)+"_Time_and_Flux.csv" #path for the csv file; e.g. 205008727/205008727_Info.csv
    print("CSV directory: ", file)
    export_csv = data.to_csv(file) #exports the csv file
    print("File exported")
    for k in range(2):
        print()
    dataset1.append(data) #appends the data about that one EPIC ID into a larger dataset with data about every EPIC ID

dataset = pandas.Series(dataset1, index = targets) #sets the EPIC ID as the queryable index of the larger dataset