$path  = $ARGV[0]; $bed_file = $ARGV[1]; $output = $ARGV[2]; 
open (O, ">$output/config_CNV.txt");
print O "[general]

chrLenFile = /home/ubuntu/Programs/files_for_control_freec/fai_file/my_genome.fa.fai
chrFiles = /home/ubuntu/Programs/files_for_control_freec/chromFa/
window = 0
ploidy = 2
intercept=1
minMappabilityPerWindow = 0.7
outputDir = $output
sex=XY
breakPointType=2
degree=3
coefficientOfVariation = 0.05
breakPointThreshold = 0.6
maxThreads = 10
sambamba = /home/ubuntu/sambamba_installed/sambamba_0_8_2
SambambaThreads = 10


noisyData = TRUE
printNA=FALSE

[sample]

mateFile = $path
inputFormat = BAM
mateOrientation = FR

[target]

captureRegions = $bed_file";
