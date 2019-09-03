#!/bin/bash

# https://community.emlid.com/t/my-software-setup-using-4g-mission-planner-gstreamer/3031/32
#docker run --privileged --rm -it psaghelyi/dronekit:video_streaming \
#  raspivid -n -t 0 -rot 180 -w 960 -h 720 -fps 30 -b 2000000 -co 60 -sh 30 -sa 10 -o - | \
#  gst-launch-1.0 -e -vvvv fdsrc ! h264parse ! rtph264pay pt=96 config-interval=5 ! udpsink host=25.23.28.85 port=5004

#docker run --privileged --rm -it -p 5004:5004 psaghelyi/dronekit:video_streaming \
#  raspivid -t 0 -n -a 12 -b 2000000 -pf high --mode 5 -fps 30 -g 60 --flush -o - | \
#  gst-launch-1.0 -e -vvvv fdsrc ! h264parse ! rtph264pay config-interval=5 pt=96 ! tcpserversink host=0.0.0.0 port=5004


# RAW H.264 stream
# client: gst-launch-1.0.exe tcpclientsrc host=25.72.139.4 port=5004 ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
###
docker run --privileged --rm -it -p 5004:5004 psaghelyi/dronekit:video_streaming \
  raspivid -t 0 -n -a 12 -b 2000000 -pf high --mode 5 -fps 30 -g 60 --flush -l -o tcp://0.0.0.0:5004 -rot 180

