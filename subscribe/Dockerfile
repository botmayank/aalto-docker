#FROM resin/rpi-raspbian:jessie
FROM ubuntu:16.04
RUN apt-get update && apt-get install -y \
    python \
    python-numpy \
    python-scipy \
    python-pip   

RUN pip install paho-mqtt

ADD subscribeImageSobel.py /
CMD ["python","./subscribeImageSobel.py"]