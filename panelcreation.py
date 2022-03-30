import os
import pandas as pd
import numpy as np
import config_gui
import tkinter as tk
from importlib import reload

import globalv

def panel():
    reload(globalv)
    location= globalv.location
    sample_type=globalv.sample_type
    projectdir=globalv.projectdir
    panel_bed=globalv.panel_bed

    file_list=os.listdir(location)

    if 'panel' in file_list:
        os.system("rm -r " + location + "/panel")

    
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
        
    mkdir="mkdir "+ location+ "/panel"
    os.system(mkdir)
    panelcreate= location +  "/panel/panelcreate.sh"
    f1= open(panelcreate,"x")
    f1.close()
    f1= open(panelcreate,"w+")
    f1.write("cd "+ location + "/panel" + '\n')
    
    if sample_type=="Somatic DNA":
        for s in samples:
            f1.write("cp "+ str(projectdir) + "/AppResults/" + s)
            f1.write("/Files/"+s+ ".hard-filtered.vcf.gz "+ location+ "/panel"+ '\n')
            f1.write('\n')
            f1.write("gzip -dk "+ s+ ".hard-filtered.vcf.gz" + '\n')
            f1.write('\n')
            f1.write("/home/ubuntu/Programs/./bedtools.static.binary intersect -header -a " + s+".hard-filtered.vcf -b /home/ubuntu/Patient_samples/bed_files/panel_bed_files/")
            f1.write(str(panel_bed)+ " > " + s + ".hard-filtered_panel.vcf")
            f1.write('\n'+ "rm -rf "+ s + ".hard-filtered.vcf")
            f1.write('\n' + "############" +'\n')
        f1.write('\n' +"echo \"######################\"")
        f1.write('\n' +"echo \"######### DONE #########\"")
        f1.write('\n' +"echo \"######################\"")
        f1.close()  
    
    elif sample_type=="Germline":
        for s in samples:
            f1.write("cp "+ str(projectdir) + "/AppResults/" + s)
            f1.write("/Files/"+s+ ".hard-filtered.vcf.gz "+ location+ "/panel"+ '\n')
            f1.write('\n')
            f1.write("gzip -dk "+ s+ ".hard-filtered.vcf.gz" + '\n')
            f1.write('\n')
            f1.write('\n' + "############" +'\n')
        f1.write('\n' +"echo \"######################\"")
        f1.write('\n' +"echo \"######### DONE #########\"")
        f1.write('\n' +"echo \"######################\"")
        f1.close()
    
    answer = tk.messagebox.askyesnocancel("Confirmation", "Run panel creation process?")    
   
    if answer:
        print("################################")
        print("############ Creating panel vcfs ###########")
        print("################################")
        panelcreate_path= location + "/panel/" + "panelcreate.sh >" + location+ "/panel/panellog.txt"
        os.system("bash " + panelcreate_path)
        print("################################")
        print("############ Panel Created ###########")
        print("################################")
        
    else:
        print("###### Panel Creation Aborted #####")
