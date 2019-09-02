FROM raspbian/stretch

WORKDIR /usr/local/src

RUN apt-get update && apt-get install -y \
    libraspberrypi-bin \
    git

RUN git clone https://gist.github.com/d8abbcae85a76d69b228827e2d9e4d72.git sqwk

RUN chmod +x sqwk/gstreamer.sh

RUN sqwk/gstreamer.sh

EXPOSE 5004

