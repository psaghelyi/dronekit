FROM python:2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./sitl sitl
COPY ./mavproxy mavproxy
COPY ./start.sh start.sh

CMD ./start.sh

#EXPOSE 14551:14551/udp
