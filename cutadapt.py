import os
import globalv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

location= globalv.location
libkit=globalv.libkit
proj=globalv.proj

def cafa():
    
 #retrieving sample name
    file_list=os.listdir(location)
    if 'temp1.sh' in file_list:
        os.system("rm " + location + "/temp1.sh")
    if 'cutadaptlog' in file_list:
        os.system("rm " + location + "/cutadaptlog")
#kit chosen and retrieving adapters 
    
    if libkit=="Roche":
        adapter="AGATCGGAAGAGC"
    elif libkit=="Illumina":
        adapter="CTGTCTCTTATACACATCT"
    else:
        adapter="AGATCGGAAGAGC"

#project selection and project id retrieval
    
    if proj=="Somatic DNA":
        vctype="1"
        pid="175429254"
    elif proj=="Somatic RNA":
        pid="148206064"
    else:
        pid="166558401"
        vctype="0"

    l1="for i in *_R1.fastq.gz"
    l2="do"
    l3="   SAMPLE=$(echo ${i} | sed \"s/_R1\.fastq\.gz//\") "
    l4="   echo ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz"
    l5="   cutadapt -j 30 -m 35 -a "+ adapter +" -A " +adapter+" -o ${SAMPLE}_S1_L001_R1_001.fastq.gz -p ${SAMPLE}_S1_L001_R2_001.fastq.gz ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz >" + location + "/cutadaptlog" + "/${SAMPLE}_cutadaptlog.txt"
    l6="done"
    l8="bs upload dataset --project="
    l10="echo \"############ FQ and CA completed ###########\""
    
    os.system("mkdir "+ location+ "/cutadaptlog")
    temp= location + "/temp1.sh"
    f= open(temp,"x")
    f.close()
    f= open(temp,"w+")
    f.write("cd " + location)
    f.write('\n' + l1)
    f.write('\n' + l2)
    f.write('\n' + l3)
    f.write('\n' + l4)
    f.write('\n' + l5)
    f.write('\n' + l6)
    f.write('\n'+ l8 + str(pid) + " *R1_001.fastq.gz *R2_001.fastq.gz")
    f.write('\n' + l10)
    f.close()
    
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
