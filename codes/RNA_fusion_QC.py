import os
import pandas as pd
import glob
from importlib import reload
import config_gui
import globalv
import pyfiglet
from alive_progress import alive_bar
import tabletext

def rna_fusion_qc():
	reload(globalv)
	path= globalv.location
	projectdir=globalv.projectdir
	GUIpath= config_gui.GUIpath

	#copying the files from basespace to local system
	f = open(path+'/'+'list.txt')
	for line in f:
		line_1=line.replace('\n',"")
		print(line_1)
		os.system("echo '##########Starting copying preliminary, coverage and general stats files from basespace #################'")
		command_n='cp ' +str(projectdir) + '/AppResults/'+line_1+'_*/Files/'+line_1+'.fusion_candidates.preliminary '+path+'/'
		#print(command_n)
		command_m='cp ' +str(projectdir) + '/AppResults/'+line_1+'_*/Files/multiqc_data/multiqc_general_stats.txt '+path+'/'
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

	################ Running coverconcat.sh ######################
	#giving the necessary permissions
	os.chdir(path)
	os.system('chmod 777 *')

    #modifying the annotation_mod.sh file
	coverconcatfile=path+'/ca_fq_dragen36.sh'
    # Read in the file
	with open(coverconcatfile, 'r') as file :
		filedata = file.read()

    # Replace the project directory location, annotation_db. annotation_spk
		filedata = filedata.replace('{{location}}', path)
    
    # Write the file out again
	with open(coverconcatfile, 'w') as file:
		file.write(filedata)
	
	os.system(GUIpath+'/rna_qc_scripts/coverconcat2.sh')	

	################ Running RNA QC script ######################

	disp = pyfiglet.figlet_format("RNA QC METRICS", font = "digital" )
	print(disp)

	##=========CONCATENATION AND GENERATING THE QC METRICS FOR BATCH===============#
	path = os.getcwd()
	dirname = input("Where you want to save the save the file? enter the directory(BATCH NAME) ====> "+"\n"+"-> ")
	path_cov = input("Please input the path of the coverage report file for the batch ==> "+"\n"+"-> ")
	print("\n"+"######### Creating new directory with BATCH NAME --->  " + dirname + "  #########")
	os.mkdir(dirname)
	pattern = "*" + input("\n"+"Pattern or extension of the file to be concatenated ====> "+"\n"+"->")
	print("######### SELECTED PATTERN/EXTENSION FOR CONCATENATION ==> " + pattern +"\n")
	pattern_files = glob.glob(os.path.join(path, pattern))
	allfiles = pattern_files

	dfx = []

	with alive_bar(len(allfiles)) as bar:
		for f in allfiles:
			df = pd.read_csv(f, sep="\t")
			dfx.append(df)
			qc_genstats = pd.concat(dfx)
			bar()

	genfile = dirname + "-genstats_QC.csv"
	qc_genstats.to_csv(dirname+"/"+genfile, index=False)

	print("\n"+"======= CONCATENATION SUCCESSFUL :) ============")
	#==============================================================================#

	#===========MERGING THE TargetCoverage file with generalstats==================#
	coverage = pd.read_csv(path_cov, sep="\t")
	df = pd.merge(qc_genstats, coverage, on='Sample', how='inner')
	#==============================================================================#


	##DECLARING THE QC VARIABLES FOR EASY AND BRIEF OPERATION======================#
	tir = ('DRAGEN mapping_mqc-generalstats-dragen_mapping-Total_input_reads')
	dups = ('DRAGEN mapping_mqc-generalstats-dragen_mapping-Number_of_duplicate_marked_reads_pct')
	insertL = ('DRAGEN mapping_mqc-generalstats-dragen_mapping-Insert_length_median')

	##SCORING======================================================================#
	###===1===###
	df.loc[df[tir] >= 20000000, 'TIP_SC'] = 1
	df.loc[df[dups] <= 55, 'DUPS_SC'] = 1
	df.loc[df[insertL] >= 75, 'INSERT_SC'] = 1
	df.loc[df['TargetCoverage'] >= 30, 'COV_SC'] = 1

	df.loc[df[tir] < 20000000, 'TIP_SC'] = 0
	df.loc[df[dups] > 55, 'DUPS_SC'] = 0
	df.loc[df[insertL] < 75, 'INSERT_SC'] = 0
	df.loc[df['TargetCoverage'] < 30, 'COV_SC'] = 0

	##SUMMING UP THE SAMPLE SCORES##===============================================#
	sc_cols = ['TIP_SC', 'DUPS_SC', 'INSERT_SC', 'COV_SC']
	df['SCORE'] = df[sc_cols].sum(axis=1)

	##ASSIGNING 'STATUS' ACCORDING TO THE SCORES##=================================#
	df.loc[df['SCORE'] >= 4, 'STATUS'] = 'PASS'
	df.loc[df['SCORE'] == 3, 'STATUS'] = 'RECONSIDER'
	df.loc[df['COV_SC'] == 0, 'STATUS'] = 'FAIL'
	df.loc[df['INSERT_SC'] == 0, 'STATUS'] = 'FAIL'
	df.loc[df['TIP_SC'] == 0, 'STATUS'] = 'FAIL'

	##REMARKS COLUMN & RECONSIDERATION##===========================================#

	##LEVEL1, DUPS 55-60##----------------------------------------------------------
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 40000000) & (df[dups] < 60) & (df[dups] > 55) & (df['COV_SC'] == 1), 'REMARKS'] = 'ADEQUATE READS & COVERAGE'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 40000000) & (df[dups] < 60) & (df[dups] > 55) & (df['COV_SC'] == 1), 'STATUS'] = 'PASSED AFTER RECONSIDERATION'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] < 40000000) & (df[dups] < 60) & (df[dups] > 55) & (df['COV_SC'] == 1), 'REMARKS'] = 'LOW INPUT READS'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] < 40000000) & (df[dups] < 60) & (df[dups] > 55) & (df['COV_SC'] == 1), 'STATUS'] = 'FAILED AFTER RECONSIDERATION'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 40000000) & (df[dups] < 60) & (df[dups] > 55) & (df['COV_SC'] == 0), 'REMARKS'] = 'LOW COVERAGE'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 40000000) & (df[dups] < 60) & (df[dups] > 55) & (df['COV_SC'] == 0), 'STATUS'] = 'FAILED AFTER RECONSIDERATION'

	##LEVEL2, DUPS 60-65##----------------------------------------------------------
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 60000000) & (df[dups] < 65) & (df[dups] > 60) & (df['COV_SC'] == 1), 'REMARKS'] = 'ADEQUATE READS & COVERAGE'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 60000000) & (df[dups] < 65) & (df[dups] > 60) & (df['COV_SC'] == 1), 'STATUS'] = 'PASSED AFTER RECONSIDERATION'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] < 60000000) & (df[dups] < 65) & (df[dups] > 60) & (df['COV_SC'] == 1), 'REMARKS'] = 'LOW INPUT READS'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] < 60000000) & (df[dups] < 65) & (df[dups] > 60) & (df['COV_SC'] == 1), 'STATUS'] = 'FAILED AFTER RECONSIDERATION'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 60000000) & (df[dups] < 65) & (df[dups] > 60) & (df['COV_SC'] == 0), 'STATUS'] = 'FAILED AFTER RECONSIDERATION'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 60000000) & (df[dups] < 65) & (df[dups] > 60) & (df['COV_SC'] == 0), 'REMARKS'] = 'LOW COVERAGE'

	##LEVEL3, DUPS 65-70##----------------------------------------------------------
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 80000000) & (df[dups] < 70) & (df[dups] > 65) & (df['COV_SC'] == 1), 'REMARKS'] = 'ADEQUATE READS & COVERAGE'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 80000000) & (df[dups] < 70) & (df[dups] > 65) & (df['COV_SC'] == 1), 'STATUS'] = 'PASSED AFTER RECONSIDERATION'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] < 80000000) & (df[dups] < 70) & (df[dups] > 65) & (df['COV_SC'] == 1), 'REMARKS'] = 'LOW INPUT READS'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] < 80000000) & (df[dups] < 70) & (df[dups] > 65) & (df['COV_SC'] == 1), 'STATUS'] = 'FAILED AFTER RECONSIDERATION'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 80000000) & (df[dups] < 70) & (df[dups] > 65) & (df['COV_SC'] == 0), 'REMARKS'] = 'LOW COVERAGE'
	df.loc[(df['STATUS'] == 'RECONSIDER') & (df[tir] > 80000000) & (df[dups] < 70) & (df[dups] > 65) & (df['COV_SC'] == 0), 'STATUS'] = 'FAILED AFTER RECONSIDERATION'

	##FINAL REMARKS##==============================================================#
	##FINAL ANNOTATION
	df.loc[df['INSERT_SC'] == 0, 'REMARKS'] = 'INSERT LENGTH LESS THAN 75'
	df.loc[df['COV_SC'] == 0, 'REMARKS'] = 'LOW COVERAGE'
	df.loc[df['TIP_SC'] == 0, 'REMARKS'] = 'READS LESS THAN 20M'
	df.loc[df['SCORE'] == 4, 'REMARKS'] = 'PASSED ALL QC CHECKPOINTS'
	df.loc[(df['TIP_SC'] == 0) & (df['COV_SC'] == 0), 'REMARKS'] = 'LOW READS & COVERAGE'
	df.loc[(df['TIP_SC'] == 0) & (df['INSERT_SC'] == 0), 'REMARKS'] = 'LOW READS & INSERT LENGTH LESS THAN 75'
	df.loc[(df['COV_SC'] == 0) & (df['INSERT_SC'] == 0), 'REMARKS'] = 'LOW COVERAGE & INSERT LENGTH LESS THAN 75'
	df.loc[df['SCORE'] == 0, 'REMARKS'] = 'FAILED ALL QC CHECKPOINTS'
	df.loc[(df['SCORE'] == 3) & (df[dups] > 70), 'REMARKS'] = 'DUPS > 70'
	df.loc[df['REMARKS'] == 'DUPS > 70', 'STATUS'] = 'FAILED AFTER RECONSIDERATION'

	##SUMMARY TABLE##==============================================================#
	t_sams = len(df)
	passed = (df['STATUS']=='PASS').sum()
	failed = (df['STATUS']=='FAIL').sum()
	recon_p = (df['STATUS']=='PASSED AFTER RECONSIDERATION').sum() 
	recon_f = (df['STATUS']=='FAILED AFTER RECONSIDERATION').sum() 


	##==THE TABLE==================================================================#
	data = [["PASSED", passed], ["FAILED", failed], ["FAILED AFTER RECON", recon_f], ["PASSED AFTER RECON", recon_p], ["TOTAL SAMPLES", t_sams]]
	print("\n"+"||========SUMMARY=========||"+"\n"+tabletext.to_text(data)+"\n"+"||========SUMMARY=========||"+"\n")

	# GENERATING FILES #############################################################
	newname = dirname + "RAW-RNA-QC.csv"
	df.to_csv(dirname+"/"+newname, index=False)

	#--rearrangement and modification----------------------------------------------#
	df_mod = df.drop(['TIP_SC', 'DUPS_SC', 'INSERT_SC', 'COV_SC', 'SCORE'], axis=1)

	modname = dirname + "RNA-QC.xlsx"
	df_mod = df_mod[['Sample', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Total_input_reads', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Number_of_duplicate_marked_reads_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Insert_length_median', 'TargetCoverage', 'STATUS', 'REMARKS', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Average_sequenced_coverage_over_genome', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Reads_with_mate_sequenced_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-QC_failed_reads_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Mapped_reads_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Unmapped_reads_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Number_of_unique_mapped_reads_excl_duplicate_marked_reads_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Properly_paired_reads_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Not_properly_paired_reads_discordant_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Paired_reads_mapped_to_different_chromosomes_MAPQ_10_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Q30_bases_pct', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Total_alignments', 'DRAGEN mapping_mqc-generalstats-dragen_mapping-Secondary_alignments_pct', 'DRAGEN coverage_mqc-generalstats-dragen_coverage-Aligned_reads', 'DRAGEN coverage_mqc-generalstats-dragen_coverage-Aligned_bases', 'DRAGEN coverage_mqc-generalstats-dragen_coverage-Average_alignment_coverage_over_genome', 'DRAGEN coverage_mqc-generalstats-dragen_coverage-Uniformity_of_coverage_PCT_0_2_mean_over_genome', 'DRAGEN coverage_mqc-generalstats-dragen_coverage-Mean_Median_autosomal_coverage_ratio_over_genome', 'DRAGEN coverage_mqc-generalstats-dragen_coverage-PCT_of_genome_with_coverage_1x_inf', 'DRAGEN coverage_mqc-generalstats-dragen_coverage-PCT_of_genome_with_coverage_20x_inf', 'DRAGEN coverage_mqc-generalstats-dragen_coverage-PCT_of_genome_with_coverage_50x_inf', 'DRAGEN coverage_mqc-generalstats-dragen_coverage-PCT_of_genome_with_coverage_100x_inf']]
	df_mod.to_excel(dirname+"/"+modname, index=False)