#!/usr/bin/python3

import os, sys, datetime, subprocess, re, time
import time
import logging
from tzlocal import get_localzone

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

audio_dir="/home/sangmank/radio"
prefix="mc_"

def calculate_offset(filename):
    #tzinfo = time.timezone
    tzinfo = get_localzone()
    now = datetime.datetime.now(tzinfo)
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
    filetime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), tzinfo=now.tzinfo)
    return int((now - filetime).total_seconds())

def usage():
    print("Usage: %s {[offset]} {[duration]}" % sys.argv[0])

def duration_to_int(duration_str):
    m = re.match(r'(\d+):(\d+):(\d+)', duration_str)
    if not m:
        raise Exception("Duration format not matched %s" % duration_str)
    logger.debug("duration_to_int %s"%duration_str)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))

def pick_file(candidate_files, offset):
    # Anyfile that is within the 10 seconds of (the file offset - timezone offset)
    threshold_sec = 10
    for candidate in candidate_files:
        logger.debug("file: {} file offset: {}, offset: {}".format(candidate, calculate_offset(candidate), offset))
        if -threshold_sec <= (calculate_offset(candidate) - offset) <= threshold_sec:
            return candidate
    return None

def play_radio_files(candidates, time_offset_sec, duration_sec):
    start_time = datetime.datetime.now(get_localzone())
    end_time = start_time + datetime.timedelta(seconds=duration_sec)

    sleep_printed=False
    while True:
        file_to_play = pick_file(candidates, time_offset_sec)
        if not file_to_play:
            if not sleep_printed:
                logger.info("No file to play. Sleep")
                sleep_printed = True
            time.sleep(5)
            continue
        logger.info("file: {}".format(file_to_play))

        sleep_printed = False
        out = subprocess.check_call("/usr/bin/mpg123 %s 2>&1 | ts '[%%Y-%%m-%%d %%H:%%M:%%S]'" % os.path.join(audio_dir, file_to_play), shell=True)
        time.sleep(5)
        cur_time = datetime.datetime.now(get_localzone())
        if cur_time >= end_time:
            break


def main():
    if len(sys.argv) < 3:
        print("Usage: {} [time_offset] [record_duration] (both are of the form 10:00:00 HH:MM:SS)".format(sys.argv[0]))
        sys.exit(1)

    try:
        time_offset_sec = duration_to_int(sys.argv[1])
        # record 10 seconds less to avoid overflowing a time period
        duration_sec = max(duration_to_int(sys.argv[2]) - 10, 0)
    except Exception as e:
        print("Error: %s"%e)
        usage()
        sys.exit(1)

    audio_files = [f for f in os.listdir(audio_dir) if os.path.basename(f).startswith(prefix)]

    play_radio_files(audio_files, time_offset_sec, duration_sec)

if __name__ == "__main__":
    main()
