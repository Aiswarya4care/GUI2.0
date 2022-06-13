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
from config_gui import projectid

def cafa():
    GUIpath=config_gui.GUIpath
    reload(globalv)
    sample_type=globalv.sample_type
    location= globalv.location
    
    #fetching project id from config_gui file
    pid= projectid[sample_type]
    fastqc= config_gui.fastqc

#retrieving sample name 
    file_list=os.listdir(location)
    if 'cutadaptlog' in file_list:
        os.system("rmdir " + location + "/cutadaptlog")
    if 'ca_fq.sh' in file_list:
        os.system("rm " + location + "/ca_fq.sh")
   
    
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
    
    if sample_type=="DNA [Blood]":
        adapter='AGATCGGAAGAGC'
        
    elif sample_type=="Somatic RNA":
       adapter='CTGTCTCTTATACACATCT'
    else:
        adapter='AGATCGGAAGAGC'

    #Coping the shell script and modifying the content  
    loc_cafq_file= GUIpath.split('/codes/')[0] + '/ca_fq_dragen/ca_fq.sh'     
    os.system('cp '+ loc_cafq_file + ' ' + location) 
    
    #giving the necessary permissions
    os.chdir(location)
    os.system('chmod 777 *')

    #modifying the annotation_mod.sh file
    cafqfile=location+'/ca_fq.sh'
    # Read in the file
    with open(cafqfile, 'r') as file :
        filedata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
        filedata = filedata.replace('{{adapter}}', adapter)
        filedata = filedata.replace('{{location}}', location)
        filedata = filedata.replace('{{pid}}', pid)
    
    # Write the file out again
    with open(cafqfile, 'w') as file:
        file.write(filedata)

    os.system("mkdir "+ location+ "/cutadaptlog")
    
    
    ###location and info
    a = ("Selected Project is: " +
       str(sample_type) + "\n" +
       "Project ID is: " +
       str(pid) + "\n" +
       "Data located in: "+
       str(location)+ "\n" +
        "No. of files selected is: " + str(len(os.listdir(location))-2))
    
    answer = tk.messagebox.askyesno("Confirmation", a)
    if answer:
        print("################################")
        print("############ Running FQ and Cutadapt ###########")
        print("################################")
        
        cafq_script_path= location + "/" + "ca_fq.sh"
        os.system("sh " + cafq_script_path)
        print("################################")
        print("############ Done ###########")
        print("################################")
   
