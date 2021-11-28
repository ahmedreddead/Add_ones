import time
import threading

from zk import ZK, const
import paho.mqtt.client as mqtt
import socket
broker_address = "192.168.0.100"
finalip = '192.168.0.107'
def live () :
    Thread  = threading.Timer(25.0, live)
    Thread.start()
    zk = ZK(finalip, port=4370, timeout=5, password=0, force_udp=True, ommit_ping=True)
    conn = zk.connect()
    conn.enable_device()
    for attendance in conn.live_capture(10):
        if attendance is None:
            pass
        else:
            print("creating new instance")
            client = mqtt.Client("P1")  # create new instance
            print("connecting to broker")
            client.connect(broker_address)  # connect to broker
            client.subscribe("Attendance")
            print(attendance)
            client.publish("Attendance","ON")
            client.publish("Attendance/ID", str(attendance))

live()

    

    
