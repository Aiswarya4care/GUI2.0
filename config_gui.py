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
annotation_spk= '/home/basecare/Annotation_SPK'
simplifyvcf='/home/basecare/Programs/VCF-Simplify-master/VcfSimplify.py'
fastqc= '/home/ubuntu/Programs/fastqc_v0.11.9/FastQC/fastqc'
cgi_data='/home/basecare/cgi_commercial1/datasets'
#MSI
msisensor= '/home/ubuntu/Programs/msisensor2/msisensor2'
msi_microlist= '/home/ubuntu/Programs/MSI_Mirco_List/micro.list'

#CNV
chrLenFile = '/home/ubuntu/Programs/files_for_control_freec/fai_file/my_genome.fa.fai'
chrFiles = '/home/ubuntu/Programs/files_for_control_freec/chromFa/'
sambamba = '/usr/bin/sambamba'
controlfreec= '/home/ubuntu/Programs/FREEC-11.6/src/freec'
bedtools= '/home/ubuntu/Programs/./bedtools.static.binary intersect'

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

########### test name and panel bed prefix #############

########### capturing kit and panel bed prefix/suffix ###########
testprefix={
'TarGT_Absolute' : '_TA_',
'TarGT_Core' : '_TC_',
'TarGT_Indigene' : '_TI_',
'TarGT_Focus' : '_TF_',
'TarGT_Absolute_Germline' : '_TA_Germline_',
'Germline_Plus' : 'T_Germlineplus-',
'Germline_++' : 'T_Germlineplusplus-',
'HRR' : '_T_HRR_',
'TarGT_First':'_T1_'
}

capkitsuffix={
'SureSelectV7_covered.bed' : 'SSE.bed',
'sureselectxt_v8_covered.bed' : 'SE8.bed',
'Indiegene_Target_2109PD006-V1_4BaseCare_1K_DNA_GRCh37_sorted.bed' : 'Indie.bed',
'Illumina_Exome_TargetedRegions_v1.2.hg19.bed' : 'Illumina.bed',
'Roche_hg19.bed' : 'Roche.bed'
}

############ Developer Options ###############
default_files=['ca','panel','cutadaptlog.txt','FQlog.txt','MSI','CNV','cutadaptlog', 'FE','tmbmerged','tmbfiltered','tmb','sample','config.pl','annotation'] #pre-existing file names to be removed from the sample name list




