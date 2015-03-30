#!/usr/bin/python3

import os, sys, datetime, subprocess, re, time
from tzlocal import get_localzone

audio_dir="/home/sangmank/radio"
prefix="mc_"

def calculate_offset(filename):
    now = datetime.datetime.now(get_localzone())
    filename, fileext = os.path.splitext(filename)
    filetime_str = filename[len(prefix):]
    year = filetime_str[0:4]
    month = filetime_str[4:6]
    day = filetime_str[6:8]
    hour = filetime_str[9:11]
    if len(filetime_str) > 12:
        minute = filetime_str[11:13]
    else:
        minute = "0"
    if len(filetime_str) > 14:
        second = filetime_str[13:15]
    else:
        second = "0"
        
    filetime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), tzinfo=get_localzone())
    return int((now - filetime).total_seconds())

def usage():
    print("Usage: %s {[offset]} {[duration]}" % sys.argv[0])

def duration_to_int(duration_str):
    m = re.match(r'(\d+):(\d+):(\d+)', duration_str)
    if not m:
        raise Exception("Duration format not matched %s" % duration_str)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))

audio_files = [f for f in os.listdir(audio_dir) if os.path.basename(f).startswith(prefix)]

CLOSEST = -1

try:
    offset_sec = (len(sys.argv) == 1) and CLOSEST or duration_to_int(sys.argv[1])
    duration_sec = (len(sys.argv) < 2) and (3600 - 2) or duration_to_int(sys.argv[2])
except e:
    print("Error: %s"%e)
    usage()
    sys.exit(1)

if offset_sec == CLOSEST:
    file_to_play = sorted(audio_files, key=calculate_offset)[0]
else:
    file_to_play = sorted(audio_files, key=lambda x:abs(calculate_offset(x) - offset_sec))[0]

start_time = datetime.datetime.now(get_localzone())
end_time = start_time + datetime.timedelta(seconds=duration_sec)

while True:
    out = subprocess.check_call("/usr/bin/mpg123 %s 2>&1 | ts '[%%Y-%%m-%%d %%H:%%M:%%S]'" % os.path.join(audio_dir, file_to_play), shell=True)
    time.sleep(5)
    cur_time = datetime.datetime.now(get_localzone())
    if cur_time >= end_time:
        break
