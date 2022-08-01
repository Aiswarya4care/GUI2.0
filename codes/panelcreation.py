import os
import pandas as pd
import numpy as np
import config_gui
import tkinter as tk
from importlib import reload
from config_gui import GUIpath, testprefix, capkitsuffix, bedtools
import glob

import globalv

def panel():
    reload(globalv)
    location= globalv.location
    sample_type=globalv.sample_type
    projectdir=globalv.projectdir
    capturingkit=globalv.capturingkit
    test=globalv.test

    ########### selecting the panel bed file #############
    print(test)
    prefix=testprefix[test]
    print(capturingkit)
    suffix=capkitsuffix[capturingkit]

    panel_bed= GUIpath + '/bed_files/panel_bed_files/' + str(test)+ "/" + prefix + suffix
    
    if 'panel' in os.system(location):
                os.system("rm -r " + location + "/panel")   
    
    
    file_list=glob.glob(location+"/*_R1_fastqc.html")
    samples=[s.split('/')[-1] for s in file_list]
    samples=[s.split('_R1')[0] for s in samples]
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()


    print(samples)

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
            f1.write('chmod 777 *')
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
            f1.write('chmod 777 *')
            f1.write('\n')
            f1.write("gzip -dk "+ s+ ".hard-filtered.vcf.gz" + '\n')
            f1.write('\n')
            f1.write(bedtools + " intersect -header -a " + s+".hard-filtered.vcf -b ")
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
