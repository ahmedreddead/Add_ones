import time
import threading

import paho.mqtt.client as mqtt
import socket
broker_address = "192.168.0.100"
def live () :
    Thread  = threading.Timer(60.0, live)
    Thread.start()
    print("creating new instance")
    client = mqtt.Client("P1")  # create new instance
    print("connecting to broker")
    client.username_pw_set(username="mqtt-user", password="0000")
    client.connect(broker_address)  # connect to broker
    client.publish("hu","55 %")
    client.publish("hu1","58 %")
    client.publish("hu2","40 %")
    client.publish("hu3","46 %")
    client.publish("hu4","42 %")

    client.publish("temp","22.5°C")
    client.publish("temp1","21.4°C")
    client.publish("temp2","19.8°C")
    client.publish("temp3","15.2°C")
    client.publish("temp4","10.3°C")

live()

    

    
