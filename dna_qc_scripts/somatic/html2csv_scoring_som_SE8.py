# Importing the required modules
from bs4 import BeautifulSoup
import glob, os
import pandas as pd

# Storing the data into Pandas DataFrame
df = pd.DataFrame(columns = ['Sample Name', "Sequence_length", "Total_Sequences"], dtype=object)

print(df)
for file in glob.glob("*_fastqc.html"):
    
    with open(file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        htmltable = soup.find('table')
        rows=list()
        
        for row in htmltable.findAll("tr"):
            rows.append(row)
            
        sample_id = str(rows[1].findAll("td")[1])[4:-17]
        seq_length = int(str(rows[6].findAll("td")[1])[4:-5])
        seq_count = int(str(rows[4].findAll("td")[1])[4:-5])
        df.loc[len(df.index)] = [sample_id, seq_length, seq_count]
        
# Calculating the Total_size(GB)
df['Total_size'] = 2 * df['Sequence_length'] * df['Total_Sequences'].div(1e9)

#Assigning the scoring parameters
df['qual_Total_size(GB)'] = [0 if i <= 9 else 2 if i >= 12 else 1 for i in list(df['Total_size'])]

df.to_csv('multiqc.txt')

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
col_list = ["Sample Name","Percent duplicate aligned reads", "Unique base enrichment", "Mean target coverage depth", "Uniformity of coverage (Pct > 0.2*mean)"]
df = pd.read_csv("merged.csv", usecols=col_list)
print(df)

#Assigning the scoring parameters
df['qual_Percent duplicate aligned reads'] = [0 if i >= 56.242 else 2 if i <= 11.256 else 1 for i in list(df['Percent duplicate aligned reads'])]
df['qual_Unique base enrichment'] = [0 if i <= 46.786 else 2 if i >= 70.636 else 1 for i in list(df['Unique base enrichment'])]
df['qual_Mean target coverage depth'] = [0 if i <= 49.34 else 2 if i >= 169.4 else 1 for i in list(df['Mean target coverage depth'])]
df['qual_Uniformity of coverage (Pct > 0.2*mean)'] = [0 if i <=  81.562 else 2 if i >= 96.656 else 1 for i in list(df['Uniformity of coverage (Pct > 0.2*mean)'])]
print(df)
  
# reading and selecting specific cols from input csv files
QC_metrics = pd.read_csv('multiqc.txt')
Column_list = ["Sample Name", "Total_size","qual_Total_size(GB)"]
QC_metrics = pd.read_csv('multiqc.txt', usecols=Column_list)

#Merge required QC_parameters
df1 = pd.merge(df, QC_metrics, on='Sample Name')

#QC score of the samples
column_names = ['qual_Percent duplicate aligned reads', 'qual_Unique base enrichment', 'qual_Mean target coverage depth', 'qual_Uniformity of coverage (Pct > 0.2*mean)', 'qual_Total_size(GB)']
df1['QC_score']= df1[column_names].sum(axis=1)

#Assigning QC_status based on quality scores of each parameter
df1['QC_status'] = df1['qual_Percent duplicate aligned reads'] * df1['qual_Unique base enrichment'] * df1['qual_Mean target coverage depth'] * df1['qual_Uniformity of coverage (Pct > 0.2*mean)'] * df1['qual_Total_size(GB)']
df1['QC_status'] = df1['QC_status'].apply(lambda x: 'Fail' if x == 0 else 'Pass')

#Select specific columns for output
header = ["Sample Name", "Percent duplicate aligned reads","qual_Percent duplicate aligned reads", "Unique base enrichment", "qual_Unique base enrichment", "Mean target coverage depth", "qual_Mean target coverage depth", "Uniformity of coverage (Pct > 0.2*mean)", "qual_Uniformity of coverage (Pct > 0.2*mean)", "Total_size", "qual_Total_size(GB)","QC_score", "QC_status"]
df1.to_csv('output.csv', columns = header)

