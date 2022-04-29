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

#MSI
msisensor= '/home/ubuntu/Programs/msisensor2/msisensor2'
msi_microlist= '/home/ubuntu/Programs/MSI_Mirco_List/micro.list'

#CNV
chrLenFile = '/home/ubuntu/Programs/files_for_control_freec/fai_file/my_genome.fa.fai'
chrFiles = '/home/ubuntu/Programs/files_for_control_freec/chromFa/'
sambamba = '/usr/bin/sambamba'
controlfreec= '/home/ubuntu/Programs/FREEC-11.6/src/freec'
bedtools= '/home/ubuntu/Programs/./bedtools.static.binary intersect'

############# Bed file ID for dragen #################
dra_bed_ids= {
'Illumina':'Illumina',
'roche_hg19_whole.bed':'20977118310',
'truseq_exome_targetedregions_v1.2.bed':'18815858077',
'sureselectv7_covered.bed':'20024037150',
'sureselectxt_v8_covered.bed':'23683257154',
'ce_indiegene_target_1K_DNA_GRCh37.bed':'25985869859',
'ce_indiegene_target_RNA_Fusion_GRCh37.bed':'25985863705'

}

########### test name and panel bed prefix #############

########### capturing kit and panel bed prefix/suffix ###########
testprefix={
    'TarGT_Absolute' : 'T_Absolute-',
'TarGT_Core' : 'T_Core-',
'TarGT_Indigene' : 'T_Indie-',
'TarGT_Focus' : 'T_Focus-',
'TarGT_Absolute_Germline' : 'T_Absolute-',
'Germline_Plus' : 'T_Germlineplus-',
'Germline_++' : 'T_Germlineplusplus-',
'HRR' : 'T_HRR-'
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




