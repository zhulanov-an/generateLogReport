import argparse
import os
import os.path
from os.path import join
import json
import re
from collections import Counter
from collections import defaultdict

# main
LOGS = []
EXT_LOG = ".log"

# report
CNT_REQ_KEY = "count_requests"
CNT_BY_TYPE_REQ = "count_by_type_requests"
TOP_IP = "top_ip"

REPORT = {
    CNT_REQ_KEY: 0,
    CNT_BY_TYPE_REQ: defaultdict(int),
    TOP_IP: dict()
}

# key items
IP = "ip"
TYPE_REQ = "type_req"
DURATION = "duration"
URL = "url"
TIME = "time"
STATUS = "status"

parser = argparse.ArgumentParser()
parser.add_argument('--logdir',
                    help='directory of access log files')
parser.add_argument('--logfile',
                    help='access log file in script directory or in --logdir param')
args = parser.parse_args()
logdir = args.logdir
logfile = args.logfile


def get_path_logs(logdir, logfile):
    logs = []
    if not logdir and not logfile:
        exit("Choose log files directory or log file")
    elif logdir and not logfile:
        if os.path.exists(logdir) and os.path.isdir(logdir):
            exit(f"{logdir} isn't directory")
        for root, dirs, files in os.walk(logdir):
            for name in files:
                log_path = join(root, name)
                if name.endswith(EXT_LOG) and os.path.exists(log_path) and os.path.isfile(log_path):
                    logs.append(log_path)
    elif not logdir and logfile and logfile.endswith(EXT_LOG):
        logs.append(logfile)
    elif logdir and logfile and logfile.endswith(EXT_LOG):
        logs.append(join(logdir, logfile))
    else:
        exit(f"dir:{logdir} doesn't have {EXT_LOG} files")

    return logs


def get_count_requests(lines):
    return len(lines)


def get_count_by_type_request(lines):
    req_type_cnt = defaultdict(int)
    for line in lines:
        type_req = line[TYPE_REQ]
        req_type_cnt[type_req] += 1
    return req_type_cnt


def get_value_by_regex(regex, value):
    try:
        match = re.findall(regex, value)
        return match[0]
    except Exception as e:
        exit(f"ошибка поиска по маске {regex} в значении {value}")


def get_dict_by_line(line):
    regex_ip = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    regex_type_req = r"OPTIONS|GET|HEAD|POST|PUT|PATCH|DELETE|TRACE"
    regex_duration = r'\"\s\d{3}\s(\d+)\s'
    regex_url = r'\".+\s(.+)\sHTTP'
    regex_time = r'\[(.+)\]'
    regex_status = r'\"\s(\d{3})\s\d+\s'

    d = dict()
    d[IP] = get_value_by_regex(regex_ip, line)
    d[TYPE_REQ] = get_value_by_regex(regex_type_req, line)
    d[DURATION] = get_value_by_regex(regex_duration, line)
    d[URL] = get_value_by_regex(regex_url, line)
    d[TIME] = get_value_by_regex(regex_time, line)
    d[STATUS] = get_value_by_regex(regex_status, line)
    return d


def get_lines(file_path):
    d_lines = []
    try:
        with open(file_path) as f:
            lines = f.readlines()
    except Exception as e:
        exit(f"ошибка чтения файла {f}:{e}")

    for line in lines:
        d = get_dict_by_line(line)
        d_lines.append(d)
    return d_lines


def get_top_ip(lines):
    ips = [line[IP] for line in lines]
    cnt = Counter(ips)
    top = cnt.most_common(10)
    return dict(top)


def get_max_duration(lines):
    durs = [line[DURATION] for line in lines]
    cnt = Counter(durs)
    top = cnt.most_common(10)
    return dict(top)


for log in get_path_logs(logdir, logfile):
    d_lines = get_lines(log)
    cnt = get_count_requests(d_lines)
    req_type_cnt = get_count_by_type_request(d_lines)
    top_ips = get_top_ip(d_lines)

    REPORT[CNT_REQ_KEY] = REPORT[CNT_REQ_KEY] + cnt
    REPORT[CNT_BY_TYPE_REQ] = REPORT[CNT_BY_TYPE_REQ] | req_type_cnt
    REPORT[TOP_IP] = REPORT[TOP_IP] | top_ips

with open('report.json', 'w') as fp:
    json.dump(REPORT, fp)
