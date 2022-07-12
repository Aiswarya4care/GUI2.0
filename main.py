#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *

from codes.cutadapt_fqc import cafa
from codes.cutadapt_fqc_drag import cafadra
from codes.annotation import anno
from codes.panelcreation import panel
from codes.filter_engine import filtereng
from codes.filter_engine_tmb import filtereng_tmb
from codes.CNV import cnv_analysis 
from codes.CNV_merge import cnv_merge
from codes.MSI import msi_analysis
from codes.TMB import tmb_calculation
from codes.gene_coverage import gene_cov
#from codes.RNA_fusion import rna_fusion
from codes.RNA_fusion_QC import rna_fusion_qc
from codes.DNA_QC import dna_qc
from codes.Dragen39 import dragen39
from codes.sorting import sort
from codes.cgi_analysis import cgi

window=tk.Tk()

global GUIpath
GUIpath=os.path.realpath(__file__).split('main.py')[0]

# declaring string variables for tkinter
cap_kit=tk.StringVar()
cnv_annot=tk.StringVar()
panelbed=tk.StringVar()
location_name=tk.StringVar()
sampletype= tk.StringVar()
testtype= tk.StringVar()
folderPath=tk.StringVar()
appsession=tk.StringVar()
projectdirPath=tk.StringVar()

#setting the windows size
window.geometry("1200x850")
window.title("Patient Data Processing")  

#Browsing the folder with samples or to perform analysis
def browse():
    global folderPath
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)

#Selecting project directory (somatic or germline folders)
def projectdir_browse(): 
    #choosing a project dir
    projectdir_selected = filedialog.askdirectory()
    projectdirPath.set(projectdir_selected)

#saving all the global and cross file variables in globalv.py file
def globalva_update():
    Output.delete('1.0',END)
    capturingkit=cap_kit.get()
    stype= sampletype.get()
    ttype=testtype.get()
    location = folderPath.get()
    appsess= appsession.get()
    projectdir=projectdirPath.get()
    file1 = open(GUIpath + '/globalv.py',"w+")
    l1= 'test=' + "'" + ttype + "'"
    l2= 'location=' + "'" + location + "'"
    l3= 'capturingkit=' + "'" + capturingkit + "'"
    l4= 'sample_type=' + "'" + stype + "'"
    l5='appsess=' + "'" + appsess + "'"
    l6='projectdir=' + "'" + projectdir + "'"
    file1.writelines([l1,'\n',l2,'\n',l3,'\n',l4,'\n',l5,'\n',l6])
    file1.close()
    file1 = open(GUIpath + '/globalv.py',"r")
    data=file1.read()
    Output.config(state=NORMAL)
    Output.insert(1.0, data)
   
#Refresh basespace
def bsrefresh():
    os.system("basemount basespace/")
    os.system("basemount basespace/")


#Quit
def quit():
    file1 = open(GUIpath + '/globalv.py',"w+")
    file1.write('test=' + "'"+ "'")
    file1.write('\n'+'location=' + "'" + "'")
    file1.write('\n' + 'capturingkit=' + "'"  + "'")
    file1.write('\n' +'sample_type=' + "'" + "'")
    file1.write('\n' +'appsess=' + "'"  + "'")
    file1.write('\n' +'projectdir=' + "'"  + "'")
    file1.close()
    window.destroy()



################################################
############# Button function ##################
################################################

font_options = {'font': ('Nunito Sans',11)}

#browse button
browse_btn=tk.Button(window,text = 'Select Source directory', command = browse, height = 1, width = 18)

#projectdir browse button
projbrowse_btn=tk.Button(window,text = 'Select Project Directory', command = projectdir_browse, height = 1, width = 18)

#labels for the section
dnalabel=tk.Label(window, text= 'DNA Data Analysis',**font_options)
rnalabel=tk.Label(window, text= 'RNA Data Analysis',**font_options)

