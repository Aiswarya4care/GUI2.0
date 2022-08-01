cd {{location}}

bs upload dataset --project={{pid}} *R1_001.fastq.gz *R2_001.fastq.gz
sleep 2m
samples=({{samplenames}}) #list of samples

for i in ${samples[@]};  do
echo $i;
bsid=`bs get biosample -n $i â€“terse | grep "Id" | head -1 | grep -Eo '[0-9]{1,}'`;
bsids+=($bsid)
done
printf -v joined '%s,' "${bsids[@]}"
bsids=${joined%,}
echo $bsids

{{bscmd}}


echo "########################"
echo "Dragen Launched"
echo "########################"
perl {{fastqc}} *.gz
echo "########################"
echo "FastQC completed"
echo "########################"

