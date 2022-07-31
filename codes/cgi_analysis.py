import os
import globalv
import config_gui
from importlib import reload
import glob
import numpy as np

def cgi():
    
    reload(globalv)
    GUIpath=config_gui.GUIpath
    location= globalv.location
    cgi_data=config_gui.cgi_data
    
   #copying cgi script to the selected location
    os.system('mkdir ' + location + '/cgi')
    loc_cgi_file= GUIpath + '/cgi/cgikrispy2.sh'
    os.system('cp '+ loc_cgi_file + ' ' + location + '/cgi/')

    ######## fetching sample names ########
    samples= glob.glob(location+"/panel/*_panel.vcf")
    samples=np.array(samples).tolist()
    samples=[i.split('/panel/')[1] for i in samples]
    #giving the necessary permissions
    os.chdir(location)
    os.system('chmod 777 *')


    cgifile=location+'/cgi/cgikrispy2.sh'
    
    # Reading cgi script for modification
    with open(cgifile, 'r') as file :
        cgifiledata = file.read()

    # Replace the cgi data location and samples
        cgifiledata = cgifiledata.replace('{{samplenames}}', str(samples).strip("[]").replace("'","").replace(",",""))
        cgifiledata = cgifiledata.replace('{{cgi_data}}', cgi_data)

    with open(cgifile, 'w') as file:
            file.write(cgifiledata)
            
    os.system("bash " + cgifile )
