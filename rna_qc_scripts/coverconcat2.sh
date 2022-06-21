cd {{location}}
tail -n +1 *csv | grep "==" > samples.txt
tail -n +1 *csv | grep "Average alignment coverage over" > values.txt
paste samples.txt values.txt > coverage.txt
sed -i 's/.qc-coverage-region-1_overall_mean_cov.csv <==//g;s/,/\t/;s/==> //g' coverage.txt
cut -f 1,3 coverage.txt > Target_coverage.txt
sed -i '1i Sample\tTargetCoverage' Target_coverage.txt
