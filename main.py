import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from cutadapt_fqc import cafa
from cutadapt_fqc_drag import cafadra
from annotation import anno
from panelcreation import panel
from filter_somatic import filtereng_som
from filter_germline import filtereng_germ


window=tk.Tk()

global GUIpath
GUIpath=os.getcwd()

# declaring string variables for tkinter
library_kit=tk.StringVar()
location_name=tk.StringVar()
project= tk.StringVar()
folderPath=tk.StringVar()
appsession=tk.StringVar()
projectdirPath=tk.StringVar()

#setting the windows size
window.geometry("650x800")
window.title("Patient Data Processing")  

#Browsing the folder with samples or to perform analysis
def browse():
    global folderPath
    global project
    global library_kit
    global appsession
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
    libkit=library_kit.get()
    proj= project.get()
    location = folderPath.get()
    appsess= appsession.get()
    projectdir=projectdirPath.get()
    file1 = open(GUIpath + '/globalv.py',"w+")
    l1= 'location=' + "'" + location + "'"
    l2= 'libkit=' + "'" + libkit + "'"
    l3= 'proj=' + "'" + proj + "'"
    l4='appsess=' + "'" + appsess + "'"
    l5='projectdir=' + "'" + projectdir + "'"
    file1.writelines([l1,'\n',l2,'\n',l3,'\n',l4,'\n',l5])
    file1.close()
    file1 = open(GUIpath + '/globalv.py',"r")
    data=file1.read()
    Output.config(state=NORMAL)
    Output.insert(1.0, data)
   
#Refresh basespace
def bsrefresh():
    os.system("basemount basespace/")
    os.system("basemount basespace/")

#Run Cutadapt and FastQC
def cutad_fqc():
    cafa()
    
#Run Cutadapt, FastQC and Launch Dragen
def cutad_fqc_dra():
    cafadra()

#Annotation 
def annotate():
    anno()

#Panel creation
def panelcreation():
    panel()

#Filter-Engine Somatic
def filtersomatic():
    filtereng_som()

#Filter-Engine Germline
def filtergermline():
    filtereng_germ()

#Quit
def quit():
    file1 = open(GUIpath + '/globalv.py',"w+")
    file1.write('location=' + "'" + "'")
    file1.write('\n' + 'libkit=' + "'"  + "'")
    file1.write('\n' +'proj=' + "'" + "'")
    file1.write('\n' +'appsess=' + "'"  + "'")
    file1.write('\n' +'projectdir=' + "'"  + "'")
    file1.close()
    window.destroy()



################################################
############# Button ###########################
################################################


#browse button
browselabel= tk.Label(window, text='Choose folder path')
browse_btn=tk.Button(window,text = 'Browse', command = browse, height = 1, width = 18)
browselabel.config(font=('Nunito Sans',12))


#dropdown for library kits    
kitlabel= tk.Label(window, text= 'Select the bed file')
kitchoosen = ttk.Combobox(window, width = 26, textvariable = library_kit)
kitchoosen['values'] = ('Roche', 'Illumina','Agilent')
kitlabel.config(font=('Nunito Sans',12))

#selecting projects and retrieving project IDs
projectlabel= tk.Label(window, text= 'Select the project')
projectchoosen = ttk.Combobox(window, width = 26, textvariable = project)
projectchoosen['values'] = ('Somatic DNA', 'Somatic RNA','Germline')
projectlabel.config(font=('Nunito Sans',12))

#Appsession details
appsessionlabel= tk.Label(window, text='Enter Appsession details')
appsession= tk.Entry(window, width = 27, textvariable=appsession)
appsessionlabel.config(font=('Nunito Sans',12))

#submit button
globalv_btn=tk.Button(window,text = 'Submit', command = globalva_update, height = 1, width = 18)

#basespace refresh button
bsrefresh_btn=tk.Button(window,text = 'Refresh Basespace', command = bsrefresh, height = 1, width = 18)

#Display Information
Output = Text(window, height = 7, width = 60, bg = "light cyan")

#Cutadapt & FastQ button
cutad_fqclabel= tk.Label(window, text='Cutadapt & FastQC')
cutad_fqc_btn=tk.Button(window,text = 'Cutadapt & FastQ', command = cutad_fqc, height = 1, width = 18)
cutad_fqclabel.config(font=('Nunito Sans',13))

#Cutadapt, Fastqc and dragen button
cutad_fqc_dra_btn=tk.Button(window,text = 'Run CA, FQ and Dragen', command = cutad_fqc_dra, height = 1, width = 18)

#projectdir browse button
projlabel= tk.Label(window, text='Choose Project Folder')
projbrowse_btn=tk.Button(window,text = 'Select Project Folder', command = projectdir_browse, height = 1, width = 18)
projlabel.config(font=('Nunito Sans',12))

#Annotation
annotate_btn=tk.Button(window, text = 'Annotation', command = annotate,height = 1, width = 18) 

#Panel creation
panel_btn=tk.Button(window, text = 'Panel Creation', command = panelcreation ,height = 1, width = 18) 

#Filter Engine Somatic
filtersom_btn=tk.Button(window, text = 'Filter Engine Somatic', command = filtersomatic,height = 1, width = 18) 

#Filter Engine Somatic
filtergerm_btn=tk.Button(window, text = 'Filter Engine Germline', command = filtergermline,height = 1, width = 18) 

#Quit button
close_btn=tk.Button(window, text="Quit", command=quit, height = 1, width = 18)


################# Positioning ##########################
browselabel.grid(row=0,column=0,pady=8)
browse_btn.grid(row=0, column=1,pady=8)
kitlabel.grid(row=1, column=0,pady=8)
kitchoosen.grid( row = 1,column = 1,pady=8)
projectlabel.grid(row=2,column=0,pady=8)
projectchoosen.grid(row=2, column=1,pady=8)
appsessionlabel.grid(row=3,column=0,pady=8)
appsession.grid(row=3,column=1,pady=8)
projlabel.grid(row=4,column=0,pady=8)
projbrowse_btn.grid(row=4, column=1,pady=8)
cutad_fqc_btn.grid(row=8, column=0,pady=8)
cutad_fqc_dra_btn.grid(row=8,column=1,pady=8)

globalv_btn.grid(row=5,column=0,pady=8)
bsrefresh_btn.grid(row=5,column=1,pady=8)

Output.grid(row=6,column=0,pady=8,columnspan=5)
panel_btn.grid(row=9,column=0,pady=8) 
annotate_btn.grid(row=9,column=1,pady=8) 
filtersom_btn.grid(row=10,column=0,pady=8)
filtergerm_btn.grid(row=10,column=1,pady=8)
close_btn.grid(row=12,column=0,pady=8)

window.mainloop()        
  







