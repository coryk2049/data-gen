# Dummy PCRF Data Generator
A simple Python 2.7 implementation of dummy PCRF EDR, log, and statistic data generator with microsecond interval support (i.e. `"%Y/%m/%d %H:%M:%S.%f"`) in CSV file format.

## Main Script Usage
```shell
neo@taylor:~/pcrf/bin$ ./pcrf_csv_hb.py

Usage: pcrf_csv_hb.py [switches] [argument]
  -i, --system_id
        System Id (e.g. pcrf1.example.com)
  -d, --division_id
        Division Id (e.g. B52)
  -s, --start_datetime
        Start datetime (e.g. '2017/01/01 00:00:00')
  -e, --end_datetime
        End datetime   (e.g. '2017/01/01 00:00:15')
  -r, --record_count
        Record count (e.g. 5000)
Example:
  pcrf_csv_hb.py -i pcrf1.example.com -d B52 -s '2017/01/01 00:00:00' -e '2017/01/01 00:00:15' -r 5000
```
Ensure that post checkout all scripts in `~/pcrf/bin` are Unix executable (e.g. `chmod +x *.sh *.py`)

## Execute Example Test Script
Example test script to generate dummy PCRF data with 15 second intervals.
```shell
neo@taylor:~/pcrf/bin$ ./create_some_data_pcrf_csv_hb.sh
```
This script is simply a wrapper for `~/pcrf/bin/create_pcrf_csv.sh` which in turn invokes `pcrf_csv_hb.py`. 

## Output Folder Artifacts
Post execution of the above example test script, two new scripts should get created in `~/pcrf/output` folder that must be manually executed to finally generate the dummy data CSV files for you.

Example Observation:
```shell
neo@taylor:~/pcrf/output$ ls -l
total 960
-rwxrwxr-x 1 neo neo 616320 Jan  1 17:14 create_pcrf_csv_hb_20170101_B25_pcrf1.example.com.sh
-rwxrwxr-x 1 neo neo  17441 Jan  1 17:14 create_pcrf_csv_hb_20170101_B52_pcrf1.example.com.sh
-rw-rw-r-- 1 neo neo  53430 Jan  1 18:15 pcrf1.example.com_edr_B25_20170101000000_20170101000014.csv
-rw-rw-r-- 1 neo neo 113713 Jan  1 18:15 pcrf1.example.com_stats_B25_20170101000000_20170101000014.csv
-rw-rw-r-- 1 neo neo 169240 Jan  1 18:15 pcrf1.example.com_ulog_B25_20170101000000_20170101000014.csv
[..]
```
