import os
import globalv
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

location= globalv.location
libkit=globalv.libkit
proj=globalv.proj
appsess=globalv.appsess

def cafadra():
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
#kit chosen and retrieving adapters 
    
    if libkit=="Roche":
        adapter="AGATCGGAAGAGC"
        bed_file_loc= "roche_hg19_panel.bed"
    elif libkit=="Illumina":
        adapter="CTGTCTCTTATACACATCT"
        bed_file_loc="CEX_illumina_nextera_panel.bed"
    else:
        adapter="AGATCGGAAGAGC"
        bed_file_loc="New_agilent_panel.bed"

#project selection and project id retrieval
    
    if proj=="Somatic DNA":
        vctype="1"
        pid="175429254"
        proj_des="Somatic_Patient_Samples_3"
    elif proj=="Somatic RNA":
        pid="148206064"
    else:
        pid="166558401"
        vctype="0"
        proj_des="Germline_Patient_Sample"

#command for dragen
    if libkit=="Illumina" and proj=="Somatic DNA":
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l " + appsess +" -o project-id:175429254 -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:Illumina_Exome_TargetedRegions_v1.2 -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o commandline-disclaimer:true"
    
    if libkit=="Illumina" and proj=="Germline":
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:166558401 -o vc-type:0 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:Illumina_Exome_TargetedRegions_v1.2 -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o sv_checkbox:1 -o commandline-disclaimer:true"

    if libkit=="Agilent" and proj=="Somatic DNA":
        bed_id=20024037150
        cmd= "bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:175429254 -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:"+ str(bed_id) +" -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o commandline-disclaimer:true"
    
    if libkit=="Agilent" and proj=="Germline":
        bed_id=20024037150        
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:166558401 -o vc-type:0 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:"+ str(bed_id) +" -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o sv_checkbox:1 -o commandline-disclaimer:true"

    if libkit=="Roche" and proj=="Somatic DNA":
        bed_id=20977118310
        cmd= "bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:175429254 -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:"+ str(bed_id) +" -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o commandline-disclaimer:true"

    if libkit=="Roche" and proj=="Germline":
        bed_id=20977118310        
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:166558401 -o vc-type:0 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:"+ str(bed_id) +" -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o sv_checkbox:1 -o commandline-disclaimer:true"
    
    if proj=="Somatic RNA":
        cmd="bs launch application -n \"DRAGEN RNA Pipeline\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:148206064 -o sample-id:$bsids -o ht-ref:hg19-altaware-cnv-anchor.v8 -o gene_fusion:1 -o quantification_checkbox:0 -o commandline-disclaimer:true"
    
#for dragen 
    
    
    l2="for i in *_R1.fastq.gz"
    l3="do"
    l4="   SAMPLE=$(echo ${i} | sed \"s/_R1\.fastq\.gz//\") "
    l5="   echo ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz"
    l6="   cutadapt -j 30 -m 35 -a "+ adapter +" -A " +adapter+" -o ${SAMPLE}_S1_L001_R1_001.fastq.gz -p ${SAMPLE}_S1_L001_R2_001.fastq.gz ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz >" + location + "/cutadaptlog" + "/${SAMPLE}_cutadaptlog.txt"
    l7="done"
    l8="bs upload dataset --project="
    l10="samples=(" + str(samples).strip("[]").replace("'","").replace(",","") + ")"
    l11="for i in ${samples[@]};  do"
    l12="echo $i;"
    l13="bsid=`bs get biosample -n $i –terse | grep \"Id\" | head -1 | grep -Eo '[0-9]{1,}'`;"
    l14="bsids+=($bsid)"
    l15="done"
    l16="printf -v joined '%s,' \"${bsids[@]}\""
    l17="bsids=${joined%,}"
    l18="echo $bsids"
    l1="perl /home/ubuntu/Programs/fastqc_v0.11.9/FastQC/fastqc *.gz"
    
    os.system("mkdir "+ location+ "/cutadaptlog")
    temp= location + "/temp1.sh"
    f= open(temp,"x")
    f.close()
    f= open(temp,"w+")
    f.write("cd " + location)
    f.write('\n' + l2)
    f.write('\n' + l3)
    f.write('\n' + l4)
    f.write('\n' + l5)
    f.write('\n' + l6)
    f.write('\n' + l7)
    f.write('\n'+ l8 + str(pid) + " *R1_001.fastq.gz *R2_001.fastq.gz")
    f.write('\n' + l10)
    f.write('\n' + l11)
    f.write('\n' + l12)
    f.write('\n' + l13)
    f.write('\n' + l14)
    f.write('\n' + l15)
    f.write('\n' + l16)
    f.write('\n'+l17)
    f.write('\n'+l18)
    f.write('\n'+ cmd)
    f.write('\n'+"echo \"########################\"")
    f.write('\n'+"echo \"Dragen Launched\"")
    f.write('\n'+"echo \"########################\"")
    f.write('\n' + l1)
    f.write('\n'+"echo \"########################\"")
    f.write('\n'+"echo \"FastQC completed\"")
    f.write('\n'+"echo \"########################\"")
    f.close()
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
        
cafadra()