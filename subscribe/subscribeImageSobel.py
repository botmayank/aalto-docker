#!/usr/bin/python
import paho.mqtt.client as mqtt
import json
import base64
import numpy as np
import scipy
from scipy import ndimage

picture  = []
count = 0

def processImage(picture):
    with open("recvd.jpg", "wb") as image_file:
        image_file.write(base64.decodestring(picture))
    im = scipy.misc.imread('recvd.jpg')
    im = im.astype('int32')
    dx = ndimage.sobel(im, 0)
    dy = ndimage.sobel(im, 1)
    mag = np.hypot(dx, dy)
    mag *= 255.0 / np.max(mag)
    scipy.misc.imsave('sobel.jpg', mag)

def on_connect(mqttc, obj, flags, rc):
    print("Connected, result code: "+str(rc))

def on_message(mqttc, obj, msg):
    global picture, count

    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    part = json.JSONDecoder().decode(msg.payload)
    if part['pos'] == 0:
        picture = ['0']*int(part['size']+1)     
        picture[part['pos']] = part['data']
        count = part['size']        
    else:
        picture[part['pos']] = part['data']
        count -= 1
        if count == 0:           
            print "Received full image"
            processImage(''.join(picture))
            print "Output image saved as sobel.jpg"

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("iot.eclipse.org", 1883, 60)
mqttc.subscribe("Image-Data", 0)
mqttc.loop_forever()