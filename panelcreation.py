import os
import pandas as pd
import numpy as np
import warnings
import re
import tkinter as tk
from tkinter import filedialog
from importlib import reload

import globalv

def panel():
    reload(globalv)
    location= globalv.location
    sample_type=globalv.sample_type
    projectdir=globalv.projectdir

    file_list=os.listdir(location)

    if 'panel' in file_list:
        os.system("rm -r " + location + "/panel")

    bed_file_loc=globalv.dragen_bed_file
    
    samples=[]
    for file in file_list:
        sample= file.split("_")
        samples.append(sample[0])
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()
    if 'temp1.sh' in samples:
        samples.remove('temp1.sh')
    if 'panel' in samples:
        samples.remove('panel')
    if 'panellog.txt' in samples:
        samples.remove('panellog.txt')
    if 'cutadaptlog.txt' in samples:    
        samples.remove('cutadaptlog.txt')
    if 'FQlog.txt' in samples:    
        samples.remove('FQlog.txt')
    if 'MSI' in samples:
        samples.remove('MSI')
    if 'CNV' in samples:
        samples.remove('CNV')
    if 'cutadaptlog' in samples:
        samples.remove('cutadaptlog') 
        
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
            f1.write(str(bed_file_loc)+ " > " + s + ".hard-filtered_panel.vcf")
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
        rm_cmd=" rm "+ location + "/panel/" + "panelcreate.sh"
        os.system(rm_cmd) 
