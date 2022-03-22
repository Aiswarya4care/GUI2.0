import os
import globalv
import config_gui
import re
from importlib import reload

#current working directory
global GUIpath
GUIpath=os.getcwd()


def anno():
    #fetching the location for annotation (should contain list.txt) and the project dir
    reload(globalv)
    location= globalv.location
    projectdir= globalv.projectdir
    
    #fetching config location from config_gui file
    annotation_db= config_gui.annotation_db
    annotation_spk= config_gui.annotation_spk
    simplifyvcf= config_gui.simplifyvcf

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
    # Read in the file
    with open(annofile, 'r') as file :
        filedata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
        filedata = filedata.replace('{{projectdir}}', projectdir)
        filedata = filedata.replace('{{annotation_db}}', annotation_db)
        filedata = filedata.replace('{{annotation_spk}}', annotation_spk)
        filedata = filedata.replace('{{simplifyvcf}}', simplifyvcf)

    # Write the file out again
    with open(annofile, 'w') as file:
        file.write(filedata)

    os.system('sh annotation_mod.sh')
