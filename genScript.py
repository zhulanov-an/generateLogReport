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
CNT_REQ_KEY_REPORT = "count_requests"
CNT_BY_TYPE_REQ_KEY_REPORT = "count_by_type_requests"
TOP_IP_KEY_REPORT = "top_ip"
TOP_LONGEST_REQ_KEY_REPORT = "the_longest_requests"
TOP_CLIENT_ERROR_KEY_REPORT = "top_client_error_key_report"
TOP_SERVER_ERROR_KEY_REPORT = "top_server_error_key_report"

REPORT = {
    CNT_REQ_KEY_REPORT: 0,
    CNT_BY_TYPE_REQ_KEY_REPORT: defaultdict(int),
    TOP_IP_KEY_REPORT: defaultdict(int),
    TOP_LONGEST_REQ_KEY_REPORT: list(),
    TOP_CLIENT_ERROR_KEY_REPORT: defaultdict(list),
    TOP_SERVER_ERROR_KEY_REPORT: defaultdict(list)
}

CNT_OF_MOST_COMMON = 10

# key items
IP_KEY_ITEM = "ip"
TYPE_REQ_KEY_ITEM = "type_req"
DURATION_KEY_ITEM = "duration"
URL_KEY_ITEM = "url"
TIME_KEY_ITEM = "time"
STATUS_KEY_ITEM = "status"

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


def get_dict_by_line(line):
    def get_value_by_regex(regex, value, type_value=str):
        try:
            match = re.findall(regex, value)
            return type_value(match[0])
        except Exception as e:
            exit(f"ошибка поиска по маске {regex} в значении {value}")

    regex_ip = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    regex_type_req = r"OPTIONS|GET|HEAD|POST|PUT|PATCH|DELETE|TRACE"
    regex_duration = r'\"\s\d{3}\s(\d+)\s'
    regex_url = r'\".+\s(.+)\sHTTP'
    regex_time = r'\[(.+)\]'
    regex_status = r'\"\s(\d{3})\s\d+\s'

    d = dict()
    d[IP_KEY_ITEM] = get_value_by_regex(regex_ip, line)
    d[TYPE_REQ_KEY_ITEM] = get_value_by_regex(regex_type_req, line)
    d[DURATION_KEY_ITEM] = get_value_by_regex(regex_duration, line, type_value=int)
    d[URL_KEY_ITEM] = get_value_by_regex(regex_url, line)
    d[TIME_KEY_ITEM] = get_value_by_regex(regex_time, line)
    d[STATUS_KEY_ITEM] = get_value_by_regex(regex_status, line, type_value=int)
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


def get_count_requests(lines):
    return len(lines)


def get_count_by_type_request(lines):
    req_type_cnt = defaultdict(int)
    for line in lines:
        type_req = line[TYPE_REQ_KEY_ITEM]
        req_type_cnt[type_req] += 1
    return req_type_cnt


def get_top_ip(lines):
    ips = [line[IP_KEY_ITEM] for line in lines]
    cnt = Counter(ips)
    top = cnt.most_common(CNT_OF_MOST_COMMON)
    return dict(top)


def get_max_duration(lines):
    sort_by_duration = sorted(lines, key=lambda d: d[DURATION_KEY_ITEM])[:CNT_OF_MOST_COMMON]
    dur_list = list()
    for l in sort_by_duration:
        dur_list.append(
            {
                TYPE_REQ_KEY_ITEM: l.get(TYPE_REQ_KEY_ITEM),
                URL_KEY_ITEM: l.get(URL_KEY_ITEM),
                IP_KEY_ITEM: l.get(IP_KEY_ITEM),
                DURATION_KEY_ITEM: l.get(DURATION_KEY_ITEM)
            }
        )
    return dur_list


def most_common_record_by_duration(lines):
    report_long_req = lines + REPORT[TOP_LONGEST_REQ_KEY_REPORT]
    return sorted(report_long_req, key=lambda d: d[DURATION_KEY_ITEM], reverse=True)[:CNT_OF_MOST_COMMON]


def get_common_error(lines, start_err, end_err):
    d_client_err = dict()
    for err in range(start_err, end_err + 1):
        d_client_err[err] = list(filter(lambda l: l[STATUS_KEY_ITEM] == err, lines))

    def order_by_len(item):
        return len(item[1])

    sorted_by_cnt_error = sorted(d_client_err.items(), key=order_by_len, reverse=True)[:CNT_OF_MOST_COMMON]
    return dict(sorted_by_cnt_error)


for log in get_path_logs(logdir, logfile):
    d_lines = get_lines(log)
    cnt = get_count_requests(d_lines)
    req_type_cnt = get_count_by_type_request(d_lines)
    top_ips = get_top_ip(d_lines)
    dur_lines = get_max_duration(d_lines)
    top_client_error_lines = get_common_error(d_lines, 400, 499)
    top_server_error_lines = get_common_error(d_lines, 500, 526)

    REPORT[CNT_REQ_KEY_REPORT] = REPORT[CNT_REQ_KEY_REPORT] + cnt
    REPORT[CNT_BY_TYPE_REQ_KEY_REPORT] = REPORT[CNT_BY_TYPE_REQ_KEY_REPORT] | req_type_cnt
    REPORT[TOP_IP_KEY_REPORT] = REPORT[TOP_IP_KEY_REPORT] | top_ips
    REPORT[TOP_LONGEST_REQ_KEY_REPORT] = most_common_record_by_duration(dur_lines)
    REPORT[TOP_CLIENT_ERROR_KEY_REPORT] = REPORT[TOP_CLIENT_ERROR_KEY_REPORT] | top_client_error_lines
    REPORT[TOP_SERVER_ERROR_KEY_REPORT] = REPORT[TOP_SERVER_ERROR_KEY_REPORT] | top_server_error_lines

with open('report.json', 'w') as fp:
    json.dump(REPORT, fp, indent=4)
