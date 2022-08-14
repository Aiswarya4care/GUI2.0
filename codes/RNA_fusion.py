import os
import pandas as pd
import glob
from importlib import reload
import numpy as np
import globalv


def rna_fusion():
	reload(globalv)
	path= globalv.location
	projectdir=globalv.projectdir

	file_list=os.listdir(path)

	if 'fusions' in file_list:
		os.system("rm -r " + path + "/fusions")

	os.system("mkdir "+ path+ "/fusions")
	os.system('mkdir '+ path +'/fusions/'+'modified_files')

	samples=glob.glob(path+"/*_R1_fastq.gz")
	samples=[s.split('/')[-1] for s in file_list]
	samples=[s.split('_R1')[0] for s in samples]
	samples= pd.unique(samples)
	samples=np.array(samples).tolist()

	print(samples)
	
	fusioncreate= path +  "/fusions/fusions.sh"
	f1= open(fusioncreate,"x")
	f1.close()
	f1= open(fusioncreate,"w+")
	f1.write("cd "+ path + "/fusions" + '\n')

	f1= open(fusioncreate,"x")
	f1.close()
	f1= open(fusioncreate,"w+")
	f1.write("echo '##########Starting copying preliminary, coverage and general stats files from basespace #################'")

	for s in samples:
			f1.write('\n' +'cp ' +str(projectdir) + '/AppResults/'+s+'_*/Files/'+s+'.fusion_candidates.preliminary '+path+'/fusions/')
			f1.write('\n' +'cp' +str(projectdir) + '/AppResults/'+s+'_*/Files/multiqc_data/multiqc_general_stats.txt '+path+'/fusions')
			f1.write('\n' +'mv '+path+'/multiqc_general_stats.txt '+path+'/'+s+'_multiqc_general_stats.txt')
			f1.write('\n' +'cp ' +str(projectdir) + '/AppResults/'+s+'_*/Files/'+s+'.qc-coverage-region-1_coverage_metrics.csv '+path+'/')
			f1.write('\n' + "echo '##########Done copying preliminary, coverage and general stats files from basespace #################'")
	f1.write('\n' +"echo '################## ALL FILES ARE DONE ###########################'")
	f1.write('\n' +"echo '################## CREATED DIRECTORY modified_files ###########################'")
	f1.close()

	files = glob.glob(os.path.join(path+"/fusions/","*.preliminary"))
	
	#Editing Score coloumn
	for fp in files:
		df = pd.read_table(fp, sep='\t')
		df["Score"] = df["Score"].astype(float)
		df["Score"] = df["Score"].round(5)
		df["Score"] = df["Score"].astype(str)
		f_name=os.path.basename(fp).split('.')[0]
		df.to_excel(path+r'/modified_files/'+f_name+'_FUS_P'+'.xlsx', index = False)

	os.system("echo '################## ALL FILES SCORE COLUMN FORMAT MODIFICATION DONE ###########################'")
	
	files_1 = glob.glob(os.path.join(path,"*_general_stats.txt"))
	for fp in files_1:
		df = pd.read_csv(fp, sep = "\t")
		df1 = df.transpose()
		f_name=os.path.basename(fp).split('.')[0]
		df1.to_excel(path+r'/'+f_name+'.xlsx', index = False)
		