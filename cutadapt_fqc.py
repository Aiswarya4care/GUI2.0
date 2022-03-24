import os
import globalv
import config_gui
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from importlib import reload

#current working directory
global GUIpath
GUIpath=os.getcwd()

def cafa():
    reload(globalv)
    dragen_bed=globalv.dragen_bed
    sample_type=globalv.sample_type
    location= globalv.location
    proj=globalv.proj

    #fetching project id from config_gui file
    proj_somatic_dna=config_gui.proj_somatic_dna
    proj_germline=config_gui.proj_germline
    proj_somatic_rna=config_gui.proj_somatic_rna

#retrieving sample name 
    file_list=os.listdir(location)
    if 'cutadaptlog' in file_list:
        os.system("rm " + location + "/cutadaptlog")
    if 'temp1.sh' in file_list:
        os.system("rm " + location + "/temp1.sh")
   
    
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

#project selection and project id retrieval
    
    if sample_type=="Somatic DNA":
        pid= proj_somatic_dna
        adapter='AGATCGGAAGAGC'
        
    elif sample_type=="Somatic RNA":
        pid= proj_somatic_rna
        adapter='CTGTCTCTTATACACATCT'
    else:
        pid= proj_germline
        adapter='AGATCGGAAGAGC'

    #Coping the shell script and modifying the content  
    loc_cafqdra_file= GUIpath + '/CA_FQ_Dragen/ca_fq_dragen.sh'     
    os.system('cp '+ loc_cafqdra_file + ' ' + location) 
    
    #giving the necessary permissions
    os.chdir(location)
    os.system('chmod 777 *')

    #modifying the annotation_mod.sh file
    cafqdrafile=location+'/ca_fq_dragen.sh'
    # Read in the file
    with open(cafqdrafile, 'r') as file :
        filedata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
        filedata = filedata.replace('{{adapter}}', adapter)
        filedata = filedata.replace('{{location}}', location)
        filedata = filedata.replace('{{pid}}', pid)
    
    # Write the file out again
    with open(cafqdrafile, 'w') as file:
        file.write(filedata)

    os.system("mkdir "+ location+ "/cutadaptlog")
    
    
    ###location and info
    print("################################")
    print("######### INFORMATION ##########")
    print("################################")
    print("Selected Project is " + str(proj))
    print("Project ID is " + str(pid))
    print("Adapter information: " + str(adapter))
    print("Data located in: " + str(location))
    print("No. of files selected is " + str(len(os.listdir(location))-2))
    a = ("Selected Project is " +
       str(proj) + "\n" +
       "Project ID is " +
       str(pid) + "\n" +
       "Data located in: "+
       str(location))
    answer = tk.messagebox.askyesnocancel("Confirmation", a)
    if answer:
        print("################################")
        print("############ Running FQ and Cutadapt ###########")
        print("################################")
        
        temp1_path= location + "/" + "temp1.sh"
        os.system("sh " + temp1_path)
        print("################################")
        print("############ Done ###########")
        print("################################")
    else:
        rm_cmd=" rm "+ location + "/" + "temp1.sh"
        os.system(rm_cmd) 
