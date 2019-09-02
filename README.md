## First steps

**Enable ssh:**

create `/boot/ssh`

**Setup headless wifi:**

edit `/boot/wpa_supplicant.conf`

```
country=HU
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
  ssid="your_real_wifi_ssid"
  psk="your_real_password"
}
```

**Configure RaspberryPi:**

`$ sudo raspi-config`

-   Change password
-   Enable serial, disable boot logs export to serial
-   Enable camera

 **Check/set ttyAMA0 speed:**

`$ sudo stty -F /dev/ttyAMA0 921600`

Edit `/boot/config.txt`:

```
init_uart_clock=64000000
```

> Still a question if BT is interfering with serial
See here: [https://www.raspberrypi.org/documentation/configuration/uart.md](https://www.raspberrypi.org/documentation/configuration/uart.md)

**Edit /boot/config.txt:**

```
dtoverlay=pi3-disable-wifi
dtoverlay=pi3-disable-bt
```

**Update Raspbian:**

`$ sudo apt-get update`

`$ sudo apt-get -y dist-upgrade`

**Optionally Install camera module:**

`$ sudo modprobe bcm2835-v4l2 gst_v4l2src_is_broken=1`

**Optionally change swap size to 1024:**

`$ sudo nano /etc/dphys-swapfile`

`$ sudo /etc/init.d/dphys-swapfile stop`

`$ sudo /etc/init.d/dphys-swapfile start`

## Docker

1. Remove old version of Docker if necessarry:

`$ sudo apt-get remove docker docker-engine docker.io containerd runc`

2. Install Docker using the convenience script:

`$ curl -fsSL https://get.docker.com -o get-docker.sh`

`$ sudo sh get-docker.sh`

`$ sudo usermod -aG docker pi`

## LTE 4g

`$ sudo apt-get -y install ppp wvdial usb-modeswitch`

Edit: `/etc/wvdial.conf`

```
[Dialer Defaults]
Init1 = ATZ
Init2 = AT+CFUN=1,0
Init3 = ATQ0 V1 E1 H0 S0=0
Init4 = AT+CGDCONT=1,"IP","internet.vodafone.net"
New PPPD = Yes
ISDN = 0
Stupid Mode = 1
Dial Command = ATDT
Auto Reconnect = 1
Idle Seconds = 0
Phone = *99#
Modem = /dev/gsmmodem
Username = { }
Password = { }
Baud = 460800
```

Edit: `/etc/network/interfaces`

```
auto ppp0
iface ppp0 inet wvdial
```

Testing connection:

`$ sudo wvdial & disown`

>Note: `disown` allows you to close the terminal

Create: `/home/pi/modemstart.sh`

```
#!/bin/bash
ifdown ppp0
ifup ppp0 
```

`$ sudo chmod +x /home/pi/modemstart.sh`

Edit: `/etc/rc.local`

```
sh '/home/pi/modemstart.sh'
```

## Hamachi

**Install**

`$ sudo wget https://www.vpn.net/installers/logmein-hamachi_2.1.0.203-1_armhf.deb`

`$ sudo dpkg -i logmein-hamachi_2.1.0.203-1_armhf.deb`

**CLI**

`$ sudo hamachi login`

**Settings**

|   |   |   |
|----|-----|------|
|LogMeIn account |	psaghelyi@gmail.com	| 12***99 |
|Network-id	| 345-995-738 | t***6 |
 
`$ sudo hamachi join <Network-id>`

**GUI**

[https://www.haguichi.net/](https://www.haguichi.net/)

`$ sudo apt install dirmngr`

`$ sudo sh -c 'echo "deb http://ppa.launchpad.net/webupd8team/haguichi/ubuntu bionic main" > /etc/apt/sources.list.d/haguichi.list'`

`$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C2518248EEA14886`

`$ sudo apt update`

`$ sudo apt install -y haguichi`

## MAVLink and Python

>Disable the OS control of the serial port with raspi-config

`$ sudo apt-get install screen`

`$ sudo pip install mavproxy`

**Test:**

`$ sudo -s`

`$ mavproxy.py --master=/dev/ttyAMA0,921600 --aircraft=MyCopter`

>Note: on rPI3 ttyS0 is the serial port

**Mav console commands to disable arm checks:**

```
param show ARMING_CHECK
param set ARMING_CHECK 0
arm throttle
```

To setup MAVProxy to start whenever the RPi is restarted open a terminal window and edit the `/etc/rc.local` file, adding the following lines just before the final “exit 0” line:

```
(
date
echo $PATH
PATH=$PATH:/bin:/sbin:/usr/bin:/usr/local/bin
export PATH
cd /home/pi
screen -d -m -s /bin/bash mavproxy.py --master=/dev/ttyAMA0,921600 --out=udp:<ip-of-ground>:14550 --out=udp:<ip-of-ground>:14551 --aircraft=MyCopter
) > /tmp/rc.log 2>&1
exit 0
```

Whenever the RPi connects to the Pixhawk, three files will be created in the `/home/pi/MyCopter/logs/YYYY-MM-DD` directory:

- `mav.parm` : a text file with all the parameter values from the Pixhawk
- `flight.tlog` : a telemetry log including the vehicles altitude, attitude, etc which can be opened using the mission planner (and a number of other tools)
- `flight.tlog.raw` : all the data in the .tlog mentioned above plus any other serial data received from the Pixhawk which might include non-MAVLink formatted messages like startup strings or debug output

If you wish to connect to the MAVProxy application that has been automatically started you can log into the RPi and type:

`$ sudo screen -x`

## Camera and Broadcasting

**Update firmware:**

`$ sudo apt-get install rpi-update`

`$ sudo rpi-update`

**Start camera at boot**

Edit: `/etc/rc.local`

```
(
  while : ; do
    /usr/bin/raspivid -t 0 -n -a 12 -b 2000000 -pf high --mode 5 -fps 30 -g 60 --flush -l -o tcp://0.0.0.0:5004
  done
) &
```

>Note: 
>- Set bitrate: `--bitrate,    -b`
>- Listen on port: `--listen,    -l`
>- Rotation:  `-rot 180`
>- Specify the intra refresh period (key frame rate/GoP): `--intra,    -g`
>- Specify H264 profile to use for encoding (baseline, main, high): `--profile,    -pf`
>- Specifies the H264 encoder level to use for encoding. Options are 4, 4.1, and  4.2: `--level,    -lev`
>-Sets the H264 intra-refresh type. Possible options are cyclic, adaptive,  both, and cyclicrows: `--irefresh,    -if`
>- Video stabilization: `--vstab,    -vs`
>- Insert PPS, SPS headers: `--inline,    -ih`
>- Insert timing information into the SPS block: `--spstimings,    -stm`
>- Forces a flush of output data buffers as soon as video data is written: `--flush,    -fl`


**Using screen**

Create: `/home/pi/camerastart.sh`

```
#!/bin/bash
while : ; do
  /usr/bin/raspivid -t 0 -n -a 12 -b 2000000 -pf high --mode 5 -fps 30 -g 60 --flush -l -o tcp://0.0.0.0:5004 -rot 180
done
```

`$ sudo chmod +x /home/pi/camerastart.sh`

Edit: `/etc/rc.local`

```
screen -dm -S mavlink camerastart
```

>`-d -m` Start screen in "detached" mode

>`-S` When creating a new session, this option can be used to specify a meaningful name for the session.


**PC raw TCP receiver:**

`gst-launch-1.0.exe tcpclientsrc host=rpi2 port=5004 ! h264parse ! avdec_h264 ! videoconvert ! autovideosink`

`(gst-launch-1.0.exe tcpclientsrc host=rpi2 port=5004 ! decodebin ! videoconvert ! autovideosink)`

Save to file whilst watching:

`gst-launch-1.0.exe -e tcpclientsrc host=raspberrypi port=5004 ! tee name=t ! queue ! qtmux ! filesink location=c:\\temp\\video.h264 t. ! queue ! h264parse ! avdec_h264 ! videoconvert ! autovideosink`

Convert to mp4:

`ffmpeg -framerate 30 -i c:\\temp\\video.h264 -c copy c:\\temp\\video.mp4`

### Camera modes:

>`--mode,    -md`

Version 1.x (OV5647)

|Mode   |Size   |Aspect<br/>Ratio  |Frame rates    |FOV    |Binning|
|---|:-:|--:|---|---|---|
|0	|automatic selection|
|1	|1920x1080	|16:9	|1-30fps	|Partial|None|
|2	|2592x1944	|4:3	|1-15fps	|Full   |None|
|3	|2592x1944	|4:3	|0.1666-1fps|Full	|None|
|4	|1296x972	|4:3	|1-42fps	|Full	|2x2|
|5	|1296x730	|16:9	|1-49fps	|Full	|2x2|
|6	|640x480	|4:3	|42.1-60fps	|Full	|2x2 plus skip|
|7	|640x480	|4:3	|60.1-90fps	|Full	|2x2 plus skip|

Version 2.x (IMX219)

|Mode   |Size   |Aspect<br/>Ratio  |Frame rates    |FOV    |Binning|
|---|:-:|--:|---|---|---|
|0	|automatic selection|				
|1	|1920x1080	|16:9	|0.1-30fps	|Partial	|None
|2	|3280x2464	|4:3	|0.1-15fps	|Full	|None
|3	|3280x2464	|4:3	|0.1-15fps	|Full	|None
|4	|1640x1232	|4:3	|0.1-40fps	|Full	|2x2
|5	|1640x922	|16:9	|0.1-40fps	|Full	|2x2
|6	|1280x720	|16:9	|40-90fps	|Partial	|2x2
|7	|640x480	|4:3	|40-200fps1	|Partial	|2x2

>[raspi camera docs](https://www.raspberrypi.org/documentation/raspbian/applications/camera.md)

### RTP payload

Install GStreamer 1.0 (full):

`$ sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-pulseaudio`

High quality:

`$ raspivid -n -t 0 -rot 180 -w 960 -h 720 -fps 30 -b 2000000 -co 60 -sh 30 -sa 10 -o - | gst-launch-1.0 -e -vvvv fdsrc ! h264parse ! rtph264pay pt=96 config-interval=5 ! udpsink host=#LOCALIP# port=5000`

Med quality:

`$ raspivid -n -t 0 -rot 180 -w 640 -h 480 -fps 30 -b 600000 -co 60 -sh 40 -sa 10 -o - | gst-launch-1.0 -e -vvvv fdsrc ! h264parse ! rtph264pay pt=96 config-interval=5 ! udpsink host=#LOCALIP# port=5000`

Low quality:

`$ raspivid -n -t 0 -rot 180 -w 320 -h 240 -fps 30 -b 250000 -co 60 -sh 50 -sa 10 -o - | gst-launch-1.0 -e -vvvv fdsrc ! h264parse ! rtph264pay pt=96 config-interval=5 ! udpsink host=#LOCALIP# port=5000`

TCP:

raspivid -t 0 -n -a 12 -b 2000000 -pf high --mode 5 -fps 30 -g 60 --flush -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=0.0.0.0 port=5000

raspivid -t 0 -h 720 -w 1080 -fps 25 -hf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=YOUR_RPI_IP_ADDRESS port=5000


## Bluetooth and RF Reader





