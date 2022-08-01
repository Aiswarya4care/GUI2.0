import os
import numpy as np
import pandas as pd
import tkinter as tk
import config_gui
from importlib import reload
import config_gui
import glob

import globalv

def cnv_analysis():
    reload(globalv)
    location= globalv.location
    projectdir=globalv.projectdir
    sample_type=globalv.sample_type
    chrLenFile= config_gui.chrLenFile
    chrFiles=config_gui.chrFiles
    sambamba=config_gui.sambamba
    controlfreec=config_gui.controlfreec
    bedtools= config_gui.bedtools
    projectdir=globalv.projectdir
    capturingkit=globalv.capturingkit
    GUIpath=config_gui.GUIpath

    file_list=glob.glob(location+"/*_R1*")
    if 'CNV' in file_list:
        os.system("rm -r " + location + "/CNV")
    mkdir="mkdir "+ location+ "/CNV"
    os.system(mkdir)

    #collecting sample names
    samples=[]
    for file in file_list:
        sample=file.split("/")[-1]
        if '_S1_L001_R1_001_' in file_list[0]:
            sample= sample.split("_S1_L001_R1_")
        else:
            sample= sample.split("_R1_")
        samples.append(sample[0])
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()

    ###### writing the array to list.txt #########
    file = open(location+"/CNV/list.txt", "w+")
    # Saving the array in a text file
    for s in samples:
        file.writelines([s,'\n'])
    file.close()

    ################# selecting modified capturing bed files #################
    if capturingkit=='SureSelectXT_V8_Covered.bed':
        modified_capt_bed= 'SureSelectXT_V8_Covered.bed'
    elif capturingkit=='Indiegene_Target_2109PD006-V1_4BaseCare_1K_DNA_GRCh37.bed':
        modified_capt_bed= 'Indiegene_Target_2109PD006-V1_4BaseCare_1K_DNA_GRCh37_modified.bed'
    else:
        modified_capt_bed='###########################'

    ########################################   

    #Coping the shell script and modifying the content based on the somatic or germline
    if sample_type=='DNA [Blood]':
            script_name= 'cnv_annotation_germline_SE8.sh'
            configfile_name= 'cnv_config_germline.pl'
    else:
        script_name= 'cnv_annotation_somatic.sh'
        configfile_name='cnv_config_somatic.pl'

    loc_cnv_sh_file= GUIpath + '/cnv/' + script_name
    loc_cnv_config_file= GUIpath + '/cnv/' + configfile_name

    os.system('cp '+ loc_cnv_sh_file + ' ' + location+ "/CNV/") 
    os.system('cp '+ loc_cnv_config_file + ' ' + location+ "/CNV/") 

    #giving the necessary permissions
    os.chdir(location + '/CNV')
    os.system('chmod 777 *')

    #modifying the annotation_mod.sh file
    cnvannofile=location+'/CNV/'+ script_name
    # Read in the file
    with open(cnvannofile, 'r') as file :
        filedata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
        filedata = filedata.replace('{{location}}', location+'/CNV/')
        filedata = filedata.replace('{{projectdir}}', projectdir)
        filedata = filedata.replace('{{GUIpath}}', GUIpath)
        filedata = filedata.replace('{{modified_capt_bed}}', modified_capt_bed)
        filedata = filedata.replace('{{controlfreec}}', controlfreec)
        filedata = filedata.replace('{{bedtools}}', bedtools)

    # Write the file out again
    with open(cnvannofile, 'w') as file:
        file.write(filedata)
    #modifying the cnv perl file
    cnvperlfile=location+'/CNV/'+ configfile_name
    # Read in the file
    with open(cnvperlfile, 'r') as file :
        filedata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
        filedata = filedata.replace('{{chrLenFile}}', chrLenFile)
        filedata = filedata.replace('{{chrFiles}}', chrFiles)
        filedata = filedata.replace('{{sambamba}}', sambamba)
        
    # Write the file out again
    with open(cnvperlfile, 'w') as file:
        file.write(filedata)
        
    answer = tk.messagebox.askyesno("Confirmation", "Run CNV analysis?")

    if answer:
        print("################################")
        print("############ Running CNV analysis ###########")
        print("################################")
        cnvrun= location +  "/CNV/" + script_name
        os.system("sh "+ cnvrun)
        print("################################")
        print("############ CNV analysis completed ###########")
        print("################################")
        
    else:
        print('##### CNV Analysis Aborted #####')
