FROM ubuntu

RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y python python-dev python-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install mavproxy dronekit dronekit-sitl

COPY ./sitl sitl
COPY ./mavproxy mavproxy
COPY ./start.sh start.sh
CMD ./start.sh

#EXPOSE 14551:14551/udp
