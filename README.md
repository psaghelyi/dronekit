## First steps

**Enable ssh:**
`touch /boot/ssh`

**Setup headless wifi:**
edit /boot/wpa_supplicant.conf
```
country=HU
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
  ssid="your_real_wifi_ssid"
  psk="your_real_password"
  key_mgmt=WPA-PSK
}
```
Update Raspbian:
`sudo apt-get update`
`sudo apt-get -y dist-upgrade`

**Configure RaspberryPi:**
`sudo raspi-config`

-   Change password
-   Enable serial, disable boot logs export to serial
-   Enable camera

 **Check/set ttyAMA0 speed:**
`sudo stty -F /dev/ttyAMA0 921600`

Edit /boot/config.txt:
`init_uart_clock=64000000`

> Still a question if BT is interfering with serial
See here: [https://www.raspberrypi.org/documentation/configuration/uart.md](https://www.raspberrypi.org/documentation/configuration/uart.md)

Edit /boot/config.txt:
`dtoverlay=pi3-disable-wifi`
`dtoverlay=pi3-disable-bt`

Optionally Install camera module
`sudo modprobe bcm2835-v4l2 gst_v4l2src_is_broken=1`

Optionally change swap size to 1024
`sudo nano /etc/dphys-swapfile`
`sudo /etc/init.d/dphys-swapfile stop`
`sudo /etc/init.d/dphys-swapfile start`
