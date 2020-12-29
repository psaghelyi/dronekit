# https://codecalamity.com/raspberry-pi-hardware-accelerated-h264-webcam-security-camera/

## Video Devices

`v4l2-ctl --list-devices`

`v4l2-ctl -d /dev/video0 --list-formats-ext`

## Audio Devices

`arecord -l`

## Tell the webcam we live in a 50hz power area (removes flicker)
`v4l2-ctl --device=/dev/video0 -c power_line_frequency=1`

`ffmpeg -nostdin -hide_banner -loglevel error -f v4l2 -input_format h264 -s 1920x1080 -i /dev/video1 -f alsa -ac 1 -i hw:2,0 -map 0:0 -map 1:0 -c:a aac -b:a 96k -ar 44100 -c:v copy -f rtsp rtsp://localhost:8554/streaming1`




`ffmpeg -f v4l2 -input_format h264 -profile:v high -s 1920x1080 -i /dev/video1 -f alsa -ac 2 -ar 44100 -i hw:CARD=C920,DEV=0 -map 0:0 -map 1:0 -c:a aac -b:a 128k -ar 44100 -c:v copy -f rtsp rtsp://localhost:8554/streaming1`




`ffmpeg -nostdin -hide_banner -loglevel error -input_format yuyv422 
 -f video4linux2 -s 1280x720 -r 10 -i /dev/video0 -c:v h264_omx -r 10 -b:v 2M 
 -vf "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf 
 :text='%{localtime}:x=8:y=8:fontcolor=white: box=1: boxcolor=black" -an 
 -f rtsp rtsp://localhost:80/live/stream`


`ffmpeg -nostdin -hide_banner -loglevel error -f v4l2 -input_format h264 -s 1920x1080 -i /dev/video1 -c:v copy -f rtsp rtsp://localhost:8554/streaming1`

OK:
 
`ffmpeg -nostdin -hide_banner -loglevel error -f v4l2 -input_format yuyv422 -s 1024x768 -r 10 -i /dev/video0 -c:v h264_omx -r 10 -b:v 2M -an -f rtsp rtsp://localhost:8554/streaming0`


# OK for rpiCameraV1

raspicam -> omx -> rtsp

`ffmpeg -nostdin -hide_banner -loglevel error -f v4l2 -input_format yuyv422 -s 1280x720 -r 25 -i /dev/video0 -vf hflip,vflip -c:v h264_omx -r 25 -b:v 2M -f rtsp rtsp://localhost:8554/streaming0`

raspicam -> rtsp

`ffmpeg -nostdin -hide_banner -loglevel error -f v4l2 -input_format h264 -s 1280x720 -i /dev/video0 -c:v copy -metadata:s:v:0 rotate=180 -f rtsp rtsp://localhost:8554/streaming0`
