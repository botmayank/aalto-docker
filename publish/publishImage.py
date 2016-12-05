#!/usr/bin/python
import base64
from time import sleep
import paho.mqtt.client as mqtt
import random, string
import math
import json
import picamera

mqttc = mqtt.Client()
camera = picamera.PiCamera()
packet_size = 3000

try:
    camera.start_preview()
    sleep(1)
    camera.capture('input.jpg', resize=(500,281))
    camera.stop_preview()
    pass
finally:
    camera.close()

def convertImageToBase64():
    with open("input.jpg", "rb") as image_file:
        encoded = base64.b64encode(image_file.read())
        return encoded

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def publishEncodedImage(encoded):
    end = packet_size
    start = 0
    length = len(encoded)
    picId = randomword(8)
    pos = 0
    no_of_packets = math.ceil(length/packet_size)

    while start <= len(encoded):            
        data = {"data": encoded[start:end], "pic_id":picId, "pos": pos, "size": no_of_packets}
        mqttc.publish("Image-Data",json.JSONEncoder().encode(data))
        end += packet_size
        start += packet_size
        pos = pos + 1
        sleep(0.1)

mqttc.connect("iot.eclipse.org", 1883, 60)
mqttc.loop_start()

encoded = convertImageToBase64()
publishEncodedImage(encoded)
