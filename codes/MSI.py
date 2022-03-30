import os
import numpy as np
import pandas as pd
import tkinter as tk
import config_gui
from importlib import reload

import globalv
  
def msi_analysis():
    reload(globalv)
    location= globalv.location
    projectdir=globalv.projectdir
    msisensor=config_gui.msisensor
    msi_microlist= config_gui.msi_microlist

    file_list=os.listdir(location)
    if 'MSI' in file_list:
        os.system("rm -r " + location + "/MSI")   

    samples=[]
    for file in file_list:
        sample= file.split("_")
        samples.append(sample[0])
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()
    
    #Removing default file names from the sample name list
    default_files=config_gui.default_files
    for s in default_files:
        if s in samples:
            samples.remove(s)
    
        
    mkdir="mkdir "+ location+ "/MSI"
    os.system(mkdir)
    msitxt= location +  "/MSI/msi.sh"
    f1= open(msitxt,"x")
    f1.close()
    f1= open(msitxt,"w+")
    f1.write("cd "+ location + "/MSI" + '\n')
    
    for s in samples:
        f1.write('\n' + str(msisensor)+" msi -b 30 -d " + str(msi_microlist)+ " -t ")
        f1.write( str(projectdir) + "/AppResults/" + s)
        f1.write("/Files/"+s+ ".bam ")
        f1.write("-o " + location + "/MSI/" + s + "_msi" + '\n')
    
    f1.write('\n'+"echo \"######################\"")
    f1.write('\n'+"echo \"######### DONE #########\"")
    f1.write('\n'+"echo \"######################\"")
    f1.close()  

    answer = tk.messagebox.askyesnocancel("Confirmation", "Run MSI analysis?")    
   
    if answer:
        print("################################")
        print("############ Running MSI analysis ###########")
        print("################################")
        msi_path= location + "/MSI/" + "msi.sh"
        os.system("bash " + msi_path + "> "+ location + "/MSI/msilog.txt")
        print("################################")
        print("############ MSI completed ###########")
        print("################################")
    else:
        rm_cmd=" rm "+ location + "/MSI/" + "msi.sh"