#dropdown for capturing_kit
capturingkit= os.listdir(GUIpath+'/bed_files/capturing_kits')
capturingkitlabel= tk.Label(window, text= 'Select capturing kit',**font_options)
capturingkitchosen = ttk.Combobox(window, width = 28, textvariable = cap_kit)
capturingkitchosen['values'] = (capturingkit)

#selecting test name
testlabel=tk.Label(window, text= 'Select the Test name',**font_options)
testchosen=ttk.Combobox(window, width = 28, textvariable = testtype)
testchosen['values'] = ( 'TarGT_Absolute','TarGT_Core', 'TarGT_Indigene', 'TarGT_Focus', 'TarGT_First', 'TarGT_Absolute_Germline',  'Germline_Plus', 'Germline_++','HRR')

#selecting projects and retrieving project IDs
sampletypelabel= tk.Label(window, text= 'Select the sample type',**font_options)
sampletypechosen = ttk.Combobox(window, width = 28, textvariable = sampletype)
sampletypechosen['values'] = ('DNA [FFPE, FF]', 'DNA [Blood]','DNA [cf]','RNA')

#Appsession details
appsessionlabel= tk.Label(window, text='Enter Appsession details',**font_options)
appsession= tk.Entry(window, width = 29, textvariable=appsession)

#submit button
globalv_btn=tk.Button(window,text = 'Submit', command = globalva_update, height = 1, width = 18)

#basespace refresh button
bsrefresh_btn=tk.Button(window,text = 'Refresh Basespace', command = bsrefresh, height = 1, width = 18)

#Display Information
Output = Text(window, height = 12, width = 60, bg = "light cyan")

#SOrting files based on sample extension
sort_btn=tk.Button(window,text = 'Sort files', command = sort, height = 1, width = 18)

#Cutadapt & FastQ button
#cutad_fqclabel= tk.Label(window, text='Cutadapt & FastQC',**font_options)
cutad_fqc_btn=tk.Button(window,text = 'Cutadapt & FastQ', command = cafa, height = 1, width = 18)

#Cutadapt, Fastqc and dragen button
cutad_fqc_dra_btn=tk.Button(window,text = 'Run CA, FQ and Dragen', command = cafadra, height = 1, width = 18)

#Dragen alone
dna_drag36_btn= tk.Button(window,text = 'Dragen 3.6', command = cafadra, height = 1, width = 18)
dna_drag39_btn= tk.Button(window,text = 'Dragen 3.9', command = dragen39, height = 1, width = 18)
rna_drag_btn= tk.Button(window,text = 'Gene fusion Var call', command = cafadra, height = 1, width = 18)

#CGI analysis
cgi_btn=tk.Button(window, text = 'Run CGI', command = cgi ,height = 1, width = 18) 

#Annotation
annotate_btn=tk.Button(window, text = 'Annotation', command = anno,height = 1, width = 18) 

#ANnotation, filter, TMB
annofiltertmb_btn=tk.Button(window, text = 'Annot + Filter + TMB', command = anno,height = 1, width = 18)

#Panel creation
panel_btn=tk.Button(window, text = 'Panel Creation', command = panel ,height = 1, width = 18) 

#Filter Engine Somatic
filtereng_btn=tk.Button(window, text = 'Filter Engine', command = filtereng,height = 1, width = 18) 

#Filter Engine Somatic
filterengtmb_btn=tk.Button(window, text = 'Filter Engine + TMB', command = filtereng_tmb,height = 1, width = 18) 

#CNV Analysis
cnv_btn=tk.Button(window, text = 'Run CNV', command = cnv_analysis, height = 1, width = 18) 

#CNV and Merge
cnvmerge_btn=tk.Button(window, text = 'CNV Merge', command = cnv_merge ,height = 1, width = 18) 

#MSI analysis
msi_btn=tk.Button(window, text = 'Run MSI', command = msi_analysis ,height = 1, width = 18) 

