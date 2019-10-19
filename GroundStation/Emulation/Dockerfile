FROM python:3

RUN pip install --no-cache-dir dronekit-sitl mavproxy

CMD dronekit-sitl copter --home=47.496538,19.052661,0,180 &\
    mavproxy.py --master tcp:127.0.0.1:5760 --out udp:10.0.75.1:14551 --out udp:10.0.75.1:14550
