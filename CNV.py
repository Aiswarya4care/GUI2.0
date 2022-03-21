import os
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import globalv

location= globalv.location
libkit=globalv.libkit
proj=globalv.proj


def cnv():
    file_list=os.listdir(location)
    if 'CNV' in file_list:
        os.system("rm -r " + location + "/CNV")
    
    #kit chosen and retrieving adapters 
    if libkit=="Roche":
        cnv_loc= "/home/ubuntu/Patient_samples/bed_files/roche/KAPA HyperExome Design files hg19/KAPA HyperExome_hg19_capture_targets.bed"
    elif libkit=="Illumina":
        cnv_loc="/home/ubuntu/Patient_samples/bed_files/Illumina_CEX_bed/TruSeq_Exome_TargetedRegions_v1.2.bed"
    else:
        cnv_loc="/home/ubuntu/Patient_samples/bed_files/v7/SureSelectV7_covered.bed"
    
    mkdir="mkdir "+ location+ "/CNV"
    os.system(mkdir) 
    #project selection and project id retrieval
    if proj=="Somatic DNA":
        proj_dest="Somatic_Patient_Samples_3"
    elif proj=="Somatic RNA":
        proj_dest="Somatic_Patient_RNA"
    else:
        proj_dest="Germline_Patient_Sample"
    
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
        
    if proj=="Somatic DNA":
        for s in samples:
            os.system("mkdir "+ location+ "/CNV/" + s)
            cnvtxt= location +  "/CNV/" + s + "/" + s+"_cnv.txt"
            f1= open(cnvtxt,"x")
            f1.close()
            f1= open(cnvtxt,"w+")
            f1.write("[general]")
            f1.write('\n'+ "chrLenFile = /home/ubuntu/Programs/files_for_control_freec/fai_file/my_genome.fa.fai")
            f1.write('\n'+ "chrFiles = /home/ubuntu/Programs/files_for_control_freec/chromFa/")
            f1.write('\n' + "window = 0" + '\n' +"ploidy = 2" + '\n' + "intercept=1")
            f1.write('\n' + "minMappabilityPerWindow = 0.7" + '\n' + "outputDir = " + location+ "/CNV/" + s)
            f1.write('\n' + "sex=XY" + '\n' + "breakPointType=2" + '\n' + "degree=3")
            f1.write('\n' + "coefficientOfVariation = 0.05" + '\n'+ "breakPointThreshold = 0.6")
            f1.write('\n' + "maxThreads = 30" + '\n' + "sambamba = /usr/bin/sambamba")
            f1.write('\n' + "SambambaThreads = 30" + '\n' + "noisyData = TRUE" + '\n'+ "printNA=FALSE")
            f1.write('\n' + '\n'+ "[sample]" +'\n')
            f1.write('\n' + "mateFile = " + "/home/ubuntu/basespace/Projects/" + str(proj_dest))
            f1.write("/AppResults/"+ s + "/Files/" + s + ".bam")
            f1.write('\n' + "inputFormat = BAM")
            f1.write('\n' + "mateOrientation = FR")
            f1.write('\n' + '\n' + "[control]" + '\n') 
            f1.write('\n' + "mateFile = /home/ubuntu/basespace/Projects/Germline_Patient_Sample/AppResults/IN-423-TJWA-B-TRIMMED/Files/IN-423-TJWA-B-TRIMMED.bam")
            f1.write('\n' + "inputFormat = BAM")
            f1.write('\n' + "mateOrientation = FR" + '\n')
            f1.write('\n' + "[BAF]" + '\n')
            f1.write('\n' + "minimalCoveragePerPosition = 5" +'\n')
            f1.write('\n' + "[target]"+ '\n')
            f1.write('\n' + "captureRegions =")
            f1.write(str(cnv_loc)) 
        f1.close()  
        
    elif proj=="Germline":
        for s in samples:
            os.system("mkdir "+ location+ "/CNV/" + s)
            cnvtxt= location +  "/CNV/" + s + "/" + s+"_cnv.txt"
            f1= open(cnvtxt,"x")
            f1.close()
            f1= open(cnvtxt,"w+")
            f1.write("[general]")
            f1.write('\n'+ "chrLenFile = /home/ubuntu/Programs/files_for_control_freec/fai_file/my_genome.fa.fai")
            f1.write('\n'+ "chrFiles = /home/ubuntu/Programs/files_for_control_freec/chromFa/")
            f1.write('\n' + "window = 0" + '\n' +"ploidy = 2" + '\n' + "intercept=1")
            f1.write('\n' + "minMappabilityPerWindow = 0.7" + '\n' + "outputDir = " + location+ "/CNV/" + s)
            f1.write('\n' + "sex=XY" + '\n' + "breakPointType=2" + '\n' + "degree=3")
            f1.write('\n' + "coefficientOfVariation = 0.05" + '\n'+ "breakPointThreshold = 0.6")
            f1.write('\n' + "maxThreads = 30" + '\n' + "sambamba = /usr/bin/sambamba")
            f1.write('\n' + "SambambaThreads = 30" + '\n' + "noisyData = TRUE" + '\n'+ "printNA=FALSE")
            f1.write('\n' + '\n'+ "[sample]" +'\n')
            f1.write('\n' + "mateFile = " + "/home/ubuntu/basespace/Projects/" + str(proj_dest))
            f1.write("/AppResults/"+ s + "/Files/" + s + ".bam")
            f1.write('\n' + "inputFormat = BAM")
            f1.write('\n' + "mateOrientation = FR")
            f1.write('\n' + "[target]"+ '\n')
            f1.write('\n' + "captureRegions =")
            f1.write(str(cnv_loc)) 
        f1.close()
    
        
    cnvrun= location +  "/CNV/run_cnv.sh"
    f2= open(cnvrun,"x")
    f2.close()
    f2= open(cnvrun,"w+")
    f2.write("cd " + location + "/CNV"+ '\n')
    for s in samples:
        f2.write('\n' + "/home/ubuntu/Programs/FREEC-11.6/src/freec -conf ")
        f2.write(s + "/" + s+"_cnv.txt" + '\n')
        f2.write('\n')
        f2.write("/home/ubuntu/Programs/./bedtools.static.binary intersect -a " +s +"/" + s + ".bam_CNVs")
        f2.write(" -b /home/ubuntu/Patient_samples/bed_files/CNV/CNV_36_genes.bed -loj | sort -V | awk -F\"\t\" \'{print $1\"\t\"$2\"\t\"$3\"\t\"$4\"\t\"$5\"\t\"$9}\' | awk -vOFS=\"\t\" \'$1=$1; BEGIN { str=\"Chromosome Start End Predicted_copy_number Type_of_alteration Gene\"; split(str,arr,\" \"); for(i in arr) printf(\"%s\t\", arr[i]);print}\' | awk '$6 != \".\"\' > ")
        f2.write(s + "\"_cnv_output.txt\"" + '\n')
        f2.write('\n'+ "##############################")
    f2.write('\n'+"echo \"######################\"")
    f2.write('\n'+"echo \"######### DONE #########\"")
    f2.write('\n'+"echo \"######################\"")
    f2.close() 
    
    answer = tk.messagebox.askyesnocancel("Confirmation", "Run CNV analysis?")
    
    if answer:
        print("################################")
        print("############ Running CNV analysis ###########")
        print("################################")
        cnv_path= location + "/CNV/run_cnv.sh >" + location + "/CNV/cnvlog.txt" 
        os.system("bash " + cnv_path)
        print("################################")
        print("############ CNV analysis completed ###########")
        print("################################")
        
    else:
        rm_cmd=" rm "+ location + "/CNV/run_cnv.sh"
