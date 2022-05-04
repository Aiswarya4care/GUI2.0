import os
import globalv
import config_gui
from importlib import reload


def cgi():
    os.system()
    reload(globalv)
    GUIpath=config_gui.GUIpath
    location= globalv.location
    cgi_data=config_gui.cgi_data
    
    #copying cgi script to the selected location
    loc_cgi_file= GUIpath.split('/codes/')[0] + '/cgi/cgikrispy2.sh'
    os.system('cp '+ loc_cgi_file + ' ' + location + 'CGI')
    
    #giving the necessary permissions
    os.chdir(location)
    os.system('chmod 777 *')


    cgifile=location+'CGI/cgikrispy2.sh'
   
    # Reading cgi script for modification
    with open(cgifile, 'r') as file :
        cgifiledata = file.read()

    # Replace the cgi data location
        cgifiledata = cgifiledata.replace('{{cgi_data}}', cgi_data)
    
    os.system("bash " + cgifile )
