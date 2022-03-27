cd {{location}}
for i in *_R1.fastq.gz
do
   SAMPLE=$(echo ${i} | sed "s/_R1\.fastq\.gz//") 
   echo ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz
   cutadapt -j 30 -m 35 -a {{adapter}} -A {{adapter}} -o ${SAMPLE}_S1_L001_R1_001.fastq.gz -p ${SAMPLE}_S1_L001_R2_001.fastq.gz ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz >{{location}}/cutadaptlog/${SAMPLE}_cutadaptlog.txt
done
sleep 2m
bs upload dataset --project={{pid}} *R1_001.fastq.gz *R2_001.fastq.gz
echo "############ FQ and CA completed ###########"
