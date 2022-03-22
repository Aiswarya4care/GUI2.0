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
    libkit=globalv.libkit
    proj=globalv.proj
    file_list=os.listdir(location)
    if 'panel' in file_list:
        os.system("rm -r " + location + "/panel")
 #kit chosen and retrieving adapters 
    if libkit=="Roche":
        bed_file_loc= "roche_hg19_panel.bed"
    elif libkit=="Illumina":
        bed_file_loc="CEX_illumina_nextera_panel.bed"
    else:
        bed_file_loc="New_agilent_panel.bed"

#project selection and project id retrieval
    if proj=="Somatic DNA":
        proj_dest="Somatic_Patient_Samples_3"
    elif proj=="Somatic RNA":
        proj_dest="Somatic_Patient_RNA"
    else:
        proj_dest="Germline_Patient_Sample"
    
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
    temp2= location +  "/panel/temp2.sh"
    f1= open(temp2,"x")
    f1.close()
    f1= open(temp2,"w+")
    f1.write("cd "+ location + "/panel" + '\n')
    
    if proj=="Somatic DNA":
        for s in samples:
            f1.write("cp /home/ubuntu/basespace/Projects/"+ str(proj_dest) + "/AppResults/" + s)
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
    
    elif proj=="Germline":
        for s in samples:
            f1.write("cp /home/ubuntu/basespace/Projects/"+ str(proj_dest) + "/AppResults/" + s)
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
        temp2_path= location + "/panel/" + "temp2.sh >" + location+ "/panel/panellog.txt"
        os.system("bash " + temp2_path)
        print("################################")
        print("############ Panel Created ###########")
        print("################################")
        
    else:
        rm_cmd=" rm "+ location + "/panel/" + "temp2.sh"
        os.system(rm_cmd) 
