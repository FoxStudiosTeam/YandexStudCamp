#!/bin/sh

cd /home/pi/work/mjpg-streamer/mjpg-streamer-experimental
sudo ./start.sh &

#sudo kill -9 `ps -ef| grep mjpg_streamer| awk '{print $2}'`



