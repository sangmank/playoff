#!/usr/bin/python3

import os, sys, datetime, re, subprocess, time
from tzlocal import get_localzone

audio_dir="/home/sangmank/radio"
prefix="mc_"
url = "http://mfmtunein.imbc.com/tmfm/_definst_/tmfm.stream/playlist.m3u8"

def usage():
    print("Usage: %s {[duration]}" % sys.argv[0])

def duration_to_int(duration_str):
    m = re.match(r'(\d+):(\d+):(\d+)', duration_str)
    if not m:
        raise Exception("Duration format not matched %s" % duration_str)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))

def main():
    try:
        duration_str = len(sys.argv) < 2 and "00:59:55" or sys.argv[1]
        duration_sec = duration_to_int(duration_str)
    except e:
        print("Error: %s"%e)
        usage()
        sys.exit(1)

    start_time = datetime.datetime.now(get_localzone())
    end_time = start_time + datetime.timedelta(seconds=duration_sec)
    cur_time = start_time
    
    while True:
        filename = prefix + cur_time.strftime("%Y%m%d_%H%M%S") + ".mp3"
        cmd = 'ffmpeg -i "%s" -t %s  -codec:a libmp3lame -qscale:a 8 -y %s 2>&1 | ts "[%%Y-%%m-%%d %%H:%%M:%%S]"' % (url, duration_str, os.path.join(audio_dir, filename))
        print(cmd)
        out = subprocess.check_call(cmd, shell=True)
        time.sleep(5)
        cur_time = datetime.datetime.now(get_localzone())
        if cur_time >= end_time:
            print("Passed the end time. Ending the record")
            break
        duration = end_time - cur_time

        if duration.total_seconds() < 10:
            time.sleep(duration.total_seconds())
            print("Almost the end time. Ending the record")
            break

        hours = duration.total_seconds()/3600
        minutes = (duration.total_seconds() % 3600) / 60
        seconds = duration.total_seconds() % 60
        duration_str = "%d:%d:%d"%(hours, minutes, seconds)

if __name__ == "__main__":
    main()
