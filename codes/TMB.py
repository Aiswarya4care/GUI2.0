import os
import numpy as np
import pandas as pd
import tkinter as tk
import warnings
from importlib import reload
import config_gui

import globalv

global GUIpath
GUIpath=config_gui.GUIpath
    

def tmb_calculation():
    reload(globalv)
    dirpath= globalv.location
    
    collist= pd.read_csv(GUIpath+ "/filter/columns39.csv")
    cohort4= pd.read_csv(GUIpath+ "/filter/4basecare-germline-cohort.tsv",sep='\t')
    folders= os.listdir(dirpath)
    
    os.system("mkdir " + dirpath + "/tmbmerged")
    os.system("mkdir " + dirpath + "/tmbfiltered")
    warnings.filterwarnings("ignore")
    
    filtered_df= pd.DataFrame(columns=['samplename','total_var','after pass','after allele freq', 'after mq', 'after dp', 'after exonic', 'after synony', 'after pop_freq', 'after allele freq2', 'after cohort4'])
    
    for f in folders:
        num=folders.index(f)
        f_path= dirpath + "/" + f
        files= os.listdir(f_path)
        cancer= [obj for obj in files if 'cancervar.hg19_multianno.txt.cancervar' in obj]
        annovar= [obj for obj in files if '_out.hg19_multianno' in obj]
        vcf= [obj for obj in files if 'final.tab' in obj]
        print(f)
    
        #locations of different files
        cancerloc= dirpath + "/" + f + "/" + cancer[0]
        vcfloc= dirpath + "/" + f + "/" + vcf[0]
        annoloc= dirpath + "/" + f + "/" + annovar[0]
    
        cancercol=collist['cancervar'][collist['cancervar'].notna()]
        cancervar= pd.read_csv(cancerloc, usecols=cancercol, sep='\t')
        
        vcfcol=collist['vcf_wo_art'][collist['vcf_wo_art'].notna()]
        vcfcol=[int(i) for i in vcfcol]
        vcf= pd.read_csv(vcfloc, usecols=vcfcol, sep='\t')
        
        annocol=collist['multianno'][collist['multianno'].notna()]
        annovar= pd.read_csv(annoloc,usecols=annocol, sep='\t')
        
        # modifying vcf position values
        
        for i in range(len(vcf)):
            if len(vcf['REF'][i])>len(vcf['ALT'][i]):
                vcf['POS'][i]=vcf['POS'][i]+1
                
        #rename annovar columns
        annovar=annovar.rename(columns={'Chr':'CHROM', 'Start': 'POS', 'Ref':'REF', 'Alt':'ALT','Gene.knownGene':'Ref.Gene' })
        
        #rename annovar columns
        cancervar=cancervar.rename(columns={'#Chr':'CHROM', 'Start': 'POS', 'Ref':'REF', 'Alt':'ALT','Gene.knownGene':'Ref.Gene' })
        
            
        cancervar['CHROM']=list(map(str, cancervar['CHROM']))
        cancervar['CHROM']='chr' + cancervar['CHROM']
        
        aicdf= pd.merge(annovar,cancervar, on= ['CHROM','POS','End','REF','ALT'])
        merged_df= pd.merge(vcf, aicdf, how='outer', on= ['CHROM','POS'])
           
        merged_df.fillna('.', inplace = True)
        
        #preparing intervar_inhouse columns
        for i in range(30,57):
            merged_df[merged_df.columns[i]]=merged_df.columns[i]+ ":" + merged_df[merged_df.columns[i]]
        
        merged_df['intervar_inhouse']=merged_df[list(merged_df.columns[30:57])].apply(lambda x: ', '.join(x[x.notnull()]), axis = 1)
        
        print(f + " : merged")
                         
        final_df=merged_df          
        tot_var=len(final_df)
             
        output_path= dirpath + "/tmbmerged/" + f + '_merged_output.csv'        
        final_df.to_csv(output_path, index=False)
        
        ####################################
        ############## Filtration ##########
        
        df= final_df
        
        ##################### After PASS filter ##################
        
        df=df[df['FILTER']=='PASS']
        
        afpass=len(df)
        
        ######### filtering allele frequency ###############
        
        allele_freq=list(df.columns[df.columns.str.contains(':AF')])[0]
        df[allele_freq]=df[allele_freq].replace('.',100).fillna(100) 
        df[allele_freq]=  df[allele_freq].astype(float)
        df=df[df[allele_freq]>=0.05]
            
        afallele=len(df)
        
        
        ######## filtering MQ ###################
        mq=list(df.columns[df.columns.str.contains(':MQ')])[0]
        df[mq]=df[mq].replace('.',100).fillna(100) 
        df[mq]=  df[mq].astype(float)
        df=df[df[mq]>=20]
           
        afmq=len(df)
        
        ########## Filtering DP
        dp=list( df.columns[df.columns.str.contains(":DP")])[0]
        df[dp]=df[dp].replace('.',100).fillna(100) 
        df[dp]=  df[dp].astype(float)
        df=df[df[dp]>=30]
        
        afdp=len(df)

        
        ####### filtering Func.knownGene
       
        df= df[df['Func.ensGene'].str.contains('exonic|splicing', case=False, regex=True)]
        df= df[df['Func.ensGene'].str.contains('RNA')==False]
        afknowngene= len(df)   
        
        ##### filtering synonymous
        df= df[df['ExonicFunc.ensGene']!='synonymous SNV']
        df= df[df['ExonicFunc.ensGene']!='.'] #commented on 10/12/2021 Friday
        afsynony= len(df)  
        
        #####filtering pop freq
        
        popfreqs=['ExAC_ALL','ExAC_SAS','AF','AF_sas','1000g2015aug_all','1000g2015aug_SAS']
            
        print(f + " filtering in progress..")
        for p in popfreqs:
            df[p]=df[p].replace('.',0).fillna(0) 
            df[p]=  df[p].astype(float)
            df=df[df[p]< 0.01]
            
        afpop=len(df)
            
        ########## Filtering allele freq 0.44 & 0.55
        df=df[(df[allele_freq]>=0.55) | (df[allele_freq]<=0.44)]
        
        af_alfq=len(df)
        
    
        
        ################## Final step of filtration ###############
        
        ####################### Removing 4basecare cohort alone ###############
        cohort4=cohort4.rename(columns={'chr':'CHROM', 'start':'POS', 'ref':'REF_x', 'alt':'ALT_x'})
        df=df.merge(cohort4, how = 'outer',on= ['CHROM','POS','REF_x','ALT_x'],indicator=True).loc[lambda x : x['_merge']=='left_only']
    
        afcohort4= len(df)
        
       ################################################################################
            
        print(f + " :filtered")
        ###################################
        ### making filtered csv
        to_append= [f,tot_var,afpass,afallele, afmq, afdp,afknowngene,afsynony,afpop,af_alfq,afcohort4]
        dflen=len(filtered_df)
        filtered_df.loc[dflen]=to_append
        print(to_append)  
        
        output_path= dirpath + "/tmbfiltered/" + f + '_filtered_output.csv'        
        df.to_csv(output_path, index=False)
        
        print( "###" + str(num+1) + " out of " + str(len(folders)) + " files done")
                
    filtered_df.to_csv(dirpath+"/"+"tmb_filtered.csv", index=False)    
    
    print("#############################")
    print("############ DONE ###########")
    print("#############################")
