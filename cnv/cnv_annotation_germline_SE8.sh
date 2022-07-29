cd {{location}}
input="list.txt"
while IFS= read -r line
do
echo "Starting ${line}"
mkdir ${line}
#preparing config file
echo "##########Starting preparing config file#################"
perl cnv_config_germline.pl {{projectdir}}/AppResults/${line}/Files/${line}.bam {{GUIpath}}/bed_files/cnv_bed_files/cnv_capturing_bedfiles/{{modified_capt_bed}}  ${line}
echo "##########Ending preparing config file#################"
#run CNV
echo "##########Starting CNV Control Freec#################"
{{controlfreec}} -conf ${line}/config_CNV.txt
echo "##########Ending CNV Control Freec#################"
#Annotating file
echo "##########Starting annotation#################"
{{bedtools}} intersect -a ${line}/${line}.bam_CNVs -b /home/ubuntu/Programs/files_for_control_freec/bed_file_CNV/indiegene_whole-gene.bed -loj | sort -V | awk -F"\t" '{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$9}' | awk -vOFS="\t" '$1=$1; BEGIN { str="Chromosome Start End Predicted_copy_number Type_of_alteration Gene"; split(str,arr," "); for(i in arr) printf("%s\t", arr[i]);print}' | awk '$6 != "."' > ./${line}"_Indiegene_cnv_output.txt"

{{bedtools}} intersect -a ${line}/${line}.bam_CNVs -b {{GUIpath}}/bed_files/cnv_bed_files/cnv_capturing_bedfiles/cnv_36_genes.bed -loj | sort -V | awk -F"\t" '{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$9}' | awk -vOFS="\t" '$1=$1; BEGIN { str="Chromosome Start End Predicted_copy_number Type_of_alteration Gene"; split(str,arr," "); for(i in arr) printf("%s\t", arr[i]);print}' | awk '$6 != "."' > ./${line}"_cnv_output.txt"

echo "##########Ending annotation#################"
done < "$input"
echo "################## ALL FILES ARE DONE ###########################"
