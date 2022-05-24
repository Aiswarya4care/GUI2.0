cd /home/ubuntu/Patient_Sample_Processing/Somatic_DNA_SE8

#Renamed samples should be suffix _S1_L001_R1_001.fastq.gz & _S1_L001_R2_001.fastq.gz e.g. VDAA-F-SE8-raw-S44_S1_L001_R1_001.fastq.gz VDAA-F-SE8-raw-S44_S1_L001_R2_001.fastq.gz
/home/ubuntu/bs/bs upload dataset --project=346604264 *R1_001.fastq.gz *R2_001.fastq.gz
samples=(VDAA-F-SE8-raw-S44) #list of samples

sleep 2m

for i in ${samples[@]};  do
echo $i;
bsid=`/home/ubuntu/bs/bs get biosample -n $i â€“terse | grep "Id" | head -1 | grep -Eo '[0-9]{1,}'`;
bsids+=($bsid)
done
printf -v joined '%s,' "${bsids[@]}"
bsids=${joined%,}
echo $bsids


/home/ubuntu/bs/bs launch application -n "DRAGEN Enrichment" --app-version 3.9.5 -o project-id:346604264 -o app-session-name:2nd_May_batch_Somatic_DNA_SE8  -l 2nd_May_batch_Somatic_DNA_SE8  -o vc-type:1 -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:23683257154 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o af-filtering:1  -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o sq-filtering:1 -o tmb:1 -o vc-hotspot:26309592242 -o baseline-noise-bed:25849773923 -o vcf-site-filter:1 -o cnv_checkbox:1 -o cnv_ref:1 -o cnv_segmentation_mode:cbs -o cnv-filter-qual:50.0 -o cnv-baseline-id:25791243964,25791291016,25791291033,25791291050,25791406163,25791440084,25791528878,25791528895,25791582119,25791582931,25791595964,25791595981,25791598767,25791637964,25791670919,25791679146,25791679164,25791681916,25791681933 -o cnv_gcbias_checkbox:1 -o hla:1 -o commandline-disclaimer:true -o arbitrary:"--read-trimmers:adapter --trim-adapter-read1" -o additional-file:25600057590 -o automation-sex:unkown

echo "########################"
echo "Dragen Launched"
echo "########################"
perl /home/basecare/Programs/fastqc_v0.11.9/FastQC/fastqc *.gz
echo "########################"
echo "FastQC completed"
echo "########################"

