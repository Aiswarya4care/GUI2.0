import os
import numpy as np
import pandas as pd
import tkinter as tk
import glob
from tkinter import filedialog
from tkinter import messagebox
from functools import reduce
from importlib import reload

import globalv


def gene_cov():
	reload(globalv)
	path= globalv.location
	projectdir=globalv.projectdir

	mkdir_cmd_2='mkdir '+ path +'/'+'sample_coverage'
	os.system(mkdir_cmd_2)
		
	f = open(path+'/'+'list.txt')
	for line in f:
		line_2=line.replace('\n',"")
		print('##########Starting Coverage Calculation for '+line_2+' #################')
		#next line will take bam directly from basespace & process not need to copy
		comd_2='bedtools bamtobed -i '+ projectdir + '/AppResults/'+line_2+'/Files/'+line_2+'.bam | bedtools coverage -a /home/ubuntu/Patient_Sample_Processing/bed_files/Indiegene_gene_coverage_bed/Indiegene_intersected_V8.bed -b - > '+path+'/sample_coverage/'+line_2+'.coverage'
		os.system(comd_2)
		'''
		if "-F-" or "-F1-" or "-F2-" or "-Z-" in line_2:
			comd_2='bedtools bamtobed -i /home/ubuntu/basespace/Projects/Somatic_Patient_Samples_3/AppResults/'+line_2+'/Files/'+line_2+'.bam | bedtools coverage -a /home/ubuntu/Patient_Sample_Processing/bed_files/Indiegene_bed_files/Indiegene_V8.bed -b - > '+path+'/sample_coverage/'+line_2+'.coverage'
			os.system(comd_2)
		elif '-B-' in line_2:
			comd_2='bedtools bamtobed -i /home/ubuntu/basespace/Projects/Germline_Patient_Samples_January/AppResults/'+line_2+'/Files/'+line_2+'.bam | bedtools coverage -a /home/ubuntu/Patient_Sample_Processing/bed_files/Indiegene_bed_files/Indiegene_V8.bed -b - > '+path+'/sample_coverage/'+line_2+'.coverage'
			os.system(comd_2)
		'''
		print('##########Ending Coverage Calculation for '+line_2+' #################')

def compile_gene_cov():
	reload(globalv)
	path= globalv.location
	mkdir_cmd_3='mkdir '+ path +'/'+'Average'
	os.system(mkdir_cmd_3)
	f = open(path+'/'+'list.txt')
	for line in f:
		line_2=line.rstrip("\n")
		print('Processing Average Coverage for each Gene in Sample '+line_2+' : ' + '\033[1m'+'STARTED'+'\033[0m')
		f = open(path+'/'+'genelist_required.txt')
		for line_3 in f:
			line_3a=line_3.rstrip("\n")
			comd_1a = 'grep '+line_3a+' '+path+'/sample_coverage/'+line_2+'.coverage'+' | '+'awk \'{ total += $8 } END { print total/NR }\''+' > '+path+'/Average/'+line_3a+'.average'+' | '+ 'cat '+path+'/Average/*average > '+path+'/Average/average.txt'
			os.system(comd_1a)
			comd_1b= 'sort '+path+'/'+'genelist_required.txt '+'| '+ 'paste - ' +path+'/Average/average.txt > '+path+'/avg_'+line_2+'.tsv'
			os.system(comd_1b)
		print('########Genes from GeneList under process for Average Coverage########')
		print('Processing Average Coverage for each Gene in Sample '+line_2+' : ' + '\033[1m'+'DONE & COMPILED'+'\033[0m'+'\n')
	os.system('echo "################## ALL RESULTS GENERATED ########################"')
	os.system('echo "Removing unnecessary files"')
	rm_cmd_1='rm '+ path +'/Average/'+'*average'
	os.system(rm_cmd_1)
	os.system('echo "################## Files Removed ########################"')
	tsv_files = glob.glob(os.path.join(path, "*.tsv"))
	samples = [] #defining list
	for filename in tsv_files:
		sample_cn=os.path.basename(filename).split('.')[0]
		a='Coverage_'+sample_cn 
		df=pd.read_csv(filename,header=None , sep='\t', usecols=[0,1], names=['Gene',a])
		df[a]=df[a].fillna(0)
		df[a]=df[a].astype(float).map("{:.2%}".format)
		samples.append(df)
		#print(samples)
	sample_all = reduce(lambda left,right: pd.merge(left,right,on='Gene',how='outer'), samples)
	sample_all.to_excel(path+"/all_sample_coverage.xlsx", index = False)
	rm_cmd_2='rm '+ path+'/'+'avg_*' #added on 12 Jan 2022
	os.system(rm_cmd_2) #added on 12 Jan 2022
	os.system("echo '########## Ending Process #################'")
