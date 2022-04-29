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
from config_gui import dra_bed_ids

#current working directory
global GUIpath
GUIpath=os.path.realpath(__file__).split('main.py')[0]

def cafadra():
    reload(globalv)
    location= globalv.location
    capturingkit=globalv.capturing_kit
    sample_type=globalv.sample_type
    appsess=globalv.appsess
    bed_id=dra_bed_ids[capturingkit]
    projectdir=globalv.projectdir

    #fetching project id from config_gui file
    proj_somatic_dna=config_gui.proj_somatic_dna
    proj_germline=config_gui.proj_germline
    proj_somatic_rna=config_gui.proj_somatic_rna
    fastqc= config_gui.fastqc
    

    #retrieving sample names 
    file_list=os.listdir(location)
       
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
        pid= proj_somatic_dna
        adapter='AGATCGGAAGAGC'
        bscmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:" + pid + " -o vc-type:0 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:" + str(bed_id) + " -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o sv_checkbox:1 -o commandline-disclaimer:true"
        
    elif sample_type=="RNA":
        pid= proj_somatic_rna
        bscmd="bs launch application -n \"DRAGEN RNA Pipeline\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:" + pid + " output_format:BAM -o coverage_list.coverage_bed_id:Numeric-ID -o sample-id:$bsids -o ht-ref:hg19-altaware-cnv-anchor.v8 -o gene_fusion:1 -o quantification_checkbox:1 -o commandline-disclaimer:true"
        adapter='CTGTCTCTTATACACATCT'
    
    elif sample_type=="DNA [cf]":
        pid= proj_somatic_rna
        bscmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:" + pid + " -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:" + str(bed_id) + " -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o liquid_tumor:1 -o vc-af-call-threshold:1 -o vc-af-filter-threshold:5 -o sv_checkbox:1 -o commandline-disclaimer:true"
        adapter='CTGTCTCTTATACACATCT'

    else:
        pid= proj_germline
        adapter='AGATCGGAAGAGC'
        bscmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:" + pid + " -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:" + str(bed_id) + " -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o commandline-disclaimer:true"
        

    #Coping the shell script and modifying the content  
    loc_cafqdra_file= GUIpath.split('/codes/')[0] + '/ca_fq_dragen/ca_fq_dragen.sh'     
    os.system('cp '+ loc_cafqdra_file + ' ' + location) 
    print(loc_cafqdra_file)
    print(location)
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
        filedata = filedata.replace('{{bscmd}}', bscmd)
        filedata = filedata.replace('{{pid}}', pid)
    
    # Write the file out again
    with open(cafqdrafile, 'w') as file:
        file.write(filedata)

    os.system("mkdir "+ location+ "/cutadaptlog")
    
 ###location and info
    print("################################")
    print("######### INFORMATION ##########")
    print("################################")
    print("Selected project directory is " + str(projectdir))
    print("Project ID is " + str(pid))
    print("Adapter information: " + str(adapter))
    print("No. of files selected is " + str(len(os.listdir(location))-2))
    print("Data located in: " + str(location))
    a = ("Selected Project is " +
       str(projectdir) + "\n" +
       "Project ID is " +
       str(pid) + "\n" +
       "Data located in: "+
       str(location))
    answer = tk.messagebox.askyesno("Confirmation", a)    
   
    if answer:
        
        print("################################")
        print("############ Running it all together ###########")
        print("################################")
        
        cafqdra_script_path= location + "/" + "ca_fq_dragen.sh"
        os.system("bash " + cafqdra_script_path)
        print("################################")
        print("############ Done ###########")
        print("################################")
        
    else:
        rm_cmd=" rm "+ location + "/" + "ca_fq_dragen.sh"
        os.system(rm_cmd) 