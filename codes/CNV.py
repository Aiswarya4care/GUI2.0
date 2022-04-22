import os
import numpy as np
import pandas as pd
import tkinter as tk
import config_gui
from importlib import reload
import config_gui

import globalv

global GUIpath
GUIpath=GUIpath=os.path.realpath(__file__).split('main.py')[0]

def cnv_analysis():
    reload(globalv)
    location= globalv.location
    projectdir=globalv.projectdir
    chrLenFile= config_gui.chrLenFile
    chrFiles=config_gui.chrFiles
    sambamba=config_gui.sambamba
    controlfreec=config_gui.controlfreec
    bedtools= config_gui.bedtools
    cnv_ref_bed=globalv.cnv_ref_bed
    cnv_annot_bed=globalv.cnv_annot_bed
    projectdir=globalv.projectdir
    capturingkit=globalv.capturingkit

    file_list=os.listdir(location)
    if 'CNV' in file_list:
        os.system("rm -r " + location + "/CNV")
    mkdir="mkdir "+ location+ "/CNV"
    os.system(mkdir)
    
    #collecting sample names
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

    ########################################   
    #generating config files for each sample#
    for s in samples:
        os.system("mkdir "+ location+ "/CNV/" + s)

    #Coping the shell script and modifying the content  
    loc_cnvconfig_file= GUIpath + '/cnv/samplename_cnv_config.txt'     
    os.system('cp '+ loc_cnvconfig_file + ' ' + location+ "/CNV/" + s) 
    
    #giving the necessary permissions
    os.chdir(location)
    os.system('chmod 777 *')

    #modifying the annotation_mod.sh file
    cnvconfigfile=location+'/samplename_cnv_config.txt'
    # Read in the file
    with open(cnvconfigfile, 'r') as file :
        filedata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
        filedata = filedata.replace('{{chrLenFile}}', chrLenFile)
        filedata = filedata.replace('{{chrFiles}}', chrFiles)
        filedata = filedata.replace('{{outputDir}}', location+ "/CNV/" + s)
        filedata = filedata.replace('{{sambamba}}', sambamba)
        filedata = filedata.replace('{{mateFile}}', projectdir + "/AppResults/" + s + "/Files/"+ s + ".bam")
        filedata = filedata.replace('{{captureRegions}}', capturingkit)

    # Write the file out again
    with open(cnvconfigfile, 'w') as file:
        file.write(filedata)

    for s in samples:
        os.system("mkdir "+ location+ "/CNV/" + s)
        cnvtxt= location +  "/CNV/" + s + "/" + s+"_cnv.txt"
        f1= open(cnvtxt,"x")
        f1.close()
        f1= open(cnvtxt,"w+")
        f1.write("[general]")
        f1.write('\n'+ "chrLenFile = " + chrLenFile )
        f1.write('\n'+ "chrFiles = " + chrFiles)
        f1.write('\n' + "window = 0" + '\n' +"ploidy = 2" + '\n' + "intercept=1")
        f1.write('\n' + "minMappabilityPerWindow = 0.7" + '\n' + "outputDir = " + location+ "/CNV/" + s)
        f1.write('\n' + "sex=XY" + '\n' + "breakPointType=2" + '\n' + "degree=3")
        f1.write('\n' + "coefficientOfVariation = 0.05" + '\n'+ "breakPointThreshold = 0.6")
        f1.write('\n' + "maxThreads = 30" + '\n' + "sambamba = "+ sambamba)
        f1.write('\n' + "SambambaThreads = 30" + '\n' + "noisyData = TRUE" + '\n'+ "printNA=FALSE")
        f1.write('\n' + '\n'+ "[sample]" +'\n')
        f1.write('\n' + "mateFile = " + str(projectdir))
        f1.write("/AppResults/"+ s + "/Files/" + s + ".bam")
        f1.write('\n' + "inputFormat = BAM")
        f1.write('\n' + "mateOrientation = FR")
        f1.write('\n' + "[BAF]" + '\n')
        f1.write('\n' + "minimalCoveragePerPosition = 5" +'\n')
        f1.write('\n' + "[target]"+ '\n')
        f1.write('\n' + "captureRegions =")
        f1.write(str(GUIpath+'/bed_files/cnv_bed_files/cnv_reference_bedfiles/'+ cnv_ref_bed)) 
    f1.close()  
        
            
    cnvrun= location +  "/CNV/run_cnv.sh"
    f2= open(cnvrun,"x")
    f2.close()
    f2= open(cnvrun,"w+")
    f2.write("cd " + location + "/CNV"+ '\n')
    for s in samples:
        f2.write('\n' + controlfreec +" -conf ")
        f2.write(s + "/" + s+"_cnv.txt" + '\n')
        f2.write('\n')
        f2.write(bedtools + " -a " +s +"/" + s + ".bam_CNVs")
        f2.write(" -b " + cnv_annot_bed + " -loj | sort -V | awk -F\"\t\" \'{print $1\"\t\"$2\"\t\"$3\"\t\"$4\"\t\"$5\"\t\"$9}\' | awk -vOFS=\"\t\" \'$1=$1; BEGIN { str=\"Chromosome Start End Predicted_copy_number Type_of_alteration Gene\"; split(str,arr,\" \"); for(i in arr) printf(\"%s\t\", arr[i]);print}\' | awk '$6 != \".\"\' > ")
        f2.write(s + "\"_cnv_output.txt\"" + '\n')
        f2.write('\n'+ "##############################")
    f2.write('\n'+"echo \"######################\"")
    f2.write('\n'+"echo \"######### DONE #########\"")
    f2.write('\n'+"echo \"######################\"")
    f2.close() 
    
    answer = tk.messagebox.askyesno("Confirmation", "Run CNV analysis?")
    
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
        print('##### CNV Analysis Aborted #####')
