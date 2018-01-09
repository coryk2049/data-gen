#!/bin/bash
script_name=`basename $0`
if [ $# -ne 5 ]; then
    echo "Usage: ${script_name} <format_type> <process_date> <process_host> <division_id> <record_count>"
    echo "  <format_type>   = Output CSV format type (hb:Header,Body, kv:Key=Value)"
    echo "  <process_date>  = Processed date (e.g. 20170101)"
    echo "  <process_host>  = Hostname of EDR source system (e.g. ts1.edr-example.com)"
    echo "  <division_id>   = Division Id (e.g. B52, T13)"
    echo "  <record_count>  = Number of records per file"
    echo "Example:"
    echo "${script_name} hb 20170101 pcrf1.example.com B52 5000"
    exit 1
fi
format_type=$1
process_date=$2
process_host=$3
div_id=$4
record_count=$5
fr_date="${process_date} 00:00:00"
to_date="${process_date} 23:59:59"
fr_secs=$(date --date="${fr_date}" +%s)
to_secs=$(date --date="${to_date}" +%s)
#echo ">> Local Time (Eastern): From Date: ${fr_date} = ${fr_secs}, To Date: ${to_date} = ${to_secs}"
tz_offset=$[5 * 60 * 60]
fr_secs=$[${fr_secs} - ${tz_offset}]
to_secs=$[${to_secs} - ${tz_offset}]
#echo ">> GMT Time  (Adjusted): From Date: ${fr_date} = ${fr_secs}, To Date: ${to_date} = ${to_secs}"
output_script=create_pcrf_csv_${format_type}_${process_date}_${div_id}_${process_host}.sh
output_script_full=../output/${output_script}
rm -f ${output_script_full}
while [[ ${fr_secs} < ${to_secs} ]]; do
    date_start_secs=$(date -d "1970-01-01 ${fr_secs} sec" "+%Y/%m/%d %H:%M:%S")
    fr_secs=$[${fr_secs} + 14]
    date_end_secs=$(date -d "1970-01-01 ${fr_secs} sec" "+%Y/%m/%d %H:%M:%S")
    fr_secs=$[${fr_secs} + 1]
    # create 15 seconds interval in test data timeline
    echo "../bin/pcrf_csv_${format_type}.py -i ${process_host} -d ${div_id} -s '${date_start_secs}' -e '${date_end_secs}' -r ${record_count}" >> ${output_script_full}
done
chmod +x ${output_script_full}
#cd ../output; ./${output_script}; cd ../bin
exit 0
