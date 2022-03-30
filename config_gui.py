############# Project ID for dragen ###########
proj_somatic_dna= '175429254'
proj_germline= '166558401'
proj_somatic_rna= '148206064'

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

############ Developer Options ###############
default_files=['ca_fq_dragen.sh','ca_fq.sh','panel','cutadaptlog.txt','FQlog.txt','MSI','CNV','cutadaptlog', 'FE_merged','FE_filtered','FE_filtered.csv','tmbmerged','tmbfiltered','tmb_filtered.csv','sample_coverage'] #pre-existing file names to be removed from the sample name list




