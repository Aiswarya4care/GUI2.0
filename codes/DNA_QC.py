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
import sys

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

    os.system('mkdir '+ location + '/QC')

    ###### segregating files into lists #########3
    samples=glob.glob("*_fastqc.html")
    se8=list(filter(lambda x:'-SE8-' in x, samples))
    ce=list(filter(lambda x:'-CE-' in x, samples))

    #choosing between germline and somatic
    if sample_type=='DNA [Blood]':
        script_path= GUIpath + '/dna_qc_scripts/germline/'
        
    else:
        script_path= GUIpath + '/dna_qc_scripts/somatic/'
            
    #performing QC based on CE or SE8
    if len(se8)>0:
        os.system('mkdir '+ location + '/QC/SE8')
        for script in glob.glob(script_path+'*SE8.py'):
            shutil.copy(script,location + '/QC/SE8')
        for s in se8:
            print(s)
            shutil.copy(s,location + '/QC/SE8')
        
        os.chdir(location+'/QC/SE8')
    
        if len(glob.glob(location + '/QC/SE8'+'/*metrics*.csv'))>0:
            answer = tk.messagebox.askyesno("Confirmation", 'Running QC for SE8 samples')
            if answer:
                os.system('python3 '+ 'html-csv_germline_SE8.py' )
                os.system('python3 '+ 'scoring_metrics_germline_SE8.py' )
        else:
            tk.messagebox.showwarning(title='Warning', message='Please add metrics files to the folder')
            
        
    if len(ce)>0:
        os.system('mkdir '+ location + '/QC/CE')
        for script in glob.glob(script_path+'*CE.py'):
            shutil.copy(script,location + '/QC/CE')
        for c in ce:
            print(c)
            shutil.copy(c,location + '/QC/CE')
        
        os.chdir(location+'/QC/CE')

        if len(glob.glob(location + '/QC/CE'+'/*metrics*.csv'))>0:
            answer = tk.messagebox.askyesno("Confirmation", 'Running QC for CE samples')
            if answer:
                os.system('python3 '+ 'html-csv_germline_CE.py' )
                os.system('python3 '+ 'scoring_metrics_germline_CE.py' )
        else:
            tk.messagebox.showwarning(title='Warning', message='Please add metrics files to the folder')
            
        

        

