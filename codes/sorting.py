import os
import globalv
import glob
import shutil

def sort():
    location= globalv.location
    sample_type=globalv.sample_type

    os.chdir(location)
    samples=glob.glob("*fastq.gz")

    if sample_type=='RNA':
        s=list(filter(lambda x:'-ST8-' in x, samples))
        c=list(filter(lambda x:'-CT-' in x, samples))
        s_pattern='/ST8'
        c_pattern='/CT'
    else:
        s=list(filter(lambda x:'-SE8-' in x, samples))
        c=list(filter(lambda x:'-CE-' in x, samples))
        s_pattern='/SE8'
        c_pattern='/CE'


    if len(s)>0:
        os.system('mkdir '+ location + s_pattern)
        os.chdir(location)
        for sf in s:
            shutil.move(sf,location + s_pattern)
        
    if len(c)>0:
        os.system('mkdir '+ location + c_pattern)
        os.chdir(location)
        for cf in c:
            shutil.move(cf,location + c_pattern)
        
