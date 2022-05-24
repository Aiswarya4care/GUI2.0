import os
import globalv
import config_gui
import pandas as pd
import numpy as np
import tkinter as tk
from importlib import reload
from config_gui import dra_bed_ids
from config_gui import projectid

def dragen39():

    reload(globalv)
    GUIpath=config_gui.GUIpath
    location= globalv.location
    capturingkit=globalv.capturing_kit
    sample_type=globalv.sample_type
    appsess=globalv.appsess
    bed_id=dra_bed_ids[capturingkit]
    projectdir=globalv.projectdir

    
    #fetching project id from config_gui file
    pid= projectid[sample_type]

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
    
    if sample_type=="DNA [FFPE, FF]":
        adapter='AGATCGGAAGAGC'
        bscmd= "bs launch application -n \"DRAGEN Enrichment\" --app-version 3.9.5 -o project-id:" + pid + " -o app-session-name:"+ appsess +"  -l "+ appsess +"  -o vc-type:1 -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:" + str(bed_id) + " -o input_list.sample-id:$bsids -o picard_checkbox:1 -o af-filtering:1  -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o sq-filtering:1 -o tmb:1 -o vc-hotspot:26309592242 -o baseline-noise-bed:25849773923 -o vcf-site-filter:1 -o cnv_checkbox:1 -o cnv_ref:1 -o cnv_segmentation_mode:cbs -o cnv-filter-qual:50.0 -o cnv-baseline-id:25791243964,25791291016,25791291033,25791291050,25791406163,25791440084,25791528878,25791528895,25791582119,25791582931,25791595964,25791595981,25791598767,25791637964,25791670919,25791679146,25791679164,25791681916,25791681933 -o cnv_gcbias_checkbox:1 -o hla:1 -o commandline-disclaimer:true -o arbitrary:\"--read-trimmers:adapter --trim-adapter-read1\" -o additional-file:25600057590 -o automation-sex:unkown"


    #Coping the shell script and modifying the content  
    loc_cafqdra_file= GUIpath.split('/codes/')[0] + '/ca_fq_dragen/dragen39.sh'     
    os.system('cp '+ loc_cafqdra_file + ' ' + location) 
    print(loc_cafqdra_file)
    print(location)
    #giving the necessary permissions
    os.chdir(location)
    os.system('chmod 777 *')

    #modifying the annotation_mod.sh file
    dragen39file=location+'/dragen39.sh'
    # Read in the file
    with open(dragen39file, 'r') as file :
        filedata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
        filedata = filedata.replace('{{samplenames}}', str(samples).strip("[]").replace("'","").replace(",",""))
        filedata = filedata.replace('{{adapter}}', adapter)
        filedata = filedata.replace('{{location}}', location)
        filedata = filedata.replace('{{bscmd}}', bscmd)
        filedata = filedata.replace('{{pid}}', pid)
    
    # Write the file out again
    with open(dragen39file, 'w') as file:
        file.write(filedata)

    os.system("mkdir "+ location+ "/cutadaptlog")
    


    dragen39file=location+'/dragen39.sh'
    with open(dragen39file, 'w') as file:
        file.write(bscmd)

   
 ###location and info
    print("################################")
    print("######### INFORMATION ##########")
    print("################################")
    print("Selected project directory is " + str(projectdir))
    print("No. of files selected is " + str(len(samples)))
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
        os.system("bash " + dragen39file)
        print("################################")
        print("############ Done ###########")
        print("################################")
        
    else:
        rm_cmd=" rm "+ dragen39file
        os.system(rm_cmd) 

