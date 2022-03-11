import pandas as pd
import numpy as np
import glob
import inflect
from functools import reduce
import os
import warnings
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import shutil
import test

window=tk.Tk()

# setting the windows size
window.geometry("500x500")
window.title("Patient Data Processing")  

# declaring string variab nle
library_kit=tk.StringVar()
location_name=tk.StringVar()
project= tk.StringVar()
folderPath=tk.StringVar()
appsession_name=tk.StringVar()


def browse():
    global location_name
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)
    location_name=folderPath.get()

    
def submit():
    cafa()

################################################
############# Button ###########################
################################################
        
#browse button
samplelabel= tk.Label(window, text='Choose folder location')
browse_btn=tk.Button(window,text = 'Browse', command = browse, height = 1, width = 18)
samplelabel.config(font=('Nunito Sans',13))


#dropdown for library kits    
kitlabel= tk.Label(window, text= 'Select the library kit')
kitchoosen = ttk.Combobox(window, width = 27, textvariable = library_kit)
kitchoosen['values'] = ('Roche', 'Illumina','Agilent')
kitlabel.config(font=('Nunito Sans',13))

#selecting projects and retrieving project IDs
projectlabel= tk.Label(window, text= 'Select the project')
projectchoosen = ttk.Combobox(window, width = 27, textvariable = project)
projectchoosen['values'] = ('Somatic DNA', 'Somatic RNA','Germline')
projectlabel.config(font=('Nunito Sans',13))

#submit button
sub_btn=tk.Button(window,text = 'Run FQ & CA', command = submit, height = 1, width = 22)

#Quit button
close_btn=tk.Button(window, text="Quit", command=window.destroy, height = 1, width = 22)


################# Positioning ##########################
samplelabel.grid(row=0,column=0,pady=3)
browse_btn.grid(row=0, column=1,pady=3)
sub_btn.grid(row=4,column=0,pady=3)
close_btn.grid(row=12,column=0,pady=3)
kitlabel.grid(row=1, column=0,pady=3)
kitchoosen.grid( row = 1,column = 1,pady=3)
projectlabel.grid(row=2,column=0,pady=3)
projectchoosen.grid(row=2, column=1,pady=3)


window.mainloop()        
  







