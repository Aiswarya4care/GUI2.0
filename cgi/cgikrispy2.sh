export CGI_DATA={{cgi_data}}
export TRANSVAR_CFG=${CGI_DATA}/transvar.cfg
export TRANSVAR_DOWNLOAD_DIR=${CGI_DATA}/transvar

input="list.txt"
 
while IFS= read -r line
do
echo "Starting CGI analysis for  ${line}"
cgi -i ${line} -o ${line}_CGI

echo "Starting Comprssion of ${line}"
zip -r ${line}_CGI.zip ${line}_CGI

echo "Ending CGI analysis for ${line} and compressed the Results"
done < "$input"



echo "################## ALL CGI RESULTS GENERATED ########################"





