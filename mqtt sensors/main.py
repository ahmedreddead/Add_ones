import time
import threading

import paho.mqtt.client as mqtt
import socket
broker_address = "192.168.0.100"
def live () :
    Thread  = threading.Timer(120.0, live)
    Thread.start()
    print("creating new instance")
    client = mqtt.Client("P1")  # create new instance
    print("connecting to broker")
    #client.username_pw_set(username="mqtt-user", password="0000")
    client.username_pw_set(username="homeassistant", password="yayeeheed8eezaechiwu4thahbaij2eiki0eim8Bo1chahbatief4Ohs1mait0Ph")
    client.connect(broker_address)  # connect to broker
    client.publish("hu","100 %")
    client.publish("hu1","58 %")
    client.publish("hu2","40 %")
    client.publish("hu3","46 %")
    client.publish("hu4","42 %")
    client.publish("hu5","55 %")
    client.publish("hu6","58 %")
    client.publish("hu7","40 %")
    client.publish("hu8","46 %")
    client.publish("hu9","90 %")

    client.publish("temp","18.5°C 58 %RH")
    client.publish("temp1","15.4°C 40 %RH ")
    client.publish("temp2","19.8°C 46 %RH")
    client.publish("temp3","15.2°C 58 %RH")
    client.publish("temp4","5.2°C 100 %RH")

    client.publish("temp5","18.5°C 58 %RH")
    client.publish("temp6","19.4°C 43 %RH")
    client.publish("temp7","19.8°C 55 %RH")
    client.publish("temp8","15.2°C 45 %RH")
    client.publish("temp9","7.3°C 90 %RH")

live()

    

    
