import os
import globalv
import config_gui
import pandas as pd
import numpy as np
import tkinter as tk
from importlib import reload
from config_gui import dra_bed_ids
from config_gui import projectid

#current working directory
global GUIpath
GUIpath=GUIpath=os.path.realpath(__file__).split('main.py')[0]

def dragen39():
    reload(globalv)
    location= globalv.location
    capturingkit=globalv.capturing_kit
    sample_type=globalv.sample_type
    appsess=globalv.appsess
    bed_id=dra_bed_ids[capturingkit]
    pid=projectid[sample_type]
    projectdir=globalv.projectdir

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
  
    if capturingkit=="sureselectxt_v8_covered.bed":
        bscmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.9.5 -o project-id:" + pid + " -o app-session-name:"+ appsess +"  -l "+ appsess +"  -o vc-type:1 -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:" + str(bed_id) + "-o input_list.sample-id:biosamples/526165645 -o picard_checkbox:1 -o af-filtering:1  -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o sq-filtering:1 -o tmb:1 -o vc-hotspot:26309592242 -o baseline-noise-bed:25849773923 -o vcf-site-filter:1 -o cnv_checkbox:1 -o cnv_ref:1 -o cnv_segmentation_mode:cbs -o cnv-filter-qual:50.0 -o cnv-baseline-id:25791243964,25791291016,25791291033,25791291050,25791406163,25791440084,25791528878,25791528895,25791582119,25791582931,25791595964,25791595981,25791598767,25791637964,25791670919,25791679146,25791679164,25791681916,25791681933 -o cnv_gcbias_checkbox:1 -o hla:1 -o commandline-disclaimer:true -o arbitrary:\"--read-trimmers:adapter --trim-adapter-read1\" -o additional-file:25600057590 -o automation-sex:unkown"

    elif capturingkit=="Indiegene_Target_2109PD006-V1_4BaseCare_1K_DNA_GRCh37_sorted.bed":
        bscmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.9.5 -o project-id:" + pid + "  -o app-session-name:"+ appsess +" -l "+ appsess +" -o vc-type:1 -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:" + str(bed_id) + "-o input_list.sample-id:biosamples/526193668 -o picard_checkbox:1 -o af-filtering:1  -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o sq-filtering:1 -o tmb:1 -o vc-hotspot:26309592242 -o baseline-noise-bed:26693875133 -o vcf-site-filter:1 -o cnv_checkbox:1 -o cnv_ref:1 -o cnv_segmentation_mode:cbs -o cnv-filter-qual:50.0 -o cnv-baseline-id:26595964844,26596768352,26596768352,26597000441,26596302077,26596768331,26596296009,26596677367,26596984439,26596440110,26596089873,26596890400,26596199853,26595963870,26597226773,26596302095,26597235779,26596296030,26595984910,26595972945,26596669273,26596477171,26596089892,26595984889,26596677388,26596477187,26596861347,26596268048,26596565254,26596669289,26596247018,26595984929,26596477204,26596302112,26596199870,26596302128,26596477221,26595972961,26596302145,26595984953,26595991950,26595972980,26596199887,26596049977,26596565272,26596669311,26609829389,26596565288,26596302164 -o cnv_gcbias_checkbox:1 -o hla:1 -o commandline-disclaimer:true -o arbitrary:\"--read-trimmers:adapter --trim-adapter-read1\" -o additional-file:25600057590 -o automation-sex:unkown"



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

