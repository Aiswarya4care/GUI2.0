import os
import numpy as np
import pandas as pd
import tkinter as tk
import warnings
from importlib import reload
import config_gui
from config_gui import tmbpanelsize
import globalv

global GUIpath
GUIpath=config_gui.GUIpath
    

def tmb_calculation():
    GUIpath=config_gui.GUIpath
    reload(globalv)
    dirpath= globalv.location
    capturingkit=globalv.capturingkit
    panelsize=tmbpanelsize[capturingkit] #number that has to be divided with for tmb calculation

    cohort4= pd.read_csv(GUIpath+ "/filter/4basecare-germline-cohort.csv")

    #fetching sample folders
    files= os.listdir(dirpath + "/annotation/FE_merged/")
    warnings.filterwarnings("ignore")

            
    tmb_filtered_df= pd.DataFrame(columns=['samplename','total_var','after pass','after allele freq', 'after mq', 'after dp', 'after exonic', 'after synony', 'after pop_freq', 'after allele freq2', 'after cohort4', 'tmb'])

    #processing every sample in folder one by one
    for f in files:
        num=files.index(f)
        ################## TMB Calculation #########################
        
        dftmb= pd.read_csv(dirpath + "/annotation/FE_merged/"+f)
        
        tot_var=len(dftmb)
        ##################### After PASS filter ##################
        
        dftmb=dftmb[dftmb['FILTER']=='PASS']
        
        afpass=len(dftmb)
        
        ######### filtering allele frequency ###############
        
        allele_freq=list(dftmb.columns[dftmb.columns.str.contains(':AF')])[0]
        dftmb[allele_freq]=dftmb[allele_freq].replace('.',100).fillna(100) 
        dftmb[allele_freq]=  dftmb[allele_freq].astype(float)
        dftmb=dftmb[dftmb[allele_freq]>=0.05]
            
        afallele=len(dftmb)
        
        
        ######## filtering MQ ###################
        mq=list(dftmb.columns[dftmb.columns.str.contains(':MQ')])[0]
        dftmb[mq]=dftmb[mq].replace('.',100).fillna(100) 
        dftmb[mq]=  dftmb[mq].astype(float)
        dftmb=dftmb[dftmb[mq]>=20]
        
        afmq=len(dftmb)
        
        ########## Filtering DP
        dp=list( dftmb.columns[dftmb.columns.str.contains(":DP")])[0]
        dftmb[dp]=dftmb[dp].replace('.',100).fillna(100) 
        dftmb[dp]=  dftmb[dp].astype(float)
        dftmb=dftmb[dftmb[dp]>=30]
        
        afdp=len(dftmb)

        
        ####### filtering Func.knownGene

        dftmb= dftmb[dftmb['Func.ensGene'].str.contains('exonic|splicing', case=False, regex=True)]
        dftmb= dftmb[dftmb['Func.ensGene'].str.contains('RNA')==False]
        afknowngene= len(dftmb)   
        
        ##### filtering synonymous
        dftmb= dftmb[dftmb['ExonicFunc.ensGene']!='synonymous SNV']
        dftmb= dftmb[dftmb['ExonicFunc.ensGene']!='.'] #commented on 10/12/2021 Friday
        afsynony= len(dftmb)  
        
        #####filtering pop freq
        
        popfreqs=['ExAC_ALL','ExAC_SAS','AF','AF_sas','1000g2015aug_all','1000g2015aug_SAS']
            
        print(f + " tmb filtering in progress..")
        for p in popfreqs:
            dftmb[p]=dftmb[p].replace('.',0).fillna(0) 
            dftmb[p]=  dftmb[p].astype(float)
            dftmb=dftmb[dftmb[p]< 0.01]
            
        afpop=len(dftmb)
            
        ########## Filtering allele freq 0.44 & 0.55
        dftmb=dftmb[(dftmb[allele_freq]>=0.55) | (dftmb[allele_freq]<=0.44)]
        
        af_alfq=len(dftmb)
        


        ################## Final step of filtration ###############
        
        ####################### Removing 4basecare cohort alone ###############
        cohort4=cohort4.rename(columns={'chr':'CHROM_x', 'start':'POS_x', 'ref':'REF_x', 'alt':'ALT_x'})
        cohort4['POS_x']=[str(i) for i in cohort4['POS_x']]
        dftmb['POS_x']=[str(i) for i in dftmb['POS_x']]
        df_filter=dftmb.merge(cohort4, how = 'left', on= ['CHROM_x','POS_x','REF_x','ALT_x'])
        afcohort4= len(dftmb)
        
        print(f + " :tmb-filtered")
        ###################################
        ### making filtered csv after tmb calculation
        tmb= round(afcohort4/panelsize,2)
        to_append= [f,tot_var,afpass,afallele, afmq, afdp,afknowngene,afsynony,afpop,af_alfq,afcohort4,tmb]
        
        dflen=len(tmb_filtered_df)
        tmb_filtered_df.loc[dflen]=to_append
        print(to_append)  
        
        print( "###" + str(num+1) + " out of " + str(len(files)) + " files done")


    tmb_filtered_df.to_csv(dirpath + '/tmbinfo.csv', index=False)    
    dftmb.to_csv(dirpath+"/FE_filtered/" + f + "_filtered.csv", index=False)   

    print("#############################")
    print("############ DONE ###########")
    print("#############################")


    ############################################################_END FILTER_ENGINE ############################################################