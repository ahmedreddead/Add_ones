import os
import numpy as np
import threading
import socket
import binascii
from datetime import date
from datetime import datetime

def Get_Date():
    today = date.today()
    d3 = today.strftime("%m/%d/%y")
    d3 = d3.split('/')
    month = hex(int(d3[0])).replace("0x", "")
    day = hex(int(d3[1])).replace("0x", "")
    year = hex(int(d3[2])).replace("0x", "")
    if len(month) == 1:
        month = month.replace(month, "0" + month)
    if len(day) == 1:
        day = day.replace(day, "0" + day)
    if len(year) == 1:
        year = year.replace(year, "0" + year)
    a= year + month + day
    return a
def Get_Time() :
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    d3 = current_time.split(':')
    hour = hex(int(d3[0])).replace("0x", "")
    minits = hex(int(d3[1])).replace("0x", "")
    sec = hex(int(d3[2])).replace("0x", "")
    if len(hour) == 1:
        hour = hour.replace(hour, "0" + hour)
    if len(minits) == 1:
        minits = minits.replace(minits, "0" + minits)
    if len(sec) == 1:
        sec = sec.replace(sec, "0" + sec)
    a= hour + minits + sec
    return a
def TempmeratureToHex (a) :
    NagitiveValue = str(4)
    PositiveValue = str(0)
    valueOfTemp = ''
    if float(a) > 0 :
        valueOfTemp = PositiveValue
    else:
        valueOfTemp =NagitiveValue

    a = hex(int(float(a)*10 ))
    a =str ( a)
    a = a.replace("0x", "")
    if len(a) == 2:
        a = a.replace(a, valueOfTemp +"0" + a)
    if len(a) == 3:
        a = a.replace(a, valueOfTemp + a)
    return a
def HumidityToHex (a) :
    a = hex(int(float(a)))
    a = a.replace("0x", "")
    if len(a)== 1 :
        a = a.replace(a,"0" +a)
    return a
def CreatePacket (GatewayID, SensorId , Temp , Hum , Date) :
    P1 = "545A00362424"
    P3 = "0406"
    P4 = "02190000"
    P5 = GatewayID
    P6 = Date
    P7 = "0000"
    P8 = "0008"
    P9 = "AA"
    P10 = "80"
    P11 = "0000"
    P12 = "019F"
    P13 = "04D0"
    PP = "000E00010B"
    IDsen = SensorId
    SATATUS = "00"
    battery = "0E33"
    tem = Temp
    hu = Hum
    RSSI = "2D"
    P14 = "0122"
    P15 = "29D3"
    P16 = "0D0A"
    packet1 = P1 + P3 + P4 + P5 + P6 + P7 + P8 + P9 + P10 + P11 + P12 + P13 + PP + IDsen + SATATUS + battery + tem + hu + RSSI + P14 + P15 + P16
    binary_string1 = binascii.unhexlify(packet1)
    return  binary_string1
def send_packet():
    Thread = threading.Timer(20.0, send_packet)
    Thread.start()
    TempList = ['99.2','88.2','77.2']
    HimList = ['44','88','77']
    templist = [TempmeratureToHex(value) for value in TempList]
    humeditylist = [HumidityToHex(value1) for value1 in HimList]
    sensorlist = ['0100010001000101','10010011','10010012','10010013']
    print(sensorlist)
    gatewaycode = sensorlist[0]
    sensorlist.remove(gatewaycode)
    date_time = Get_Date() + Get_Time()
    TCP_IP = '62.210.9.28'
    TCP_PORT = 5029
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    try:
        for i,t,h  in zip (sensorlist , templist , humeditylist ) :
                packet = CreatePacket(gatewaycode, i, t, h, date_time)
                s.send(packet)
        print("packet sent")

    except :
            print("there are error in sensor number or sever ")
send_packet()
