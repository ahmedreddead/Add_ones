import threading
import time
import json
from zk import ZK, const
import paho.mqtt.client as mqtt
import socket

broker_address = "62.210.9.28"
finalip = '192.168.0.107'

def live():
    Thread = threading.Timer(3600.0, live)
    Thread.start()
    listOfId = []
    listOfDate = []
    listOfTime = []
    zk = ZK(finalip, port=4370, timeout=15, password=0, force_udp=True, ommit_ping=True)
    conn = zk.connect()
    conn.enable_device()
    attendances = conn.get_attendance()
    print(type(attendances))
    for i in attendances:
        listvalue = str(i).split(" ")
        listOfId.append(listvalue[1])
        listOfDate.append(listvalue[3])
        listOfTime.append(listvalue[4])
    # print(listOfId[index])
    # print(listOfDate)
    # print(listOfTime)
    Nameslist = []
    idlist = []
    jsonlist = []
    users = conn.get_users()
    for user in users:
        Nameslist.append(user.name)
        idlist.append(user.user_id)

    print(Nameslist)
    print(idlist)
    for n, name in zip(idlist, Nameslist):
        for i in reversed(range(len(listOfId))):
            if listOfId[i] == n:
                index = i
                # print(listOfId[index])
                print(name)
                print(listOfDate[index])
                print(listOfTime[index])

                lastDate = listOfDate[index]
                lastTime = listOfTime[index]
                listTimesOfCurrentDay = []
                for i in reversed(range(len(listOfDate))):
                    if lastDate == listOfDate[i] :
                        listTimesOfCurrentDay.append(listOfTime[i])
                firstTime = listTimesOfCurrentDay[-1]
                Lasthours, Lastmin, Lastsec = lastTime.split(":")
                firsthours, firstmin, firstsec = firstTime.split(":")

                hours =   str ( int(Lasthours) - int (firsthours)  )

                jsonname = {"Name": name, "Date": listOfDate[index], "FirstAttendance": firstTime  , "LastAttendance": lastTime , "WorkingHours" :hours}
                print(json.dumps(jsonname))
                jsonlist.append(json.dumps(jsonname))

                break



    print("creating new instance")
    client = mqtt.Client("P1")  # create new instance
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    client.subscribe("LastAttendance")
    for i in range(len(jsonlist)):
        client.publish("LastAttendance/" + str(i), str(jsonlist[i]))


live()