#CNV & MSI together
cnvmsi_btn=tk.Button(window, text = 'CNV + MSI', command = msi_analysis ,height = 1, width = 18) 

#TMB analysis
tmb_btn=tk.Button(window, text = 'Run TMB', command = tmb_calculation ,height = 1, width = 18) 

#Gene coverage
genecov_btn= tk.Button(window, text = 'Gene Coverage', command = gene_cov ,height = 1, width = 18) 

#RNA fusion
#rnafus_btn=tk.Button(window, text = 'RNA Fusion', command = rna_fusion ,height = 1, width = 18) 

#RNA QC
rnaqc_btn= tk.Button(window, text = 'RNA Fusion & QC', command = rna_fusion_qc ,height = 1, width = 18) 

#DNA QC
dnaqc_btn= tk.Button(window, text = 'DNA QC', command = dna_qc ,height = 1, width = 18
)

#Zip files for email
zip_btn=tk.Button(window, text = 'Zip files for Mail', command = panel ,height = 1, width = 18)

#Complete DNA data analysis
completedna_btn=tk.Button(window, text = 'DNA Data Analysis', command = dna_qc ,height = 1, width = 18
)
#Complete RNA data analysis
completerna_btn=tk.Button(window, text = 'RNA Data Analysis', command = dna_qc ,height = 1, width = 18
)
#Quit button
close_btn=tk.Button(window, text="Quit", command=quit, height = 1, width = 18)


################# Button Positioning ##########################

sampletypelabel.grid(row=0,column=0,pady=6)
sampletypechosen.grid(row=0, column=1,pady=6)
testlabel.grid(row=1, column=0,pady=6)
testchosen.grid( row = 1,column = 1,pady=6)
capturingkitlabel.grid(row=2, column=0,pady=6)
capturingkitchosen.grid( row = 2,column = 1,pady=6)

appsessionlabel.grid(row=3,column=0,pady=8)
appsession.grid(row=3,column=1,pady=8)

browse_btn.grid(row=4, column=0,pady=6, padx=30)
projbrowse_btn.grid(row=4, column=1,pady=6,padx=30)

##### DNA Data analysis ####
dnalabel.grid(row=0,column=3,pady=15)
sort_btn.grid(row=1, column=3,pady=8, padx=50)
dna_drag36_btn.grid(row=2,column=3,pady=6)
dna_drag39_btn.grid(row=3,column=3,pady=6)
dnaqc_btn.grid(row=4,column=3,pady=6)
panel_btn.grid(row=5,column=3,pady=8) 
cgi_btn.grid(row=6,column=3,pady=6)
annotate_btn.grid(row=7,column=3,pady=6)
filtereng_btn.grid(row=8,column=3,pady=8)
filterengtmb_btn.grid(row=9,column=3,pady=8)
cnv_btn.grid(row=10
,column=3,pady=6)
cnvmerge_btn.grid(row=11,column=3,pady=8)
msi_btn.grid(row=12,column=3,pady=6)
cnvmsi_btn.grid(row=13,column=3,pady=8)
tmb_btn.grid(row=14,column=3,pady=6)
zip_btn.grid(row=15,column=3,pady=8)

##### RNA Analysis ####
rnalabel.grid(row=0,column=4,pady=15)
rna_drag_btn.grid(row=1,column=4,pady=6)
rnaqc_btn.grid(row=2,column=4,pady=6)
genecov_btn.grid(row=3,column=4,pady=8)
#rnafus_btn.grid(row=4,column=4,pady=8)
zip_btn.grid(row=5,column=4,pady=6)

#mandatory buttons
Output.grid(row=5,column=0,columnspan=2, rowspan=5)
globalv_btn.grid(row=10,column=0,pady=6)
bsrefresh_btn.grid(row=10,column=1,pady=6)
completedna_btn.grid(row=11,column=0,pady=6)
completerna_btn.grid(row=12,column=0,pady=6)
close_btn.grid(row=13,column=0,pady=6)

window.mainloop()        
  







