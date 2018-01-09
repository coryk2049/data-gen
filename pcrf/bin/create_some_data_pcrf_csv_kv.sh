find ../output -name "*.csv" -type f -exec rm {} \;
echo "Started - `date`"
./create_pcrf_csv.sh kv 20170101 pcrf1.example.com B25 250
./create_pcrf_csv.sh kv 20170101 pcrf1.example.com B52 500
echo "   Done - `date`"
