FROM resin/rpi-raspbian:jessie
RUN apt-get update && apt-get install -y \
    python \
    python-picamera \
    python-pip
RUN pip install paho-mqtt


ADD publishImage.py /
CMD ["python","./publishImage.py"]