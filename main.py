import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from codes.cutadapt_fqc import cafa
from codes.cutadapt_fqc_drag import cafadra
from codes.annotation import anno
from codes.panelcreation import panel
from codes.filter_somatic import filtereng_som
from codes.filter_germline import filtereng_germ
from codes.CNV import cnv_analysis
from codes.CNV_merge import cnv_merge
from codes.MSI import msi_analysis
from codes.TMB import tmb_calculation
from codes.gene_coverage import gene_cov
from codes.RNA_fusion import rna_fusion

window=tk.Tk()

global GUIpath
GUIpath=os.getcwd()

# declaring string variables for tkinter
dra_bed=tk.StringVar()
cnv_ref=tk.StringVar()
cnv_annot=tk.StringVar()
panelbed=tk.StringVar()
location_name=tk.StringVar()
sampletype= tk.StringVar()
folderPath=tk.StringVar()
appsession=tk.StringVar()
projectdirPath=tk.StringVar()

#setting the windows size
window.geometry("950x850")
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
    dragen_bed=dra_bed.get()
    cnv_ref_bed=cnv_ref.get()
    cnv_annot_bed=cnv_annot.get()
    panel_bed=panelbed.get()
    stype= sampletype.get()
    location = folderPath.get()
    appsess= appsession.get()
    projectdir=projectdirPath.get()
    file1 = open(GUIpath + '/globalv.py',"w+")
    l1= 'location=' + "'" + location + "'"
    l2= 'dragen_bed=' + "'" + dragen_bed + "'"
    l3= 'sample_type=' + "'" + stype + "'"
    l4='appsess=' + "'" + appsess + "'"
    l5='projectdir=' + "'" + projectdir + "'"
    l6= 'cnv_ref_bed=' + "'"  + cnv_ref_bed + "'"
    l7= 'cnv_annot_bed=' + "'" + cnv_annot_bed + "'"
    l8= 'panel_bed='+"'"+ panel_bed + "'"
    file1.writelines([l1,'\n',l2,'\n',l3,'\n',l4,'\n',l5,'\n',l6,'\n',l7,'\n'+l8])
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
    file1.write('location=' + "'" + "'")
    file1.write('\n' + 'dragen_bed_file=' + "'"  + "'")
    file1.write('\n' +'sample_type=' + "'" + "'")
    file1.write('\n' +'appsess=' + "'"  + "'")
    file1.write('\n' +'projectdir=' + "'"  + "'")
    file1.write('\n' +'cnv_ref_bed=' + "'"  + "'")
    file1.write('\n' +'cnv_annot_bed=' + "'"  + "'")
    file1.write('\n' +'panel_bed=' + "'"  + "'")
    file1.close()
    window.destroy()



################################################
############# Button function ##################
################################################

font_options = {'font': ('Nunito Sans',11)}

#browse button
browselabel= tk.Label(window, text='Choose folder path',**font_options)
browse_btn=tk.Button(window,text = 'Browse', command = browse, height = 1, width = 18)

#dropdown for dragen bedfiles
dragbedfiles= os.listdir(GUIpath+'/bed_files/dragen_bed_files')
dragbedfiles.insert(0, 'Illumina')
dragbedlabel= tk.Label(window, text= 'Select DRAGEN bed file',**font_options)
dragbedchosen = ttk.Combobox(window, width = 26, textvariable = dra_bed)
dragbedchosen['values'] = (dragbedfiles)

#selecting projects and retrieving project IDs
sampletypelabel= tk.Label(window, text= 'Select the sample type',**font_options)
sampletypechosen = ttk.Combobox(window, width = 26, textvariable = sampletype)
sampletypechosen['values'] = ('Somatic DNA', 'Somatic RNA','Germline')

#Appsession details
appsessionlabel= tk.Label(window, text='Enter Appsession details',**font_options)
appsession= tk.Entry(window, width = 27, textvariable=appsession)

#submit button
globalv_btn=tk.Button(window,text = 'Submit', command = globalva_update, height = 1, width = 18)

#basespace refresh button
bsrefresh_btn=tk.Button(window,text = 'Refresh Basespace', command = bsrefresh, height = 1, width = 18)

#Display Information
Output = Text(window, height = 7, width = 60, bg = "light cyan")

#Cutadapt & FastQ button
cutad_fqclabel= tk.Label(window, text='Cutadapt & FastQC',**font_options)
cutad_fqc_btn=tk.Button(window,text = 'Cutadapt & FastQ', command = cafa, height = 1, width = 18)

#Cutadapt, Fastqc and dragen button
cutad_fqc_dra_btn=tk.Button(window,text = 'Run CA, FQ and Dragen', command = cafadra, height = 1, width = 18)

#projectdir browse button
projlabel= tk.Label(window, text='Choose Project Folder',**font_options)
projbrowse_btn=tk.Button(window,text = 'Select Project Folder', command = projectdir_browse, height = 1, width = 18)

