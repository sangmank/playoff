#!/usr/bin/python3

import os, sys, datetime, subprocess
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
    filetime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), tzinfo=get_localzone())
    return int((now - filetime).total_seconds()/3600)

audio_files = [f for f in os.listdir(audio_dir) if os.path.basename(f).startswith(prefix)]

CLOSEST = -1

if len(sys.argv) == 1:
    offset = CLOSEST
else:
    offset = int(sys.argv[1])

print(list(map(lambda x:(x, abs(calculate_offset(x) - offset),), audio_files)))
print(sorted(audio_files, key=lambda x:abs(calculate_offset(x) - offset)))
if offset == CLOSEST:
    file_to_play = sorted(audio_files, key=calculate_offset)[0]
else:
    file_to_play = sorted(audio_files, key=lambda x:abs(calculate_offset(x) - offset))[0]

out = subprocess.check_call(["/usr/bin/mpg123", os.path.join(audio_dir, file_to_play)])
print("mpg123 out: %d"%out)
