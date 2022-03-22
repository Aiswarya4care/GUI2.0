input="list.txt"
while IFS= read -r line
do
mkdir ${line}
echo "Starting ${line}"
#copying.hard-filtered.vcf from basespace and unzipping
echo "##########Starting copying.hard-filtered.vcf from basespace and unzipping#################"
cp {{projectdir}}/AppResults/${line}/Files/${line}.hard-filtered.vcf.gz {{annotation_spk}}
gunzip ${line}.hard-filtered.vcf.gz
echo "##########Ending copying.hard-filtered.vcf from basespace and unzipping#################"

#finding depth
echo "##########Starting finding depth#################"
bedtools bamtobed -i {{projectdir}}/AppResults/${line}/Files/${line}.bam | bedtools coverage -header -a ${line}.hard-filtered.vcf -b - | sed '/^##/d' > ${line}/${line}.tsv
##modifying the vcf with depth(field)
awk 'NR==1{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9"\t"$10"\t"$11"Overlaps_from_BAM"$12 ;next}{print}' ${line}/${line}.tsv > ${line}/${line}_mod.tsv
echo "##########Ending finding depth#################"

#vcf to table
echo "##########Starting.hard-filtered.vcf conversion to tab#################"
python3 {{simplifyvcf}} SimplifyVCF -toType table -inVCF "${line}.hard-filtered.vcf" -outFile "${line}/${line}.tab"

##merging the tab file and tsv file 
paste ${line}/${line}.tab ${line}/${line}_mod.tsv | cut -f 1-24,35 > ${line}/${line}_final.tab

echo "##########Ending.hard-filtered.vcf conversion to tab#################"
#annovar
echo "##########Starting annovar annotation#################"
perl {{annotation_db}}/convert2annovar.pl -format vcf4old "${line}.hard-filtered.vcf" > "${line}/${line}.avinput"
perl {{annotation_db}}/Annotation_db/table_annovar.pl "${line}/${line}.avinput" {{annotation_db}}/humandb/ -buildver hg19 -out "${line}/${line}_out" -remove -protocol ensGene,avsnp150,clinvar_20190305,intervar_20170202,intervar_20180118,esp6500siv2_all,exac03,gnomad211_exome,1000g2015aug_all,1000g2015aug_SAS,cadd13gt20,dbnsfp35a,dbscsnv11,dbnsfp31a_interpro -operation g,f,f,f,f,f,f,f,f,f,f,f,f,f -nastring .
echo "##########Ending annovar annotation#################"
#preparing config file
echo "##########Starting cancervar annotation#################"
perl {{annotation_spk}}/config.pl ${line}/${line}
#running cancervar
python3 {{annotation_db}}/CancerVar.py -c config.ini
echo "##########Ending cancervar annotation#################"
rm config.ini
done < "$input"
echo "################## ALL FILES ARE DONE ###########################"