#Panel bed file dropdown
panelbedfiles= os.listdir(GUIpath+'/bed_files/panel_bed_files/')
panelbedlabel= tk.Label(window, text= 'Select Panel bed file',**font_options)
panelbedchosen = ttk.Combobox(window, width = 26, textvariable = panelbed)
panelbedchosen['values'] = (panelbedfiles)

#CNV reference bed file dropdown
cnvrefbedfiles= os.listdir(GUIpath+'/bed_files/cnv_bed_files/cnv_reference_bedfiles/')
cnvrefbedlabel= tk.Label(window, text= 'Select CNV Reference bed file',**font_options)
cnvrefbedchosen = ttk.Combobox(window, width = 26, textvariable = cnv_ref)
cnvrefbedchosen['values'] = (cnvrefbedfiles)

#CNV Annotation bed file dropdown
cnvannobedfiles= os.listdir(GUIpath+'/bed_files/cnv_bed_files/cnv_annotation_bedfiles/')
cnvannobedlabel= tk.Label(window, text= 'Select CNV Annotation bed file',**font_options)
cnvannobedchosen = ttk.Combobox(window, width = 26, textvariable = cnv_annot)
cnvannobedchosen['values'] = (cnvannobedfiles)

#Annotation
annotate_btn=tk.Button(window, text = 'Annotation', command = anno,height = 1, width = 18) 

#Panel creation
panel_btn=tk.Button(window, text = 'Panel Creation', command = panel ,height = 1, width = 18) 

#Filter Engine Somatic
filtersom_btn=tk.Button(window, text = 'Filter Engine Somatic', command = filtereng_som,height = 1, width = 18) 

#Filter Engine Somatic
filtergerm_btn=tk.Button(window, text = 'Filter Engine Germline', command = filtereng_germ,height = 1, width = 18) 

#CNV Analysis
cnv_btn=tk.Button(window, text = 'Run CNV', command = cnv_analysis, height = 1, width = 18) 

#CNV and Merge
cnvmerge_btn=tk.Button(window, text = 'CNV Merge', command = cnv_merge ,height = 1, width = 18) 

#MSI analysis
msi_btn=tk.Button(window, text = 'Run MSI', command = msi_analysis ,height = 1, width = 18) 

#TMB analysis
tmb_btn=tk.Button(window, text = 'Run TMB', command = tmb_calculation ,height = 1, width = 18) 

#Gene coverage
genecov_btn= tk.Button(window, text = 'Gene Coverage', command = gene_cov ,height = 1, width = 18) 

#RNA fusion
rnafus_btn=tk.Button(window, text = 'RNA Fusion', command = rna_fusion ,height = 1, width = 18) 

#Quit button
close_btn=tk.Button(window, text="Quit", command=quit, height = 1, width = 18)


################# Button Positioning ##########################

browselabel.grid(row=0,column=0,pady=8)
browse_btn.grid(row=0, column=1,pady=8)
dragbedlabel.grid(row=1, column=0,pady=8)
dragbedchosen.grid( row = 1,column = 1,pady=8)
sampletypelabel.grid(row=2,column=0,pady=8)
sampletypechosen.grid(row=2, column=1,pady=8)
appsessionlabel.grid(row=3,column=0,pady=8)
appsession.grid(row=3,column=1,pady=8)
projlabel.grid(row=4,column=0,pady=8)
projbrowse_btn.grid(row=4, column=1,pady=8)

cnvrefbedlabel.grid(row=5, column=0,pady=8)
cnvrefbedchosen.grid( row = 5,column = 1,pady=8)
cnvannobedlabel.grid(row=6, column=0,pady=8)
cnvannobedchosen.grid( row = 6,column = 1,pady=8)
panelbedlabel.grid(row=7, column=0,pady=8)
panelbedchosen.grid( row = 7,column = 1,pady=8)


Output.grid(row=8,column=0,pady=8,columnspan=2,rowspan=4)
globalv_btn.grid(row=13,column=0,pady=8)
bsrefresh_btn.grid(row=13,column=1,pady=8)

cutad_fqc_btn.grid(row=0, column=3,pady=8, padx=50)
cutad_fqc_dra_btn.grid(row=1,column=3,pady=8)
panel_btn.grid(row=2,column=3,pady=8) 
annotate_btn.grid(row=3,column=3,pady=8) 
filtersom_btn.grid(row=4,column=3,pady=8)
filtergerm_btn.grid(row=5,column=3,pady=8)

cnv_btn.grid(row=6,column=3,pady=8)
cnvmerge_btn.grid(row=7,column=3,pady=8)
msi_btn.grid(row=8,column=3,pady=8)
tmb_btn.grid(row=9,column=3,pady=8)
genecov_btn.grid(row=10,column=3,pady=8)
rnafus_btn.grid(row=11,column=3,pady=8)


close_btn.grid(row=15,column=0,pady=8)

window.mainloop()        
  







