#!/bin/bash

DATE=`date +%Y%m%d_%H%M`
DIR="/home/sangmank/radio/"
TIME=$1
if [[ -z $TIME ]]; then
  TIME=0:59:58
fi

mkdir -p $DIR

ffmpeg -i "http://mfmtunein.imbc.com/tmfm/_definst_/tmfm.stream/playlist.m3u8" -t $TIME  -codec:a libmp3lame -qscale:a 8 -y $DIR/mc_$DATE.mp3
