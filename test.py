import os
import globalv
import config_gui
from config_gui import bed_ids

#current working directory
global GUIpath
GUIpath=os.getcwd()
location= globalv.location
dragen_bed=globalv.dragen_bed
sample_type=globalv.sample_type
appsess=globalv.appsess
projectdir=globalv.projectdir

#fetching project id from config_gui file
proj_somatic_dna=config_gui.proj_somatic_dna
proj_germline=config_gui.proj_germline
proj_somatic_rna=config_gui.proj_somatic_rna
fastqc= config_gui.fastqc
print(bed_ids[dragen_bed])

