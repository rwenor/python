#!/bin/bash
sleep 2

cd /home/pi/Python
python tdtool-with-sensors.py -d 2821615
python tdtool-with-sensors.py -d 3017840

while true 
do
  python tdtool-with-sensors.py -d 2821615  >> TempLogBad.dat
  python tdtool-with-sensors.py -d 3017840  >> TempLogBad.dat
  sleep 600
done

