################### GUI Path #################

GUIpath='/home/ash/Documents/GitHub/GUI2.0'

############# Project ID for dragen ###########
projectid={
    'DNA [FFPE, FF]':'175429254',
    'DNA [cf]':'175429254',
    'DNA [Blood]':'166558401',
    'RNA':'148206064'
}

############# Path of tools/software ###########
annotation_db= '/home/basecare/Programs/Annotation_db'
simplifyvcf='/home/basecare/Programs/VCF-Simplify-master/VcfSimplify.py'
fastqc= '/home/basecare/Programs/fastqc_v0.11.9/FastQC/fastqc'
cgi_data='/home/basecare/cgi_commercial1/datasets'
#MSI
msisensor= '/home/basecare/Programs/msisensor2/msisensor2'
msi_microlist= '/home/basecare/Programs/MSI_Mirco_List/micro.list'

#CNV
chrLenFile = '/home/basecare/Programs/files_for_control_freec/fai_file/my_genome.fa.fai'
chrFiles = '/home/basecare/Programs/files_for_control_freec/chromFa/'
sambamba = '/usr/bin/sambamba'
controlfreec= '/home/basecare/Programs/FREEC-11.6/src/freec'
bedtools= '/home/basecare/Programs/./bedtools.static.binary'

#FusionInspector

############# Bed file ID for dragen #################
dra_bed_ids= {

'Illumina_Exome_TargetedRegions_v1.2.hg19.bed':'27352929868',
'Indiegene_Target_2109PD006-V1_4BaseCare_1K_DNA_GRCh37.bed':'25985869859',
'Indiegene_Target_2109PD008-V1_4BaseCare_RNA_Fusion_GRCh37.bed':'25985863705',
'Roche_hg19.bed':'20977118310',
'SureSelectV7_covered.bed':'20024037150',
'SureSelectXT_V8_Covered.bed':'23683257154'

}

############# Panel size for TMB calculation #################
tmbpanelsize= {

'Illumina_Exome_TargetedRegions_v1.2.hg19.bed':0,
'Indiegene_Target_2109PD006-V1_4BaseCare_1K_DNA_GRCh37.bed':4.4,
'Indiegene_Target_2109PD008-V1_4BaseCare_RNA_Fusion_GRCh37.bed':0,
'Roche_hg19.bed':0,
'SureSelectV7_covered.bed':0,
'SureSelectXT_V8_Covered.bed':41.48

}

########### test name and panel bed prefix #############
testprefix={
'TarGT_Absolute' : 'TA_',
'TarGT_Core' : 'TC_',
'TarGT_Indiegene' : 'TI_',
'TarGT_Focus' : 'TF_',
'TarGT_Absolute_Germline' : 'TA_Germline_',
'Germline_Plus' : 'Gplus_',
'Germline_++' : 'T_Germlineplusplus_',
'HRR' : 'T_HRR_',
'TarGT_First':'T1_'
}

capkitsuffix={
'SureSelectV7_covered.bed' : 'SSE.bed',
'SureSelectXT_V8_Covered.bed' : 'SE8.bed',
'Indiegene_Target_2109PD006-V1_4BaseCare_1K_DNA_GRCh37.bed' : 'Indie.bed',
'Illumina_Exome_TargetedRegions_v1.2.hg19.bed' : 'Illumina.bed',
'Roche_hg19.bed' : 'Roche.bed'
}
############ Developer Options ###############
default_files=['annotation','ca','panel', 'dragen39.sh','cutadaptlog.txt','FQlog.txt','MSI','CNV','run_cnv.sh','cutadaptlog', 'QC','FE', 'FE_filtered','FE_merged','tmbmerged','tmbfiltered','tmb','sample','config.pl','annotation'] #pre-existing file names to be removed from the sample name list




