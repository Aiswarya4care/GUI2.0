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


# In[ ]:





# In[ ]:





# In[ ]:




