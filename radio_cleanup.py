#!/usr/bin/python3

import os, sys, datetime, subprocess

audio_dir="/home/sangmank/radio"
prefix="mc_"
file_limit = 512 * (1 << 20)

def file_size(filename):
    return os.stat(filename).st_size

audio_files = sorted([os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if os.path.basename(f).startswith(prefix)], reverse=True)

to_delete = []
sum_files = 0
for f in audio_files:
    sum_files += file_size(f)
    if sum_files > file_limit:
        to_delete.append(f)

for f in to_delete:
    os.remove(f)
