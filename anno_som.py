import os
import globalv
import re

#current working directory
global GUIpath
GUIpath=os.getcwd()

#choosing the location for annotation (should contain list.txt)
location= globalv.location
projectdir= globalv.projectdir

def anno():
    
    #copying annotation.sh and config.pl to the selected location
    loc_ann_file= GUIpath + '/Annotation/annotation_mod.sh'
    loc_confi_file= GUIpath + '/Annotation/config.pl'
    os.system('cp '+ loc_ann_file + ' ' + location)
    os.system('cp '+ loc_confi_file + ' ' + location)

    #giving the necessary permissions
    os.chdir(location)
    os.system('chmod 777 *')

    #modifying the annotation_mod.sh file
    annofile=location+'/annotation_mod.sh'
    print(annofile)
    
    # Read in the file
    with open(annofile, 'r') as file :
        filedata = file.read()

    # Replace the target string
        filedata = filedata.replace('{{projectdir}}', projectdir)

    # Write the file out again
    with open(annofile, 'w') as file:
        file.write(filedata)

    os.system('sh annotation_mod.sh')
