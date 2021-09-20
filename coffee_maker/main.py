import os
import cv2
import numpy as np
import threading
import socket
import sys
import binascii
import pandas as pd
from datetime import date
from datetime import datetime
import time
import os.path
from os import path
#pyinstaller --onefile Main_v1.py --icon=img/rob.ico
ErrorFlag =0
BUTTON = ''
def Save_sensorNames(listnew) :
    textfile = open("Names.txt", "w")
    for element in listnew:
        textfile.write(element + "\n")
    textfile.close()
def Load_Names () :
    text_file = open("Names.txt", "r")
    lines = text_file.readlines()
    Nlist = [i.replace("\n","") for i in lines ]
    return Nlist
def Load_GatewayAndSensorsId_Tolist():
    lengatway = 16
    lensensor = 8
    list1 = []
    text_file = open("a_file.txt", "r")
    lines = text_file.readlines()
    for i in lines :
        list1.append(i.replace("\n",""))
    if len(list1[0])< lengatway :
        lenofzeros = lengatway - len(list1[0])
        list1[0]= lenofzeros*"0"+list1[0]
    for i in range(len(list1)) :
        if len(list1[i]) < lensensor:
            lenofzeros = lensensor - len(list1[i])
            list1[i] = lenofzeros * "0" + list1[i]
    #print(list1)
    text_file.close()
    return list1
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
def PreProceesData_EnvironMon ():
    global ErrorFlag
    try:
        testout()
    except :
        ErrorFlag = 1

    if ErrorFlag == 0 :
        Thread  = threading.Timer(20.0, PreProceesData_EnvironMon)
        Thread.start()
    data = pd.read_csv("data.csv",encoding= 'unicode_escape')
    columsName = [colum for colum in data]
    Names =[name.strip() for name in data[columsName[1]]]
    Names.insert(0,columsName[1])
    print(Names)
    Reading =[name for name in data[columsName[2]]]
    Reading.insert(0,columsName[2])
    NamesTemp = []
    NamesHum = []
    ReadingTemp = []
    ReadingHum = []
    for num in range(len(Names)) :
        if "T"  in Names[num] or  "Temperature" in Names[num] or "Temp" in Names[num] or "Fridge" in Names[num]:
            Names[num] =Names[num].replace("Temperature", "")
            Names[num] =Names[num].replace("Temp", "")
            Names[num] =Names[num].replace("T", "")
            Names[num] = Names[num].strip()
            a = Names[num]
            if str (a[-1]) == "-" :
                Names[num] = Names[num][:-1]
            NamesTemp.append(Names[num])
            ReadingTemp.append(Reading[num])
        if "RH"  in Names[num] :
            Names[num] =Names[num].replace("RH", "")
            Names[num] = Names[num].strip()
            a = Names[num]
            if str (a[-1]) == "-" :
                Names[num] = Names[num][:-1]
            NamesHum.append(Names[num])
            ReadingHum.append(Reading[num])
    print(Names)
    FinalNames = []
    FinalTemp =[]
    FinalHem =[]
    for i in Names:
        if i not in FinalNames:
            FinalNames.append(i)
    print(FinalNames)
    for Sname in FinalNames :
        if Sname in NamesTemp and Sname in NamesHum :
            indexTemp =NamesTemp.index(Sname)
            indexhem =NamesHum.index(Sname)
            FinalTemp.append(ReadingTemp[indexTemp])
            FinalHem.append(ReadingHum[indexhem])
        else:
            if Sname in NamesTemp :
                indexTemp = NamesTemp.index(Sname)
                hem = 255
                FinalTemp.append(ReadingTemp[indexTemp])
                FinalHem.append(hem)
            if Sname in NamesHum :
                Temp = 255
                indexhem = NamesHum.index(Sname)
                FinalTemp.append(Temp)
                FinalHem.append(ReadingHum[indexhem])
    print(len (FinalTemp))
    print(len (FinalHem))
    hexTempList = [TempmeratureToHex(value) for value in FinalTemp]
    hexHumList = [HumidityToHex(value1) for value1 in FinalHem]
    send_packetWithName(hexTempList , hexHumList,FinalNames)
def send_packetWithName(templist , humeditylist,Names):
    sensorlist = Load_GatewayAndSensorsId_Tolist()
    print(sensorlist)
    gatewaycode = sensorlist[0]
    sensorlist.remove(gatewaycode)
    NamesOfDataBase = Load_Names()
    date_time = Get_Date() +Get_Time()
    TCP_IP = '62.210.9.28'
    TCP_PORT = 5029
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    try:
        for Sensor_Name in NamesOfDataBase :
            if Sensor_Name in Names :
                indexDataBase = NamesOfDataBase.index(Sensor_Name)
                indexNames = Names.index(Sensor_Name)
                packet = CreatePacket(gatewaycode, sensorlist[indexDataBase], templist[indexNames], humeditylist[indexNames], date_time)
                s.send(packet)

        print("packet sent")

    except :
            print("there are error in sensor number or sever ")
def send_packet(templist , humeditylist):
    sensorlist = Load_GatewayAndSensorsId_Tolist()
    print(sensorlist)
    gatewaycode = sensorlist[0]
    sensorlist.remove(gatewaycode)
    date_time = Get_Date() +Get_Time()
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

def PreProceesData_Lascar () :
    global ErrorFlag
    try:
        testout()
    except :
        ErrorFlag = 1

    if ErrorFlag == 0 :
        Thread  = threading.Timer(20.0, PreProceesData_Lascar)
        Thread.start()
    TempList = []
    HimList = []
    for i in range(50):
        if os.path.isfile('sensor'+str(i)+'.wdf'):
            text_file = open('sensor'+str(i)+'.wdf', "r")
            lines = text_file.readlines()
            Temp = lines[-1].split()[1].split(",")[1]
            Humidiy = lines[-1].split()[1].split(",")[2]
            TempList.append(Temp)
            HimList.append(Humidiy)
    print(TempList,HimList)
    hexTempList = [TempmeratureToHex(value) for value in TempList]
    hexHumList = [HumidityToHex(value1) for value1 in HimList]
    send_packet(hexTempList, hexHumList)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    start_time = time.time()
    if os.path.isfile('sensor1.wdf'):
        PreProceesData_Lascar()
    elif os.path.isfile('data.csv') :
        PreProceesData_EnvironMon()
    print("--- %s seconds ---" % (time.time() - start_time))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
