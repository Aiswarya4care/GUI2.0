import os
import pandas as pd
import numpy as np
import config_gui
import tkinter as tk
from importlib import reload
from config_gui import GUIpath, testprefix, capkitsuffix, bedtools

import globalv

def panel():
    reload(globalv)
    location= globalv.location
    sample_type=globalv.sample_type
    projectdir=globalv.projectdir
    capturingkit=globalv.capturingkit
    test=globalv.test

    ########### selecting the panel bed file #############
    prefix=testprefix[test]
    suffix=capkitsuffix[capturingkit]

    panel_bed= GUIpath.split('codes')[0] + '/bed_files/panel_bed_files/' + str(test)+ "/" + prefix + suffix

    file_list=os.listdir(location)

    if 'panel' in file_list:
        os.system("rm -r " + location + "/panel")

    
    samples=[]
    for file in file_list:
        sample= file.split("_")
        samples.append(sample[0])
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()
    print(samples)
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
    
    if sample_type=="DNA [Blood]":
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
            
    else:        
        for s in samples:
            f1.write("cp "+ str(projectdir) + "/AppResults/" + s)
            f1.write("/Files/"+s+ ".hard-filtered.vcf.gz "+ location+ "/panel"+ '\n')
            f1.write('\n')
            f1.write("gzip -dk "+ s+ ".hard-filtered.vcf.gz" + '\n')
            f1.write('\n')
            f1.write(bedtools + " -header -a " + s+".hard-filtered.vcf -b ")
            f1.write(str(panel_bed)+ " > " + s + ".hard-filtered_" + str(test) +"_panel.vcf")
            f1.write('\n'+ "rm -rf "+ s + ".hard-filtered.vcf")
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
