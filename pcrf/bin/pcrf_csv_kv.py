#!/usr/bin/env python

import datetime
import time
import random
import uuid
import getopt
import sys
import profile

USAGE_INFO = """
Usage: pcrf_csv_kv.py [switches] [argument]
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
  pcrf_csv_kv.py -i pcrf1.example.com -d B52 -s '2017/01/01 00:00:00' -e '2017/01/01 00:00:15' -r 5000
"""

"""
    Class for generating fake PCRF EDR, Logging, Performance Statistics files
"""
class pcrf_csv_kv(object):
    # General
    DT_FORMAT = "%Y/%m/%d %H:%M:%S.%f"
    PROCESS_LIST = [1,1,1,1,1,2,2]
    COMPONENT_LIST = [1,1,1,1,1,1,2,2,2,2,3,3,3,4,4,5]
    THREAD_LIST = range(1,100)
    # Log Levels
    LOG_LEVEL_BIAS = [0,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4]
    # Statistics
    XYZ_LATENCY_LIMIT = 5
    STATISTIC_LIST = range(1,100)
    MAX_STATISTIC_LATENCY = 2.0
    # EDR
    EVENT_TYPE = "FAIR_USAGE_POLICY"
    NOTIFICATION_BIAS = [0,0,0,0,1]
    SUBSCRIBER_TYPE_BIAS = [0,0,0,0,0,0,0,0,1,1,2,3]
    GROUP_BIAS = [0,0,0,0,0,0,0,0,0,1]
    REG_PLAN_BIAS = [0,0,0,0,0,1,1,2]
    BUS_PLAN_BIAS = [0,0,0,0,0,0,1,2]
    USAGE_COUNTER_LIST_1 = range(1048576,1048576* 101,1048576)
    USAGE_COUNTER_LIST_2 = range(1048576,1048576* 501,1048576)
    USAGE_COUNTER_LIST_3 = range(1048576,1048576*1001,1048576)
    CHARGE_AMOUNT_LIST_1 = range(10,10* 101,10)
    CHARGE_AMOUNT_LIST_2 = range(10,10* 501,10)
    CHARGE_AMOUNT_LIST_3 = range(10,10*1001,10)

    def __init__(self,system_id,div_id,dt_start,dt_stop):
        dt_range_start = datetime.datetime.strptime(dt_start + '.000000', self.DT_FORMAT)
        dt_range_stop  = datetime.datetime.strptime(dt_stop  + '.000000', self.DT_FORMAT)
        ts_range_start = time.mktime(dt_range_start.timetuple()) + dt_range_start.microsecond / 1E6
        ts_range_stop  = time.mktime(dt_range_stop.timetuple())  + dt_range_stop.microsecond / 1E6
        self.system_id = system_id
        self.div_id = div_id
        self.ts_range_start = ts_range_start
        self.ts_range_stop  = ts_range_stop
        self.process_name = None
        self.component_name = None
        self.thread_id = None
        self.transaction_id = None
        self.session_id = None
        self.event_type = self.EVENT_TYPE
        self.event_ts = None
        self.ulog_filename = "{}_ulog_{}_{}_{}.csv".format(self.system_id, \
            self.div_id,flat_dt(dt_start),flat_dt(dt_stop))
        self.stats_filename = "{}_stats_{}_{}_{}.csv".format(self.system_id, \
            self.div_id,flat_dt(dt_start),flat_dt(dt_stop))
        self.edr_filename = "{}_edr_{}_{}_{}.csv".format(self.system_id, \
            self.div_id,flat_dt(dt_start),flat_dt(dt_stop))

    global flat_dt
    def flat_dt(dt):
        for ch in ['/',':',' ']:
            if ch in dt:
                dt = dt.replace(ch,'')
        return dt

    global get_ts
    def get_ts(self):
        ts = repr(random.uniform(self.ts_range_start,self.ts_range_stop))
        if len(str(ts)) == 17:
            return ts
        return get_ts(self)

    def core_init(self):
        ts = get_ts(self);
        self.process_name = 'PROCESS_' + str(random.choice(self.PROCESS_LIST))
        self.component_name = 'COMPONENT_' + str(random.choice(self.COMPONENT_LIST))
        thread_num = random.choice(self.THREAD_LIST)
        self.thread_id = str(thread_num).rjust(2,'0')
        self.transaction_id = ts.replace('.','') + '.' + self.thread_id
        self.session_id = 'Gx.' + str(int(ts.replace('.','')) + thread_num)
        self.event_ts = datetime.datetime.fromtimestamp(float(ts)).strftime(self.DT_FORMAT)

    def ulog_body(self,fh):
        log_level_types = ['FATAL','ERROR','WARN','INFO','DEBUG_X']
        log_level_idx = random.choice(self.LOG_LEVEL_BIAS)
        log_level = log_level_types[log_level_idx]
        msg_rand = str(random.choice(self.STATISTIC_LIST)).rjust(3,'0')
        message_id = log_level + "_Message_Id_XYZ_" + self.thread_id + msg_rand
        message_text = log_level + "_Message_Text_XYZ_" + self.thread_id + msg_rand
        fh.write("PROCESS_ID={},COMPONENT_ID={},THREAD_ID={},TRANSACTION_ID={},LOG_LEVEL={},MESSAGE_ID={},MESSAGE_TEXT={},CREATION_TIMESTAMP={},\n".format( \
            self.process_name, \
            self.component_name, \
            self.thread_id, \
            self.transaction_id, \
            log_level, \
            message_id, \
            message_text, \
            self.event_ts))

    def stats_body(self,fh):
        statistic_name = 'XYZ_Latency_' + str(random.choice(self.STATISTIC_LIST)).rjust(3,'0')
        statistic_duration = round(random.uniform(0.1,self.MAX_STATISTIC_LATENCY),2)
        fh.write("PROCESS_ID={},COMPONENT_ID={},TRANSACTION_ID={},STATISTIC_NAME={},STATISTIC_DURATION={},CREATION_TIMESTAMP={},\n".format( \
            self.process_name, \
            self.component_name, \
            self.transaction_id, \
            statistic_name, \
            statistic_duration, \
            self.event_ts))

    def edr_body(self,fh):
        subscriber_types = ['REG','BUS','VIP','EMP']
        notification_types = ['EMAIL','SMS']
        reg_plans = ['REG_PLAN_1','REG_PLAN_2','REG_PLAN_X']
        bus_plans = ['BUS_PLAN_1','BUS_PLAN_2','BUS_PLAN_X']
        subscriber_id = str(uuid.uuid4().fields[5]).rjust(16,'0')
        subscriber_type = subscriber_types[random.choice(self.SUBSCRIBER_TYPE_BIAS)]
        group_id = random.choice(self.GROUP_BIAS)
        if group_id != 1:
            group_id = subscriber_type + "G_" + str(uuid.uuid4().fields[1])[0:3]
        else:
            group_id = 'NONE'
        device_id = str(uuid.uuid4().fields[0]).rjust(10,'0')
        notification_type = notification_types[random.choice(self.NOTIFICATION_BIAS)]
        notification_address = device_id
        if notification_type[0] == 'E':
            notification_address = subscriber_id + "@" + subscriber_type.lower() + "-example.com"
        if subscriber_type[0] == 'R':
            plan_id = reg_plans[random.choice(self.REG_PLAN_BIAS)]
        else:
            plan_id = bus_plans[random.choice(self.BUS_PLAN_BIAS)]
        if plan_id in ['REG_PLAN_1','BUS_PLAN_1']:
            usage = random.choice(self.USAGE_COUNTER_LIST_1)
        elif plan_id in ['REG_PLAN_2','BUS_PLAN_2']:
            usage = random.choice(self.USAGE_COUNTER_LIST_2)
        elif plan_id in ['REG_PLAN_X','BUS_PLAN_X']:
            usage = random.choice(self.USAGE_COUNTER_LIST_3)
        if subscriber_type[0] not in ['V','E']:
            if plan_id in ['REG_PLAN_1','BUS_PLAN_1']:
                charge_amount = format(self.CHARGE_AMOUNT_LIST_1[(self.USAGE_COUNTER_LIST_1.index(usage))]/100.00,'.3f')
            elif plan_id in ['REG_PLAN_2','BUS_PLAN_2']:
                charge_amount = format(self.CHARGE_AMOUNT_LIST_2[(self.USAGE_COUNTER_LIST_2.index(usage))]/100.00,'.3f')
            elif plan_id in ['REG_PLAN_X','BUS_PLAN_X']:
                charge_amount = format(self.CHARGE_AMOUNT_LIST_3[(self.USAGE_COUNTER_LIST_3.index(usage))]/100.00,'.3f')
        else:
            charge_amount = format(0, '.3f')
        fh.write("PROCESS_ID={},COMPONENT_ID={},TRANSACTION_ID={},SESSION_ID={},EVENT_TIMESTAMP={},EVENT_TYPE={},DIVISION_ID={},GROUP_ID={},SUBSCRIBER_ID={},SUBSCRIBER_TYPE={},DEVICE_ID={},PLAN_ID={},NOTIFICATION_TYPE={},NOTIFICATION_ADDRESS={},USAGE={},CHARGE_AMOUNT={},\n".format( \
            self.process_name, \
            self.component_name, \
            self.transaction_id, \
            self.session_id, \
            self.event_ts, \
            self.event_type, \
            self.div_id, \
            group_id, \
            subscriber_id, \
            subscriber_type, \
            device_id, \
            plan_id, \
            notification_type, \
            notification_address, \
            usage, \
            charge_amount))

