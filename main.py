import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from cutadapt import cafa

window=tk.Tk()

# declaring string variab nle
library_kit=tk.StringVar()
location_name=tk.StringVar()
project= tk.StringVar()
folderPath=tk.StringVar()
appsession_name=tk.StringVar()

#setting the windows size
window.geometry("650x600")
window.title("Patient Data Processing")  


def browse():
    global folderPath
    global project
    global library_kit
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)
    

def cafamain():
    libkit=library_kit.get()
    proj= project.get()
    location = folderPath.get()
    file1 = open('/home/ash/Documents/GitHub/GUI2.0/globalv.py',"w+")
    file1.write('location=' + "'" + location + "'")
    file1.write('\n' + 'libkit=' + "'" + libkit + "'")
    file1.write('\n' +'proj=' + "'" + proj + "'")
    file1.close()
    print('###### Done ########')

def test():
    cafa()
    

################################################
############# Button ###########################
################################################

#test button
testlabel= tk.Label(window, text='test')
test_btn=tk.Button(window,text = 'test', command = test, height = 1, width = 18)
testlabel.config(font=('Nunito Sans',13))

#browse button
samplelabel= tk.Label(window, text='Choose folder path')
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
cafa_btn=tk.Button(window,text = 'Submit', command = cafamain, height = 1, width = 22)

#Quit button
close_btn=tk.Button(window, text="Quit", command=window.destroy, height = 1, width = 22)


################# Positioning ##########################
test_btn.grid(row=5, column=0,pady=3)
samplelabel.grid(row=0,column=0,pady=3)
browse_btn.grid(row=0, column=1,pady=3)
cafa_btn.grid(row=4,column=0,pady=3)
close_btn.grid(row=12,column=0,pady=3)
kitlabel.grid(row=1, column=0,pady=3)
kitchoosen.grid( row = 1,column = 1,pady=3)
projectlabel.grid(row=2,column=0,pady=3)
projectchoosen.grid(row=2, column=1,pady=3)



window.mainloop()        
  







