import os
import numpy as np
import pandas as pd
import tkinter as tk

import globalv

location= globalv.location
libkit=globalv.libkit
proj=globalv.proj
  
def msi():
    file_list=os.listdir(location)
    if 'MSI' in file_list:
        os.system("rm -r " + location + "/MSI")   
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
        
    mkdir="mkdir "+ location+ "/MSI"
    os.system(mkdir)
    msitxt= location +  "/MSI/msi.sh"
    f1= open(msitxt,"x")
    f1.close()
    f1= open(msitxt,"w+")
    f1.write("cd "+ location + "/MSI" + '\n')
    
    for s in samples:
        f1.write('\n' + "/home/ubuntu/Programs/msisensor2/msisensor2 msi -b 30 -d /home/ubuntu/Programs/MSI_Mirco_List/micro.list -t ")
        f1.write("/home/ubuntu/basespace/Projects/" + str(proj_dest) + "/AppResults/" + s)
        f1.write("/Files/"+s+ ".bam ")
        f1.write("-o " + location + "/MSI/" + s + "_msi" + '\n')
    
    f1.write('\n'+"echo \"######################\"")
    f1.write('\n'+"echo \"######### DONE #########\"")
    f1.write('\n'+"echo \"######################\"")
    f1.close()  

    answer = tk.messagebox.askyesnocancel("Confirmation", "Run MSI analysis?")    
   
    if answer:
        print("################################")
        print("############ Running MSI analysis ###########")
        print("################################")
        msi_path= location + "/MSI/" + "msi.sh"
        os.system("bash " + msi_path + "> "+ location + "/MSI/msilog.txt")
        print("################################")
        print("############ MSI completed ###########")
        print("################################")
    else:
        rm_cmd=" rm "+ location + "/MSI/" + "msi.sh"