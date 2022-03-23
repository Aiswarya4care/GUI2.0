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

def cafadra():
    reload(globalv)
    location= globalv.location
    libkit=globalv.libkit
    proj=globalv.proj
    appsess=globalv.appsess
    bed_id=globalv.bed_id
    
    #fetching project id from config_gui file
    proj_somatic_dna=config_gui.proj_somatic_dna
    proj_germline=config_gui.proj_germline
    proj_somatic_rna=config_gui.proj_somatic_rna
    fastqc= config_gui.fastqc

    #retrieving sample names 
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
    
    #kit chosen and retrieving adapters 
    
    if libkit=="Illumina":
        bed_file_info= "fixed-bed:Illumina_Exome_TargetedRegions_v1.2"
        adapter="CTGTCTCTTATACACATCT"
              
    else:
        bed_file_info= "fixed-bed:custom -o target_bed_id:"+ str(bed_id)
        adapter="AGATCGGAAGAGC"
        

#project selection and project id retrieval
    
    if proj=="Somatic DNA":
        pid= proj_somatic_dna
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l " + appsess +" -o project-id:" + pid + " -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o " + bed_file_info + " -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o commandline-disclaimer:true"
        
    elif proj=="Somatic RNA":
        pid= proj_somatic_rna
        cmd="bs launch application -n \"DRAGEN RNA Pipeline\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:" + pid + " -o sample-id:$bsids -o ht-ref:hg19-altaware-cnv-anchor.v8 -o gene_fusion:1 -o quantification_checkbox:1 -o commandline-disclaimer:true"
    
    else:
        pid= proj_germline
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id" + pid + " -o vc-type:0 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o " + bed_file_info + " -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o sv_checkbox:1 -o commandline-disclaimer:true"

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
        filedata = filedata.replace('{{samplenames}}', str(samples).strip("[]").replace("'","").replace(",",""))
        filedata = filedata.replace('{{adapter}}', adapter)
        filedata = filedata.replace('{{location}}', location)
        filedata = filedata.replace('{{fastqc}}', fastqc)
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
    print("No. of files selected is " + str(len(os.listdir(location))-2))
    print("Data located in: " + str(location))
    a = ("Selected Project is " +
       str(proj) + "\n" +
       "Project ID is " +
       str(pid) + "\n" +
       "Data located in: "+
       str(location))
    answer = tk.messagebox.askyesnocancel("Confirmation", a)    
   
    if answer:
        
        print("################################")
        print("############ Running it all together ###########")
        print("################################")
        
        temp1_path= location + "/" + "temp1.sh"
        os.system("bash " + temp1_path)
        print("################################")
        print("############ Done ###########")
        print("################################")
        
    else:
        rm_cmd=" rm "+ location + "/" + "temp1.sh"
        os.system(rm_cmd) 
