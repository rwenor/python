#!/bin/bash 
COUNTER=0
i=0
while [  $COUNTER -lt 10 ]; do
    echo The counter is $COUNTER
    
    sudo raspivid -o video.h264 -t 10000 -w 320 -h 240 -vf -hf
    filename="vid-$i.mp4"

    MP4Box -add video.h264 "$filename"
    let i=i+1
    # MP4Box -add video.h264 video2.mp4
    let COUNTER=COUNTER+1 
done
