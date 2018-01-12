
DROP TABLE IF EXISTS BL_EDR PURGE;

CREATE EXTERNAL TABLE BL_EDR (
	PROCESS_ID string,
	COMPONENT_ID string,
	TRANSACTION_ID string,
	SESSION_ID string,
	EVENT_TIMESTAMP string,
	EVENT_TYPE string,
	DIVISION_ID string,
	GROUP_ID string,
	SUBSCRIBER_ID string,
	SUBSCRIBER_TYPE string,
	DEVICE_ID string,
	PLAN_ID string,
	NOTIFICATION_TYPE string,
	NOTIFICATION_ADDRESS string,
	USAGE  string,
	CHARGE_AMOUNT string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://pcrf1/edr/';

DROP TABLE IF EXISTS BL_ULOG PURGE;
CREATE EXTERNAL TABLE BL_ULOG (
	PROCESS_ID string,
	COMPONENT_ID string,
	THREAD_ID string,
	TRANSACTION_ID string,
	LOG_LEVEL string,
	MESSAGE_ID string,
	MESSAGE_TEXT string,
	CREATION_TIMESTAMP string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://pcrf1/ulog/';

DROP TABLE IF EXISTS BL_STATS PURGE;
CREATE EXTERNAL TABLE BL_STATS (
	PROCESS_ID string,
	COMPONENT_ID string,
	TRANSACTION_ID string,
	STATISTIC_NAME string,
	STATISTIC_DURATION string,
	CREATION_TIMESTAMP string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://pcrf1/ulog/';
