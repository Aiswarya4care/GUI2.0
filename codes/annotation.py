import os
import globalv
import config_gui
from importlib import reload


def anno():
    #fetching the location for annotation (should contain list.txt) and the project dir
    reload(globalv)
    GUIpath=config_gui.GUIpath
    location= globalv.location
    projectdir= globalv.projectdir

    #making a directory in 
    os.system('mkdir '+ location + '/annotation')
    #fetching config location from config_gui file
    annotation_db= config_gui.annotation_db
    simplifyvcf= config_gui.simplifyvcf

    #copying annotation.sh and config.pl to the selected location
    loc_ann_file= GUIpath + '/annotation/annotation_mod.sh'
    loc_confi_file= GUIpath + '/annotation/config.pl'
    os.system('cp '+ loc_ann_file + ' ' + location + '/annotation/')
    os.system('cp '+ loc_confi_file + ' ' + location+ '/annotation/')

    #giving the necessary permissions
    os.chdir(location + '/annotation/')
    os.system('chmod 777 *')


    #modifying the annotation_mod.sh file
    annoconfigfile=location+'/annotation/config.pl'
   
    # Reading annotation_mod script for modification
    with open(annoconfigfile, 'r') as file :
        annoconfigdata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
        annoconfigdata = annoconfigdata.replace('{{annotation_db}}', annotation_db)
        

    #modifying the annotation_mod.sh file
    annofile=location+'/annotation/annotation_mod.sh'
   
    # Reading annotation_mod script for modification
    with open(annofile, 'r') as file :
        filedata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
        filedata = filedata.replace('{{projectdir}}', projectdir)
        filedata = filedata.replace('{{annotation_db}}', annotation_db)
        filedata = filedata.replace('{{simplifyvcf}}', simplifyvcf)
        filedata = filedata.replace('{{location}}', location + '/annotation/')
    # Write the file out again
    with open(annofile, 'w') as file:
        file.write(filedata)

    os.system('sh annotation_mod.sh')
