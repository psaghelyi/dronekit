#!/bin/bash

docker run -it psaghelyi/dronekit:mavproxy --master=/dev/ttyAMA0,921600 --out=udp:$1:14550 --out=udp:$1:14551 --aircraft=MyCopter"
