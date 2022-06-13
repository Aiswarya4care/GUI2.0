#Export csv files from basespace
#Create a folder and save the csv files
#python script for scoring parameters

#importing important libraries/packages
import pandas as pd
import os
import glob

#set the working directory
path = os.getcwd()

#merge the csv files
cmd = "awk 'FNR==1 && NR!=1{next;}{print}'  *.csv > merged.csv"
os.system(cmd)

#extract specific columns from csv
col_list = ["Sample Name","Percent duplicate aligned reads", "Percent Target coverage at 50X", "Mean target coverage depth", "Uniformity of coverage (Pct > 0.2*mean)"]
df = pd.read_csv("merged.csv", usecols=col_list)
print(df)

#Assigning the scoring parameters
df['qual_Percent duplicate aligned reads'] = [0 if i >= 70 else 2 if i <= 40 else 1 for i in list(df['Percent duplicate aligned reads'])]
df['qual_Percent Target coverage at 50X'] = [0 if i <= 60 else 2 if i >= 90 else 1 for i in list(df['Percent Target coverage at 50X'])]
df['qual_Mean target coverage depth'] = [0 if i <= 85 else 2 if i >= 100 else 1 for i in list(df['Mean target coverage depth'])]
df['qual_Uniformity of coverage (Pct > 0.2*mean)'] = [0 if i <=  80 else 2 if i >= 90 else 1 for i in list(df['Uniformity of coverage (Pct > 0.2*mean)'])]
print(df)
  
# reading and selecting specific cols from input csv files
QC_metrics = pd.read_csv('multiqc.txt')
Column_list = ["Sample Name", "Total_size","qual_Total_size(GB)"]
QC_metrics = pd.read_csv('multiqc.txt', usecols=Column_list)

#Merge required QC_parameters
df1 = pd.merge(df, QC_metrics, on='Sample Name')

#QC score of the samples
column_names = ['qual_Percent duplicate aligned reads', 'qual_Percent Target coverage at 50X', 'qual_Mean target coverage depth', 'qual_Uniformity of coverage (Pct > 0.2*mean)', 'qual_Total_size(GB)']
df1['QC_score']= df1[column_names].sum(axis=1)

#Assigning QC_status based on quality scores of each parameter
df1['QC_status'] = df1['qual_Percent duplicate aligned reads'] * df1['qual_Percent Target coverage at 50X'] * df1['qual_Mean target coverage depth'] * df1['qual_Uniformity of coverage (Pct > 0.2*mean)'] * df1['qual_Total_size(GB)']
df1['QC_status'] = df1['QC_status'].apply(lambda x: 'Fail' if x == 0 else 'Pass')

#Select specific columns for output
header = ["Sample Name", "Percent duplicate aligned reads","qual_Percent duplicate aligned reads", "Percent Target coverage at 50X", "qual_Percent Target coverage at 50X", "Mean target coverage depth", "qual_Mean target coverage depth", "Uniformity of coverage (Pct > 0.2*mean)", "qual_Uniformity of coverage (Pct > 0.2*mean)", "Total_size", "qual_Total_size(GB)","QC_score", "QC_status"]
df1.to_csv('output.csv', columns = header)

