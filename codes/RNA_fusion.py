import os
import pandas as pd
import glob
from importlib import reload

import globalv


def rna_fusion():
	reload(globalv)
	path= globalv.location
	projectdir=globalv.projectdir

	#copying the files from basespace to local system
	f = open(path+'/'+'list.txt')
	for line in f:
		line_1=line.replace('\n',"")
		print(line_1)
		os.system("echo '##########Starting copying preliminary, coverage and general stats files from basespace #################'")
		command_n='cp ' +str(projectdir) + '/AppResults/'+line_1+'_*/Files/'+line_1+'.fusion_candidates.preliminary '+path+'/'
		#print(command_n)
		command_m='cp' +str(projectdir) + '/AppResults/'+line_1+'_*/Files/multiqc_data/multiqc_general_stats.txt '+path+'/'
		rename1='mv '+path+'/multiqc_general_stats.txt '+path+'/'+line_1+'_multiqc_general_stats.txt'
		command_o='cp ' +str(projectdir) + '/AppResults/'+line_1+'_*/Files/'+line_1+'.qc-coverage-region-1_coverage_metrics.csv '+path+'/'
		os.system(command_n)
		os.system(command_m)
		os.system(rename1)
		os.system(command_o)
		os.system("echo '##########Done copying preliminary, coverage and general stats files from basespace #################'")

	os.system("echo '################## ALL FILES ARE DONE ###########################'")
	mkdir_cmd='mkdir '+ path +'/'+'modified_files'
	os.system(mkdir_cmd)
	os.system("echo '################## CREATED DIRECTORY modified_files ###########################'")
	

	files = glob.glob(os.path.join(path,"*.preliminary"))
	
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
		