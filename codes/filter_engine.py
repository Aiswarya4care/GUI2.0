import os
import pandas as pd
import warnings
import re
from importlib import reload
import config_gui
import globalv

def filtereng():
    GUIpath=config_gui.GUIpath
    reload(globalv)
    dirpath= globalv.location
    sample_type=globalv.sample_type
    test=globalv.test

    #importing external files for filter engine
    collist= pd.read_csv(GUIpath+ "/filter/columns.csv")
    canonical = pd.read_excel(GUIpath+ "/filter/canonical.xlsx", sheet_name=0, mangle_dupe_cols=True, engine='openpyxl')
    
    ######### selecting gene list #############
    genes= pd.read_csv(GUIpath+ "/filter/genelist.csv")
    testgenes= list(genes[test].dropna())
    testgenes=[g.upper() for g in testgenes]

    folders= os.listdir(dirpath)
    #making FE_merged and FE_filtered folders in the destination dir
    os.system("mkdir " + dirpath + "/FE_merged")
    os.system("mkdir " + dirpath + "/FE_filtered")
    warnings.filterwarnings("ignore")
    
    filtered_df= pd.DataFrame(columns=['samplename','total_var','after exonic', 'after synony','after t4', 'after benign', 'after cadd', 'after pop_freq','after gen'])
    
    #processing every sample in folder one by one
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
    
        
        #usecols to specify the columns to be read
        cancercol=collist['cancervar'][collist['cancervar'].notna()] #columns to be read in cancervar file
        cancervar= pd.read_csv(cancerloc, usecols=cancercol, sep='\t')
        
        vcfcol=collist['vcf_wo_art'][collist['vcf_wo_art'].notna()]
        vcfcol=[int(i) for i in vcfcol] #converting it into integers
        vcf= pd.read_csv(vcfloc, usecols=vcfcol, sep='\t')
        
        annocol=collist['multianno'][collist['multianno'].notna()]
        annovar= pd.read_csv(annoloc,usecols=annocol, sep='\t')
        
        # modifying vcf position values
        
        for i in range(len(vcf)):
            if len(vcf['REF'][i])>len(vcf['ALT'][i]):
                vcf['POS'][i]=vcf['POS'][i]+1
        
        print("VCF position values modified...")
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
        for i in range(31,59):
            merged_df[merged_df.columns[i]]=merged_df.columns[i]+ ":" + merged_df[merged_df.columns[i]]
        
        merged_df['intervar_inhouse']=merged_df[list(merged_df.columns[31:59])].apply(lambda x: ', '.join(x[x.notnull()]), axis = 1)
    
        ##Inserting columns 
        merged_df.insert(6, "IGV_link", value=None, allow_duplicates=False)
        merged_df.insert(7, "Mutant_allelic_burden_%", value=None, allow_duplicates=False)
        
        #add igv data in to the empty column
        merged_df['End'] =  merged_df['End'].replace('.', 0).fillna(0)
        merged_df['End'] = merged_df['End'].astype(int)
        merged_df['IGV_link'] = merged_df['CHROM'].astype(str) + [':'] + merged_df['POS'].astype(str) + ['-'] + merged_df['End'].astype(str)
        
        #add allele frequency data to empty column
        allele_freq=list(merged_df.columns[merged_df.columns.str.contains(':AF')])[0]
        merged_df[allele_freq] = merged_df[allele_freq].replace('.',0).fillna(0)
        merged_df['Mutant_allelic_burden_%'] = merged_df[allele_freq]*100
        merged_df = merged_df.round({'Mutant_allelic_burden_%' : 0})
        
       
        #function to split columns containing multiple gene names sep by ";"
        def splitDataFrameList(df,target_column,separator):
        
            def splitListToRows(row,row_accumulator,target_column,separator):
                split_row = row[target_column].split(separator)
                for s in split_row:
                   new_row = row.to_dict()
                   new_row[target_column] = s
                   row_accumulator.append(new_row)
            new_rows = []
            df.apply(splitListToRows,axis=1,args = (new_rows,target_column,separator))
            new_df = pd.DataFrame(new_rows)
            return new_df
        
        #spliting the 'Ref.Gene' column
        merged_df = splitDataFrameList(merged_df, 'Ref.Gene', ';')
        
        #performing a left merge with canonical data file
        merged_df = pd.merge(merged_df, canonical, how="left", on="Ref.Gene")
        
        #removing duplicates
        merged_df = merged_df.drop_duplicates()
        
    
        if sample_type=="DNA [Blood]":
            #splitting the AD column into two columns 
            alter_depth=list(merged_df.columns[merged_df.columns.str.contains(':AD')])[0]
            merged_df[alter_depth]= merged_df[alter_depth].fillna('.')
            merged_df[alter_depth]= merged_df[alter_depth].replace('.','.,.')
            merged_df[['Ref_Depth', 'Mutant_Depth']] = merged_df[alter_depth].str.split(",", expand=True)
        else:
            #splitting the AD column into two columns 
            alter_depth=list(merged_df.columns[merged_df.columns.str.contains(':AD')])[0]
            merged_df[['Ref_Depth', 'Mutant_Depth']] = merged_df[alter_depth].str.split(",", expand=True)

        merged_df=merged_df.dropna(axis='columns', how='all')
        print(f + " : merged")
            
        #re-arranging the index
        cols=list(merged_df.columns)
        colind= list(collist['reindex_wo_art'][collist['reindex_wo_art'].notna()])
        colindex=list( [cols[int(i)] for i in colind] )
                               
        final_df=merged_df[colindex]           
        tot_var=len(final_df)
        
        #writing merged file
        output_path= dirpath + "/FE_merged/" + f + '_merged_output.csv'        
        final_df.to_csv(output_path, index=False)
        
        ############## Filtration ##########
        
        #######$$$$$$ Filtering for Clinvar pathogenic variants 
        clinvar= final_df[final_df['clinvar: Clinvar '].str.contains('pathogen', case=False, regex=True)]
        
        ####### filtering Func.knownGene
        df= final_df[final_df['Func.ensGene'].str.contains('exonic|splicing', case=False, regex=True)]
        df= df[df['Func.ensGene'].str.contains('RNA')==False]
        afknowngene= len(df)   
        
        ##### filtering synonymous
        df= df[df['ExonicFunc.ensGene']!='synonymous SNV']
        df['ExonicFunc.ensGene']= [i.title().replace(" Snv", " SNV") for i in df['ExonicFunc.ensGene']]
        afsynony= len(df)  
        
        #####filtering pop freq
        
        popfreqs=['esp6500siv2_all','ExAC_ALL','ExAC_SAS','AF','AF_sas','1000g2015aug_all','1000g2015aug_SAS']
        
        print(f + " filtering in progress..")
        
        for p in popfreqs:
            df[p]=df[p].replace('.',0).fillna(0) 
            df[p]=  df[p].astype(float).round(4) #change 26-oct 12:45
            df=df[df[p]< 0.01] 
        
        afpop=len(df)
        
        ########## Removing Tier_IV
        df[' CancerVar: CancerVar and Evidence ']= [x.upper() for x in df[' CancerVar: CancerVar and Evidence ']]
        df=df[~df[' CancerVar: CancerVar and Evidence '].str.contains('BENIGN')]
        
        aft4=len(df)
        
        ######### Removing benign from intervar
         
        df['InterVar_automated']= [x.upper() for x in df['InterVar_automated']]
        df=df[~df['InterVar_automated'].str.contains('BENIGN')]    
        
        afben=len(df)
        
  
        df['CADD13_PHRED']=df['CADD13_PHRED'].replace('.',15).fillna(15)
        df['CADD13_PHRED']=[float(i) for i in list(df['CADD13_PHRED'])]
        df=df[df['CADD13_PHRED']>=15]
        
        afcad=len(df)
        
           
        ###### Gene filtering
        df['Ref.Gene']= [x.upper() for x in df['Ref.Gene']]
        df2=df[df['Ref.Gene'].str.contains('|'.join(testgenes))]
        df3= pd.DataFrame()
        for g in range(len(df2)):
            if ";" in df2['Ref.Gene'].iloc[g]:
                gene= df2['Ref.Gene'].iloc[g].split(";")[0]
            else:
                gene= df2['Ref.Gene'].iloc[g]
                
                if gene in testgenes:
                    df3=df3.append(df2.iloc[g])
            
        df3=df3[colindex] 
        afgen=len(df3)
       
        ##$$$$$ COMBINING clinvar variants and filtered variants together $$$$$###
        
        df3=df3.append(clinvar,sort=False)
        
        #modified 27-10-2021
        df3['ExonicFunc.ensGene'] = df3['ExonicFunc.ensGene'].str.upper()
        df3['InterVar_automated'] = df3['InterVar_automated'].str.upper()
        df3[' CancerVar: CancerVar and Evidence '] = df3[' CancerVar: CancerVar and Evidence '].str.upper()
        
        #redundant code for clinvar data
        for p in popfreqs:
            df3[p]=df3[p].replace('.',0).fillna(0) 
            df3[p]=  df3[p].astype(float).round(4)
        
        ##Generating the Genomic Alt column
        
        #Rows not containing Frameshift Deletion
        df_n= df3[~df3['ExonicFunc.ensGene'].str.contains('deletion|insertion')]
        df_n['POS_x'] =  df_n['POS_x'].replace('.', 0).fillna(0)
        df_n['POS_x'] = df_n['POS_x'].astype(int)
        df_n['Genomic Alteration'] = df_n['CHROM_x'].astype(str) + [':g.'] + df_n['POS_x'].astype(str) + df_n['REF_x'] + ['>'] + df_n['ALT_x']  
        
        #Rows containing Frameshift deletion
        df_d= df3[df3['ExonicFunc.ensGene'].str.contains('deletion|insertion')]
        df_d['End_x'] =  df_d['End_x'].replace('.', 0).fillna(0)
        df_d['End_x'] = df_d['End_x'].astype(int)
        df_d['POS_x'] =  df_d['POS_x'].replace('.', 0).fillna(0)
        df_d['POS_x'] = df_d['POS_x'].astype(int)
        df_d['Genomic Alteration'] = df_d['CHROM_x'].astype(str) + [':g.'] + df_d['POS_x'].astype(str) + "_" + df_d['End_x'].astype(str)
        
        #merging both dataframes
        df3 = pd.merge(df_n, df_d, how='outer')
        #changing coloumn
        col_list = list(df3.columns)
        col_list[-2], col_list[-1] = col_list[-1], col_list[-2]
        df3 = df3[col_list]
        #modifying the ['AAChange.ensGene'] column 
        
        aa=df3['AAChange.ensGene']
    
        to_replace={'A':'Ala','R':'Arg','N':'Asn','D':'Asp','B':'Asx','C':'Cys','E':'Glu','Q':'Gln','Z':'Glx','G':'Gly','H':'His','I':'Ile','L':'Leu','K':'Lys','M':'Met','F':'Phe','P':'Pro','S':'Ser','T':'Thr','W':'Trp','Y':'Tyr','V':'Val'}
    
        for a in aa:
          if 'ENS' in a:
            #splitting the list with , only if 'ENS' pattern is present- to avoid UNKNOWNS
            alist=a.split(',') #making a list with all the transcripts
            
            for al in alist: #running loop for changing each transcript
                    pattern = ":c.(.*?):p."
                    codon = re.search(pattern, al)
                    if codon is not None:
                        codon = re.search(pattern, al).group(1)
                    else:
                        codon=" "
                    #changing the codon nomenclature
                    if ('_' or 'del' or 'dup' or 'ins' or 'inv') in codon:
                        n_al=al #n_al where nothing is changed
                       
                    else:
                        ncodon=codon[1:len(codon)-1]+codon[0]+'>'+codon[len(codon)-1]
                        n_al=al.replace(codon, ncodon) #n_al with the replaced values
                    
                    #changing the protein nomenclature
                    if len(al.split(':p.'))>1:
                        prot=al.split(':p.')[1]
                    else:
                        prot=" "
                    for key, value in to_replace.items():
                        nprot = prot.translate(str.maketrans(to_replace))
                    
                    n_al=n_al.replace(prot, nprot)
                    
                    #making a lost of aachange
                    aa=list(map(lambda st: str.replace(st, al, n_al), aa))   
        
        #replacing the modified values in the original dataframe
        df3['AAChange.ensGene'] = aa  
        
        print("####### AAChange.ensGene column modified #######")
    
        df3=df3.dropna(axis='columns', how='all')
        df3=df3.astype(str)
        df3.drop_duplicates(subset=None, keep="first", inplace=True)
        
        ###Converting characters Cases in ExonicFunc.ensGene column###
        df3["ExonicFunc.ensGene"] = df3["ExonicFunc.ensGene"].str.capitalize()
        df3["ExonicFunc.ensGene"].replace("snv", "SNV", regex=True, inplace=True)
        df3["ExonicFunc.ensGene"].replace("deletion", "Deletion", regex=True, inplace=True) 
        df3["ExonicFunc.ensGene"].replace("insertion", "Insertion", regex=True, inplace=True) 
        ###Replacing if the last character of each cell is 'X' to 'Ter' in column AAChange.ensGene###
        df3['AAChange.ensGene'].replace("X$", "Ter", regex=True, inplace=True)
        
        df3['End_x'].replace("\.0", "", regex=True, inplace=True)  #varaible is object
        df3['CADD13_PHRED'].replace("\.0", "", regex=True, inplace=True)   
       
        df3['End_x']=df3['End_x'].astype(str).astype(int)  #varaible becomes int64 for ease in calculation
        for i in range(len(df3)):
            if (df3['ExonicFunc.ensGene'].iloc[i]=="Frameshift Insertion" or df3['ExonicFunc.ensGene'].iloc[i]=="Nonframeshift Insertion"):
                df3['End_x'].iloc[i]=df3['End_x'].iloc[i]+1
        df3['End_x'] = df3['End_x'].astype(str)
       
        df3.drop_duplicates(subset=None, keep="first", inplace=True)
        output_path= dirpath + "/FE_filtered/" + f + '_FENG.xlsx'  
        df3.to_excel(output_path, index=False)
        
        print(f + " :filtered")
        ###################################
        ### making filtered csv
        to_append= [f,tot_var,afknowngene,afsynony,afpop,aft4,afben,afcad,afgen]
        dflen=len(filtered_df)
        filtered_df.loc[dflen]=to_append
        print(to_append)  
        print( "###" + str(num+1) + " out of " + str(len(folders)) + " files done")
    
    filtered_df.to_csv(dirpath+"/"+"FE_filtered.csv")    
    
    print("#############################")
    print("############ DONE ###########")
    print("#############################")


############################################################_END FILTER_ENGINE ############################################################
