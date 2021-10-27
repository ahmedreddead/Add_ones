import threading
import time
import json
from zk import ZK, const
import paho.mqtt.client as mqtt
import socket
broker_address = "62.210.9.28"
finalip = ''
for i in range(120,150) :
    #196.221.205.166
    #192.168.0.100
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    ip = "196.221.205."+str(i)
    result = socket_obj.connect_ex((ip,4370))
    print(result)
    if result == 0 :
        finalip = ip
        socket_obj.close()
        break
    socket_obj.close()
print(finalip)
def live () :
    Thread  = threading.Timer(60.0, live)
    Thread.start()
    listOfId = []
    listOfDate = []
    listOfTime = []
    zk = ZK(finalip, port=4370, timeout=5, password=0, force_udp=True, ommit_ping=True)
    conn = zk.connect()
    conn.enable_device()
    attendances = conn.get_attendance()
    print (type (attendances) )
    for i in attendances : 
        listvalue = str(i).split (" ")
        listOfId.append(listvalue[1])
        listOfDate.append(listvalue[3])
        listOfTime.append(listvalue[4])
    #print(listOfId[index])
    #print(listOfDate)
    #print(listOfTime)
    Nameslist =[]
    idlist = []
    jsonlist = []
    conn.delete_user(user_id=9)
    users = conn.get_users()
    for user in users:
        Nameslist.append(user.name)
        idlist.append(user.user_id)
    
    print(Nameslist)
    print(idlist)
    for n,name in zip (idlist,Nameslist) :
        for i in reversed( range(len(listOfId)) ) :
            if listOfId [i] == n :
                index = i 
                #print(listOfId[index])
                print(name)
                print(listOfDate[index])
                print(listOfTime[index])
                jsonname = { "Name": name , "Date": listOfDate[index] , "Time": listOfTime[index]}
                print (json.dumps (jsonname))
                jsonlist.append (json.dumps (jsonname))
                break 

    print("creating new instance")
    client = mqtt.Client("P1")  # create new instance
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    client.subscribe("LastAttendance")
    for i in range(len (jsonlist)) :
        client.publish("LastAttendance/"+ str (i), str(jsonlist[i]))

live()
