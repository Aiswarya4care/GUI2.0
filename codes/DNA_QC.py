import os
import pandas as pd
import glob, os
import pandas as pd
from importlib import reload
import globalv
import shutil
import config_gui
import numpy as np
import tkinter as tk

def dna_qc():   
    reload(globalv)
    location= globalv.location
    sample_type=globalv.sample_type
    GUIpath=config_gui.GUIpath
    os.chdir(location)

    #retrieving sample names 
    file_list=os.listdir(location)
    samples= pd.unique(file_list)
    samples=np.array(samples).tolist()

    #Removing default file names from the sample name list
    default_files=config_gui.default_files
    for s in default_files:
        if s in samples:
            samples.remove(s)
            
    #creating QC folder inside the location
    if 'QC' in samples:
        os.system('rm -r '+ location + '/QC')
    else:
        os.system('mkdir '+ location + '/QC')

    ###### fetching sample names #########3
    samples=glob.glob(location+"/*.html")

    #renaming the files (removing _S1_L001_R1_001_)
    for i in samples:
        if '_S1_L001_R1_001_fastqc.html' in i:
            os.rename(i,i.split('_S1_L001_R1_001_fastqc.html')[0]+".html")

    #segregating the files to respective folder
    se8=list(filter(lambda x:'-SE8-' in x, samples))
    ce=list(filter(lambda x:'-CE-' in x, samples))

    #choosing between germline and somatic
    if sample_type=='DNA [Blood]':
        script_path= GUIpath + '/dna_qc_scripts/germline/'
        
    else:
        script_path= GUIpath + '/dna_qc_scripts/somatic/'
            
    ############# performing QC based on SE8 #######################
    if len(se8)>0:
        os.system('mkdir '+ location + '/QC/SE8')
        os.chdir(location)

        #copying script inside the QC folder
        for script in glob.glob(script_path+'*SE8.py'):
            shutil.copy(script,location + '/QC/SE8')
        for s in se8:
            shutil.copy(s,location + '/QC/SE8')
        
        os.chdir(location+'/QC/SE8')
        
        #adding location to the python script
        with open(glob.glob(location+"/QC/SE8/*.py")[0], 'r') as file :
            filedata = file.read()
            # Replace the location
            filedata = filedata.replace('{{location}}', "'" +location + "'")
        with open(glob.glob(location+"/QC/SE8/*.py")[0], 'w') as file:
            file.write(filedata)
            
        if len(glob.glob(location + '/QC/SE8'+'/*metrics*.csv'))>0:
            answer = tk.messagebox.askyesno("Confirmation", 'Running QC for SE8 samples')
            if answer:
                os.system('python3 '+ script )
        else:
            tk.messagebox.showwarning(title='Warning', message='Please add metrics files to the folder')
            answer = tk.messagebox.askyesno("Re-Confirmation", 'Continue with DNA QC?')
            if answer:
                os.system('python3 '+ script )
            
    ############# performing QC based on CE #######################        
    if len(ce)>0:
        os.system('mkdir '+ location + '/QC/CE')
        os.chdir(location)
        for script in glob.glob(script_path+'*CE.py'):
            shutil.copy(script,location + '/QC/CE')
        for c in ce:
            
            shutil.copy(c,location + '/QC/CE')
        
        os.chdir(location+'/QC/CE')
        
        #adding location to the python script
        with open(glob.glob(location+"/QC/CE/*.py")[0], 'r') as file :
            filedata = file.read()
            # Replace the location
            filedata = filedata.replace('{{location}}', "'" +location + "'")
        with open(glob.glob(location+"/QC/CE/*.py")[0], 'w') as file:
            file.write(filedata)
        
        if len(glob.glob(location + '/QC/CE'+'/*metrics*.csv'))>0:
            answer = tk.messagebox.askyesno("Confirmation", 'Running QC for CE samples')
            if answer:
                os.system('python3 '+ script )
        else:
            tk.messagebox.showwarning(title='Warning', message='Please add metrics files to the folder')
            answer = tk.messagebox.askyesno("Re-Confirmation", 'Continue with DNA QC?')
            if answer:
                os.system('python3 '+ script )
        
            

            

