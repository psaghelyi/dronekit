FROM python:2

RUN pip install --no-cache-dir mavproxy

CMD mavproxy.py --master tcp:simulator:5760 --out udp:10.0.75.1:14551 --out udp:10.0.75.1:14550
