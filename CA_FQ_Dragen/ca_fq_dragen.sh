cd {{location}}
for i in *_R1.fastq.gz
do
   SAMPLE=$(echo ${i} | sed "s/_R1\.fastq\.gz//") 
   echo ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz
   cutadapt -j 30 -m 35 -a {{adapter}} -A {{adapter}} -o ${SAMPLE}_S1_L001_R1_001.fastq.gz -p ${SAMPLE}_S1_L001_R2_001.fastq.gz ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz >{{location}}/cutadaptlog/${SAMPLE}_cutadaptlog.txt
done
bs upload dataset --project={{pid}} *R1_001.fastq.gz *R2_001.fastq.gz
samples=({{samplenames}})
for i in ${samples[@]};  do
echo $i;
bsid=`bs get biosample -n $i –terse | grep "Id" | head -1 | grep -Eo '[0-9]{1,}'`;
bsids+=($bsid)
done
printf -v joined '%s,' "${bsids[@]}"
bsids=${joined%,}
echo $bsids
bs launch application -n "DRAGEN Enrichment" --app-version 3.6.3 -o app-session-name:123123 -l 123123 -o project-id:175429254 -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:Illumina_Exome_TargetedRegions_v1.2 -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o commandline-disclaimer:true
echo "########################"
echo "Dragen Launched"
echo "########################"
perl {{fastqc}} *.gz
echo "########################"
echo "FastQC completed"
echo "########################"
