import os
import numpy as np
import pandas as pd
import glob
import tkinter as tk
from functools import reduce
import inflect
from importlib import reload

import globalv

path= globalv.location
libkit=globalv.libkit
proj=globalv.proj

def cnvmerge():
	files = glob.glob(os.path.join(path,"*_cnv_output.txt"))
	
	def concat_arrange(fp):
		df = pd.read_csv(fp, sep='\t')
		df['Combined'] = df['Chromosome'].map(str) + ':' + df['Start'].map(str) + '-' + df['End'].map(str) +'|'+ df['Predicted_copy_number'].map(str)+ ':' + df['Type_of_alteration'].map(str)
		sample_col_name=os.path.basename(fp).split('_')[0]
		a='Combined'
		df.rename(columns = {a: sample_col_name}, inplace = True)
		df1 = df[['Gene',sample_col_name]]
		df1.to_csv(path + r'/concatenate/'+ sample_col_name + '.csv', index = False)

	for f in files:
		concat_arrange(f)

	#collect the targetgene list file and other sample file paths
	csv_files = glob.glob(os.path.join(path,'concatenate', "*.csv"))
	#sort to keep the file of targetgene list first as we are using left merge.
	csv_files.sort()


	samples = [] #defining list
	
	for filename in csv_files:
		df=pd.read_csv(filename,encoding= 'unicode_escape') #taking in the files as dataframes
		p = inflect.engine() #reqired for grouping
		df['Gene'] += df.groupby('Gene').cumcount().add(1).map(p.ordinal).radd(':') #adding suffix to two entry gene
		samples.append(df) #appending all dataframes 
	#lambda uses multiple arguments i.e. varaible samples contains all data in form of dataframes  
	sample_all = reduce(lambda left,right: pd.merge(left,right,on='Gene',how='outer'), samples) 
	sample_all.sort_values(["Gene"], axis=0, inplace=True) #sorting to give ordered data.
	sample_all['Gene'] = sample_all['Gene'].str.split(':').str[0] #spliting out the not required part
	sample_all.drop_duplicates(inplace=True)
	sample_all.to_csv(path + "/all_sample_cnv_per_batch.csv" , index = False) #saving file

	df11=[]
	for fp in csv_files:
		#attaches extra column with information of sample ID
		df12=pd.concat([pd.read_csv(fp,encoding= 'unicode_escape').assign(Sample=os.path.basename(fp).split('-')[0])]) 
		#reqired for grouping
		p = inflect.engine() 
		#checks for multiple gene records and attaches number
		df12['Gene'] += df12.groupby('Gene').cumcount().add(1).map(p.ordinal).radd(':')
		#storing the in coloumn name
		cna_col=df12.columns[1]
		#combining required columns
		df12['ID_Combined'] = df12[['Sample',cna_col ]].agg('||'.join, axis=1)
		#Renaming column
		sample_col_name_1=os.path.basename(fp).split('.')[0]
		df12.rename(columns = {'ID_Combined': sample_col_name_1}, inplace = True)
		#filtering out coloumns required
		df_12 = df12[['Gene',sample_col_name_1]]
		df11.append(df_12)

	#merging files appended to df11
	sample_all_1 = reduce(lambda left,right: pd.merge(left,right,on='Gene',how='outer'), df11)
	sample_all_1.sort_values(["Gene"], axis=0, inplace=True)
	#leaves the first 2 coloumns and concatenate others into one using separator
	sample_all_1["ID_Combined"] = sample_all_1[sample_all_1.columns[2:]].apply(lambda x: ';'.join(x.dropna().astype(str)),axis=1)

	#filtering out coloumns required
	Gene_comb_1 = sample_all_1[['Gene','ID_Combined']]
	#if required saving file 
	#Gene_comb_1.to_csv("gene_cnv_all_1.csv", index = False)

	#function to process the files to get Gene, Smaple_ID, Combined CNV
	#fp = files gene_comb = all gene mapped to CNV  from all samples
	def copy_num_alteration_2(fp,gene_comb):
		df_5 = pd.read_csv(fp,encoding= 'unicode_escape') #importing in dataframe
		df_5['Gene'] += df_5.groupby('Gene').cumcount().add(1).map(p.ordinal).radd(':') #checking for duplicate and renaming them
		df_6=pd.merge_ordered(df_5, gene_comb, on="Gene", how ='left') #merging each data with 
		df_6['Gene'] = df_6['Gene'].str.split(':').str[0] #split number pattern from gene name and numbering pattern keep gene name
		a =df_6.columns[1] #takes in coloumn name 
		df_7 = df_6.filter(['Gene', a , 'ID_Combined']) #filters out 
		sample_col_name=os.path.basename(fp).split('-')[0] #name sample id to be taken for replacement
		df_7.rename(columns = {a: sample_col_name}, inplace = True) #replace orignal name with just ID
		f_name=os.path.basename(fp).split('.')[0] #for file name.
		#df_7.to_excel(path + r'/final_files/'+f_name+'_CNV'+'.xlsx', index = False)
		df_7.to_excel(path + r'/final_files/'+f_name+'_indiegene_CNV'+'.xlsx', index = False)  #use when merging indiegene files
		# above line saving file  #above line changed on 23-NOV-21 10 am 

	#creating files for each sample

	for file_n in csv_files:
		copy_num_alteration_2(file_n,Gene_comb_1)

	os.remove(path + r'/final_files/A_target_gene_indiegene_CNV.xlsx') #use when merging indiegene files
