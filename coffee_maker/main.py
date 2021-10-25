from zk import ZK, const
import paho.mqtt.client as mqtt
import socket
broker_address = "62.210.9.28"
finalip = ''
for i in range(99,150) :
    #196.221.205.166
    #192.168.0.100
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    ip = "192.168.0."+str(i)
    result = socket_obj.connect_ex((ip,4370))
    print(result)
    if result == 0 :
        finalip = ip
        socket_obj.close()
        break
    socket_obj.close()
    
print(finalip)
