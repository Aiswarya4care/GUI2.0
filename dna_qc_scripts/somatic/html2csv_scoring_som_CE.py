# Importing the required modules
from bs4 import BeautifulSoup
import glob, os
import pandas as pd
import re

location={{location}}

#set the working directory as QC folder
os.chdir(location)

# Storing the data into Pandas DataFrame
df = pd.DataFrame(columns = ['Sample Name', "Sequence_length", "Total_Sequences"], dtype=object)

for file in glob.glob(location + "/QC/CE/" +"*.html"):
    
    with open(file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        htmltable = soup.find('table')
        rows=list()
        
        for row in htmltable.findAll("tr"):
            rows.append(row)
            
        sample_id = str(rows[1].findAll("td")[1]).split('_')[0].split('>')[1]
        seq_length = int(re.findall(r'\d+', str(rows[6].findAll("td")[1]))[0])
        seq_count = int(re.findall(r'\d+', str(rows[4].findAll("td")[1]))[0])
        df.loc[len(df.index)] = [sample_id, seq_length, seq_count]
        
# Calculating the Total_size(GB)
df['Total_size'] = 2 * df['Sequence_length'] * df['Total_Sequences'].div(1e9)

#Assigning the scoring parameters
df['qual_Total_size(GB)'] = [0 if i <= 3 else 2 if i >= 4 else 1 for i in list(df['Total_size'])]

df.to_csv(location+'/QC/CE/'+ 'multiqc.txt')

#Export csv files from basespace
#Create a folder and save the csv files
#python script for scoring parameters

#merge all the csv files
csvfiles = glob.glob(os.path.join(location + '/QC/CE/' , "metrics*.csv"))
mergedfile=pd.concat(map(pd.read_csv, csvfiles), ignore_index=True)

mergedfile.to_csv(location+'/QC/CE/'+ 'merged.csv')

#extract specific columns from csv
col_list = ["Sample Name","Percent duplicate aligned reads", "Percent Target coverage at 50X", "Mean target coverage depth", "Uniformity of coverage (Pct > 0.2*mean)"]
df = pd.read_csv(location + "/QC/CE/merged.csv", usecols=col_list)

#Assigning the scoring parameters
df['qual_Percent duplicate aligned reads'] = [0 if i >= 70 else 2 if i <= 40 else 1 for i in list(df['Percent duplicate aligned reads'])]
df['qual_Percent Target coverage at 50X'] = [0 if i <= 60 else 2 if i >= 90 else 1 for i in list(df['Percent Target coverage at 50X'])]
df['qual_Mean target coverage depth'] = [0 if i <= 85 else 2 if i >= 100 else 1 for i in list(df['Mean target coverage depth'])]
df['qual_Uniformity of coverage (Pct > 0.2*mean)'] = [0 if i <=  80 else 2 if i >= 90 else 1 for i in list(df['Uniformity of coverage (Pct > 0.2*mean)'])]
  
# reading and selecting specific cols from input csv files
QC_metrics = pd.read_csv(location+ '/QC/CE/multiqc.txt')
Column_list = ["Sample Name", "Total_size","qual_Total_size(GB)"]
QC_metrics = pd.read_csv(location+'/QC/CE/multiqc.txt', usecols=Column_list)

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
df1.to_csv(location+'/QC/CE/output.csv', columns = header)