def main(argv):
    if len(argv) == 0:
        print(USAGE_INFO)
        return 1
    try:
        opts, args = getopt.getopt(argv,"hi:d:s:e:r:", \
            ["help", \
            "system_id=", \
            "division_id=", \
            "start_datetime=", \
            "end_datetime=", \
            "record_count="])
    except Exception, err:
        sys.stderr.write("Exception:: %s\n" % str(err))
        print(USAGE_INFO)
        return 1
    system_id = None
    division_id = None
    start_datetime = None
    end_datetime = None
    record_count = None
    for opt, arg in opts:
        if opt in ('-h' , "--help"):
            print (USAGE_INFO)
            return 1
        elif opt in ('-i', "--system_id"):
            system_id = arg.lower()
        elif opt in ('-d', "--division_id"):
            division_id = arg.upper()
        elif opt in ('-s', "--start_datetime"):
            start_datetime = arg
        elif opt in ('-e', "--end_datetime"):
            end_datetime = arg
        elif opt in ('-r', "--record_count"):
            record_count = int(arg)
    if (system_id is not None) and \
        (division_id is not None) and \
        (start_datetime is not None) and \
        (end_datetime is not None) and \
        (record_count is not None):
        pm = pcrf_csv_kv(system_id,division_id,start_datetime,end_datetime)
        ec = [0,0]
        try:
            edr_fh = open(pm.edr_filename,'w')
            ulog_fh = open(pm.ulog_filename,'w')
            stats_fh = open(pm.stats_filename,'w')
            try:
                for i in range(0,record_count):
                    pm.core_init()
                    pm.edr_body(edr_fh)
                    for j in range(0,pm.XYZ_LATENCY_LIMIT):
                        pm.ulog_body(ulog_fh)
                        pm.stats_body(stats_fh)
            except Exception, err:
                sys.stderr.write("Exception:: %s\n" % str(err))
                ec[1] = 1
            finally:
                edr_fh.close()
                ulog_fh.close()
                stats_fh.close()
            return ec[1]
        except Exception, err:
            sys.stderr.write("Exception:: %s\n" % str(err))
            ec[0] = 1
        finally:
            edr_fh.close()
            ulog_fh.close()
            stats_fh.close()
            return ec[0]
    else:
        print(USAGE_INFO)
        return 1

if __name__ == "__main__":
    #profile.run('sys.exit(main(sys.argv[1:]))')
    sys.exit(main(sys.argv[1:]))
