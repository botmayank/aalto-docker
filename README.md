Demo for a simple Docker image for Raspberry Pi
===============================================

The publisher script captures an image with the Raspberry Pi Camera, converts it into a base64 string, fragments it and sends it using MQTT.
The subscriber script listens for the incoming packets, reconstructs the image and then applies a basic Sobel filter on it and saves the output. 

To build the docker images, in each of the directories, run
`docker build -t <name_of_image> .`

To run the publisher, run
`docker run --device /dev/vchiq -t <name_of_image>`

To run the subscriber, run
`docker run -t <name_of_image>`

To check filesystem of running docker
`sudo docker exec -t -i 2c743a138817 /bin/bash`

To copy file from running docker
`sudo docker cp <container id>:/sobel.jpg /dest/path`
